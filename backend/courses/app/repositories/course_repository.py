from typing import Optional

from django.db.models import QuerySet, Q, F, Prefetch, Count, Exists, OuterRef, Avg
from elasticsearch_dsl import Q as EQ
from rest_framework.exceptions import NotFound

from core.app.repositories.base_repository import BaseRepository
from core.models import User, QuestionnaireTeacher, QuestionnaireTeacherStatuses
from courses.app.repositories.types import CourseFilterData
from courses.documents import BaseCourseDocument
from courses.models import Course, Lesson, BaseCourse, CourseStatuses


class CourseRepository(BaseRepository):
    model = Course

    def __init__(self, user: User = None):
        self.user = user

    def store(self, course: Course) -> None:
        course.save()

    def find_by_id(
        self, id_: int, raise_exception: bool = False, fetch_rels: bool = False
    ) -> Optional[Course]:
        query = self.model.objects.filter(pk=id_)
        if fetch_rels:
            query = self.fetch_relations(queryset=query)
        course = query.first()
        if not course and raise_exception:
            raise NotFound(f"Undefined course with id {id_}")
        return course

    def find_user_favorite_courses(self, user: User) -> QuerySet[Course]:
        return user.favorite_courses.all()

    def add_user_favorite_course(self, user: User, course: Course) -> None:
        course.base_course.favorites.add(user)

    def remove_user_favorite_course(self, user: User, course: Course) -> None:
        course.base_course.favorites.remove(user)

    def find_public_all(self, user_id: Optional[int] = None) -> QuerySet[Course]:
        return self.model.objects.filter(
            Q(status=CourseStatuses.PUBLISHED) | Q(base_course__teacher_id=user_id)
        )

    def filter(
        self, data: CourseFilterData, base_query: QuerySet[Course]
    ) -> QuerySet[Course]:
        filter_query = Q()
        if "query" in data:
            query = Course.objects.filter(
                base_course_id__in=BaseCourseDocument.search()
                .query(
                    EQ(
                        "multi_match",
                        query=data["query"],
                        fields=["name", "description"],
                        fuzziness="AUTO:2,4",
                    )
                )
                .to_queryset()
                .values("id")
            )
            if not query.exists():
                query = base_query.filter(
                    Q(base_course__name__icontains=data["query"])
                    | Q(base_course__description__icontains=data["query"])
                )
            base_query = query
        if "complexity" in data:
            filter_query &= Q(base_course__complexity=data["complexity"])
        if "start_datetime" in data:
            filter_query &= Q(start_datetime__date=data["start_datetime"].date())
        if "day" in data:
            filter_query &= Q(start_datetime__week_day=data["day"])
        if "end_datetime" in data:
            base_query = base_query.annotate(
                end_datetime=F("duration") + F("start_datetime")
            )
            filter_query &= Q(end_datetime__lte=data["end_datetime"])
        return base_query.filter(filter_query).order_by("-id")

    def fetch_relations(self, queryset: QuerySet[Course]) -> QuerySet[Course]:
        queryset = (
            queryset.select_related("base_course__teacher")
            .prefetch_related(
                Prefetch(
                    "lessons_set",
                    queryset=Lesson.objects.filter(
                        pk__in=Lesson.objects.order_by("id").values("id")[:15]
                    ),
                    to_attr="lessons",
                ),
                Prefetch(
                    "base_course__teacher",
                    queryset=User.objects.filter(
                        pk=OuterRef("teacher_id")
                    ).prefetch_related(
                        Prefetch(
                            "teacher_profiles",
                            queryset=QuestionnaireTeacher.objects.filter(
                                user_id=OuterRef("id"),
                                status=QuestionnaireTeacherStatuses.ACCEPTED,
                            ),
                        )
                    ),
                ),
            )
            .annotate(
                reviews_count=Count("base_course__reviews"),
                comments_count=Count("base_course__comments"),
                rate=Avg("base_course__reviews__star_rating"),
            )
        )
        if self.user and self.user.id:
            queryset = queryset.annotate(
                participant=Exists(
                    Lesson.objects.filter(
                        course_id=OuterRef("id"), participants__id=self.user.id
                    )
                ),
                favorite=Exists(
                    Course.objects.filter(
                        pk=OuterRef("id"), base_course__favorites__id=self.user.id
                    )
                ),
            )

        return queryset


class BaseCourseRepository(BaseRepository):
    model = BaseCourse

    def store(self, base_course: BaseCourse) -> None:
        base_course.save()

    def find_by_id_teacher(self, id_: int, teacher_id: int) -> Optional[BaseCourse]:
        return self.model.objects.filter(
            pk=id_, teacher_id=teacher_id
        ).first()
