from typing import List, Optional

from core.app.repositories.base_repository import BaseRepository
from core.models import User
from lessons.models import Lesson


class LessonRepository(BaseRepository):
    model = Lesson

    def bulk_create(self, objs: List[Lesson]) -> None:
        self.model.objects.bulk_create(objs)

    def find_by_id(self, id_: int) -> Optional[Lesson]:
        return self.model.objects.filter(pk=id_).first()

    def is_participant(
            self, lessoned_course: Lesson, user: User
    ) -> Optional[Lesson]:
        return lessoned_course.participants.filter(id=user.id)

    def add_participant(self, lessoned_course: Lesson, user: User) -> None:
        return lessoned_course.participants.add(user)
