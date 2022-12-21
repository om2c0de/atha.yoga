import datetime
from collections import defaultdict
from functools import cached_property
from typing import List, Dict

from django.db import transaction
from django.utils.timezone import now
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from core.app.utils.util import setup_resource_attributes
from core.models import User
from core.models import UserRoles
from lessons.app.repositories.lesson_repository import (
    CourseRepository,
    TicketRepository,
)
from lessons.app.repositories.schedule_repository import LessonRepository
from lessons.app.services.types import CourseCreateData
from lessons.app.services.types import (
    CourseUpdateData,
    LessonCreateData,
)
from lessons.models import Course, Lesson, Ticket


class CourseCreator:
    repos = CourseRepository()
    lesson_repos = LessonRepository()

    def __init__(self, data: CourseCreateData, user: User):
        self._data = data
        self._user = user

    @cached_property
    def course(self) -> Course:
        course = Course()
        course.name = self._data["name"]
        course.description = self._data["description"]
        course.course_type = self._data["course_type"]
        course.link = self._data["link"]
        course.link_info = self._data["link_info"]
        course.level = self._data["level"]
        course.duration = self._data["duration"]
        course.repeat_editing = self._data["repeat_editing"]
        course.start_datetime = self._data["start_datetime"]
        course.deadline_datetime = self._data["deadline_datetime"]
        course.payment = self._data["payment"]
        course.price = self._data["price"]
        course.complexity = self._data["complexity"]
        course.teacher = self._user
        return course

    @cached_property
    def mapped_lesson(self) -> Dict[int, List[LessonCreateData]]:
        mapped_lesson = defaultdict(list)
        for item in self._data["lesson"]:
            mapped_lesson[item["weekday"]].append(item)
        return mapped_lesson

    def _create_lesson(self) -> None:
        if not self._data["lesson"]:
            return
        lesson_to_create = []
        cur_date = self.course.start_datetime.date()
        while cur_date <= (
                self.course.deadline_datetime.date() + datetime.timedelta(days=1)
        ):
            if cur_date.weekday() in self.mapped_lesson:
                for course_info in self.mapped_lesson[cur_date.weekday()]:
                    course_datetime = datetime.datetime.combine(
                        date=cur_date, time=course_info["start_time"]
                    )
                    if self.course.deadline_datetime < course_datetime < now():
                        continue
                    lesson = Lesson()
                    lesson.course = self.course
                    lesson.start_at = course_datetime
                    lesson_to_create.append(lesson)
            cur_date += datetime.timedelta(days=1)
        self.lesson_repos.bulk_create(objs=lesson_to_create)

    def create(self) -> Course:
        if not self._user.has_role(UserRoles.TEACHER):
            raise PermissionDenied("User must be teacher for create courses")
        self.repos.store(course=self.course)
        self._create_lesson()
        return self.course


class courseUpdator:
    repository = CourseRepository()

    def __init__(self, user: User, pk: int, data: CourseUpdateData):
        self._pk = pk
        self._user = user
        self._data = data

    def update(self) -> Course:
        course = self.repository.find_by_id_teacher(
            id_=self._pk, teacher_id=self._user.id
        )
        if not course:
            raise NotFound(f"Undefined course with pk {self._pk}")
        setup_resource_attributes(
            instance=course, validated_data=self._data, fields=list(self._data.keys())
        )
        return course


class FavoriteCoursesWork:
    repository = CourseRepository()

    def __init__(self, user: User, course_id: int):
        self.user = user
        self.course_id = course_id

    @cached_property
    def course(self) -> Course:
        course = self.repository.find_by_id(id_=self.course_id)
        if not course:
            raise NotFound(f"Undefined course with id {self.course_id}")
        return course

    def add(self) -> Course:
        if self.course in self.repository.find_user_favorite_courses(user=self.user):
            raise ValidationError(
                f"Course with id {self.course_id} already in favorites"
            )
        self.repository.add_user_favorite_course(user=self.user, course=self.course)
        return self.course

    def remove(self) -> Course:
        if self.course not in self.repository.find_user_favorite_courses(
                user=self.user
        ):
            raise NotFound(f"Undefined course with id {self.course_id} in favorites")
        self.repository.remove_user_favorite_course(user=self.user, course=self.course)
        return self.course


class TicketWorkService:
    repository = TicketRepository()
    course_repository = CourseRepository()

    def _init_ticket(self, course_id: int, user: User, amount: int) -> Ticket:
        course = self.course_repository.find_by_id(id_=course_id)
        if not course:
            raise NotFound(f"Undefined course with id {course_id}")
        ticket = Ticket()
        ticket.course = course
        ticket.user = user
        ticket.amount = amount
        return ticket

    def buy(self, course_id: int, user: User, amount: int) -> Ticket:
        ticket = self.repository.ticket_for_course(course_id=course_id, user=user)
        if not ticket:
            ticket = self._init_ticket(course_id=course_id, user=user, amount=amount)
            self.repository.store(ticket=ticket)
            return ticket

        ticket.amount = int(ticket.amount) + int(amount)
        self.repository.store(ticket=ticket)
        return ticket


class CourseParticipateService:
    repository = TicketRepository()
    lesson_repository = LessonRepository()

    def __init__(self, lesson_id: int, user: User):
        self._lesson_id = lesson_id
        self._user = user

    @cached_property
    def lessoned_course(self) -> Lesson:
        lessoned_course = self.lesson_repository.find_by_id(id_=self._lesson_id)
        if not lessoned_course:
            raise NotFound(f"Undefined lessoned_course with id {self._lesson_id}")
        return lessoned_course

    def participate(self) -> str:
        participant = self.lesson_repository.is_participant(
            lessoned_course=self.lessoned_course, user=self._user
        )
        if participant:
            return self.lessoned_course.course.link

        with transaction.atomic():
            ticket = self.repository.ticket_for_course_to_update(
                course_id=self.lessoned_course.course.id, user=self._user
            )
            if not ticket or ticket.amount < 1:
                raise NotFound("You dont have ticket for this course")
            ticket.amount = int(ticket.amount) - 1

            self.lesson_repository.add_participant(
                lessoned_course=self.lessoned_course, user=self._user
            )

            self.repository.store(ticket=ticket)
        return ticket.course.link
