from typing import Optional

from django.db.models import QuerySet, Q, F
from elasticsearch_dsl import Q as EQ
from rest_framework.exceptions import PermissionDenied

from core.app.repositories.base_repository import BaseRepository
from core.models import User
from lessons.app.repositories.types import LessonFilterData
from lessons.documents import LessonDocument
from lessons.models import Lesson, Ticket


class LessonRepository(BaseRepository):
    model = Lesson

    def store(self, lesson: Lesson) -> None:
        lesson.save()

    def find_by_id(self, id_: int) -> Optional[Lesson]:
        return self.model.objects.filter(pk=id_).first()

    def find_by_id_teacher(self, id_: int, teacher_id: int) -> Optional[Lesson]:
        return self.model.objects.filter(pk=id_, teacher_id=teacher_id).first()

    def find_user_favorite_lessons(self, user: User) -> QuerySet[Lesson]:
        return user.favorite_lessons.all()

    def add_user_favorite_lesson(self, user: User, lesson: Lesson) -> None:
        lesson.favorites.add(user)

    def remove_user_favorite_lesson(self, user: User, lesson: Lesson) -> None:
        lesson.favorites.remove(user)

    def filter(self, data: LessonFilterData) -> QuerySet[Lesson]:
        base_query = self.model.objects.all()
        filter_query = Q()
        if "query" in data:
            base_query = (
                LessonDocument.search()
                .query(
                    EQ(
                        "multi_match",
                        query=data["query"],
                        fields=["name", "description"],
                        fuzziness="AUTO",
                    )
                )
                .to_queryset()
            )
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
        return base_query.filter(filter_query)


class TicketRepository(BaseRepository):
    model = Ticket

    def store(self, ticket: Ticket) -> None:
        ticket.save()

    def del_zero_ticket(self, ticket: Ticket) -> None:
        ticket.delete()

    def ticket_for_lesson(self, lesson: Lesson, user: User) -> Optional[Ticket]:
        return self.model.objects.filter(lesson=lesson.id, user=user).first()

    def find_lesson_by_id(self, id_: int) -> Lesson:
        lesson = LessonRepository.model.objects.filter(pk=id_).first()
        if not lesson:
            raise PermissionDenied("Lesson does not exist")
        return lesson
