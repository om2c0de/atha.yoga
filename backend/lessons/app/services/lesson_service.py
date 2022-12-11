from functools import cached_property

from rest_framework.exceptions import NotFound, ValidationError

from core.models import User
from lessons.app.repositories.lesson_repository import LessonRepository
from lessons.app.repositories.schedule_repository import ScheduleRepository
from lessons.app.services.types import LessonCreateData
from lessons.models import Lesson, Schedule


class LessonCreator:
    repos = LessonRepository()
    schedule_repos = ScheduleRepository()

    def __init__(self, data: LessonCreateData, user: User):
        self._data = data
        self._user = user

    @cached_property
    def lesson(self) -> Lesson:
        lesson = Lesson()
        lesson.name = self._data["name"]
        lesson.description = self._data["description"]
        lesson.lesson_type = self._data["lesson_type"]
        lesson.link = self._data["link"]
        lesson.link_info = self._data["link_info"]
        lesson.level = self._data["level"]
        lesson.duration = self._data["duration"]
        lesson.repeat_editing = self._data["repeat_editing"]
        lesson.start_datetime = self._data["start_datetime"]
        lesson.deadline_date = self._data["deadline_date"]
        lesson.payment = self._data["payment"]
        lesson.price = self._data["price"]
        lesson.complexity = self._data["complexity"]
        lesson.teacher = self._user
        return lesson

    def _create_schedule(self) -> None:
        if not self._data["schedule"]:
            return
        schedule_to_create = []
        for item in self._data["schedule"]:
            schedule = Schedule()
            schedule.lesson = self.lesson
            schedule.weekday = item["weekday"]
            schedule.start_time = item["start_time"]
            schedule_to_create.append(schedule)
        self.schedule_repos.bulk_create(objs=schedule_to_create)

    def create(self) -> Lesson:
        # if not self._user.has_role(UserRoles.TEACHER):
        #     raise PermissionDenied("User must be teacher for create lessons")
        self.repos.store(lesson=self.lesson)
        self._create_schedule()
        return self.lesson


class FavoriteLessonsWork:
    repository = LessonRepository()

    def __init__(self, user: User, lesson_id: int):
        self.user = user
        self.lesson_id = lesson_id

    @cached_property
    def lesson(self) -> Lesson:
        lesson = self.repository.find_lesson_by_id(id_=self.lesson_id)
        if not lesson:
            raise NotFound(f"Undefined lesson with id {self.lesson_id}")
        return lesson

    def add(self) -> Lesson:
        if self.lesson in self.repository.get_user_favorite_lessons(user=self.user):
            raise ValidationError(
                f"Lesson with id {self.lesson_id} already in favorites"
            )
        self.repository.add_user_favorite_lesson(user=self.user, lesson=self.lesson)
        return self.lesson

    def remove(self) -> Lesson:
        if self.lesson not in self.repository.get_user_favorite_lessons(user=self.user):
            raise NotFound(f"Undefined lesson with id {self.lesson_id} in favorites")
        self.repository.remove_user_favorite_lesson(user=self.user, lesson=self.lesson)
        return self.lesson
