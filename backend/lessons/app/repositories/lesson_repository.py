from typing import Optional

from django.db.models import QuerySet, Q, F
from elasticsearch_dsl import Q as EQ

from core.app.repositories.base_repository import BaseRepository
from core.models import User
from lessons.app.repositories.types import CourseFilterData
from lessons.documents import CourseDocument
from lessons.models import Course, Ticket


class CourseRepository(BaseRepository):
    model = Course

    def store(self, course: Course) -> None:
        course.save()

    def find_by_id(self, id_: int) -> Optional[Course]:
        return self.model.objects.filter(pk=id_).first()

    def find_by_id_teacher(self, id_: int, teacher_id: int) -> Optional[Course]:
        return self.model.objects.filter(pk=id_, teacher_id=teacher_id).first()

    def find_user_favorite_courses(self, user: User) -> QuerySet[Course]:
        return user.favorite_courses.all()

    def add_user_favorite_course(self, user: User, course: Course) -> None:
        course.favorites.add(user)

    def remove_user_favorite_course(self, user: User, course: Course) -> None:
        course.favorites.remove(user)

    def filter(self, data: CourseFilterData) -> QuerySet[Course]:
        base_query = self.model.objects.all()
        filter_query = Q()
        if "query" in data:
            query = (
                CourseDocument.search()
                .query(
                    EQ(
                        "multi_match",
                        query=data["query"],
                        fields=["name", "description"],
                        fuzziness="AUTO:2,4",
                    )
                )
                .to_queryset()
            )
            if not query.exists():
                query = base_query.filter(
                    Q(name__icontains=data["query"])
                    | Q(description__icontains=data["query"])
                )
            base_query = query
        if "complexity" in data:
            filter_query &= Q(complexity=data["complexity"])
        if "start_datetime" in data:
            filter_query &= Q(start_datetime__date=data["start_datetime"].date())
        if "day" in data:
            filter_query &= Q(start_datetime__weekday=data["day"])
        if "end_datetime" in data:
            base_query = base_query.annotate(
                end_datetime=F("duration") + F("start_datetime")
            )
            filter_query &= Q(end_datetime__lte=data["end_datetime"])
        return base_query.filter(filter_query).order_by("-id")


class TicketRepository(BaseRepository):
    model = Ticket

    def store(self, ticket: Ticket) -> None:
        ticket.save()

    def destroy(self, ticket: Ticket) -> None:
        ticket.delete()

    def ticket_for_course(self, course_id: int, user: User) -> Optional[Ticket]:
        return self.model.objects.filter(course_id=course_id, user=user.id).first()

    def ticket_for_course_to_update(
            self, course_id: int, user: User
    ) -> Optional[Ticket]:
        return (
            self.model.objects.select_for_update()
            .filter(course_id=course_id, user=user.id)
            .first()
        )
