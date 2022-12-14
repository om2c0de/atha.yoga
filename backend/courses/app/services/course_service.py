import logging
from functools import cached_property

from django.conf import settings
from django.db import transaction
from furl import furl
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from core.app.services.payment_service import TinkoffPaymentService
from core.app.services.types import PaymentStatuses
from core.app.utils.util import setup_resource_attributes
from core.models import User, TransactionStatuses
from core.models import UserRoles
from courses.app.repositories.course_cycle_repository import CourseCycleRepository
from courses.app.repositories.course_repository import (
    CourseRepository,
    BaseCourseRepository,
)
from courses.app.repositories.lesson_repository import LessonRepository
from courses.app.repositories.ticket_repository import TicketRepository
from courses.app.repositories.transaction_repository import TicketTransactionRepository
from courses.app.services.types import CourseCreateData
from courses.app.services.types import (
    CourseUpdateData,
)
from courses.models import (
    Course,
    Lesson,
    Ticket,
    TicketTransaction,
    CoursePaymentTypes,
    CourseCycle,
    CourseSchedule,
    BaseCourse,
    CourseStatuses,
)


class CourseCreator:
    repos = CourseRepository()
    base_course_repos = BaseCourseRepository()
    course_cycle_repos = CourseCycleRepository()
    lesson_repos = LessonRepository()

    def __init__(self, data: CourseCreateData, user: User):
        self._data = data
        self._user = user

    def _base_course(self) -> BaseCourse:
        base_course = BaseCourse()
        base_course.name = self._data["name"]
        base_course.description = self._data["description"]
        base_course.course_type = self._data["course_type"]
        base_course.complexity = self._data["complexity"]
        base_course.level = list(self._data["level"])
        base_course.teacher = self._user
        return base_course

    def _course(self, base_course: BaseCourse) -> Course:
        course = Course()
        course.base_course = base_course
        course.link = self._data["link"]
        course.link_info = self._data["link_info"]
        course.duration = self._data["duration"]
        course.start_datetime = self._data["start_datetime"]
        course.deadline_datetime = self._data["deadline_datetime"]
        course.payment = self._data["payment"]
        course.price = self._data["price"]
        if self._data["is_draft"]:
            course.status = CourseStatuses.DRAFT
        course.schedule = [
            CourseSchedule(weekday=item["weekday"], start_time=item["start_time"])
            for item in self._data["lessons"]
        ]
        return course

    def _init_course_cycle(self, course: Course) -> CourseCycle:
        course_cycle = CourseCycle()
        course_cycle.course = course
        course_cycle.start_at = course.start_datetime
        course_cycle.end_at = course.deadline_datetime
        return course_cycle

    def _create_lessons(self, course: Course) -> None:
        if not self._data["lessons"]:
            return
        lessons_to_create = []
        possible_lessons = course.lessons_in_range(
            date_start=course.start_datetime,
            date_end=course.deadline_datetime,
        )
        if not possible_lessons:
            raise ValidationError("Undefined any lesson to create")

        for lesson_datetime in possible_lessons:
            lesson = Lesson()
            lesson.course = course
            lesson.start_at = lesson_datetime
            lessons_to_create.append(lesson)
        self.lesson_repos.bulk_create(objs=lessons_to_create)

    def _created_course(self) -> Course:
        base_course = self._base_course()
        course = self._course(base_course=base_course)
        self.base_course_repos.store(base_course=base_course)
        self.repos.store(course=course)
        return course

    def create(self) -> Course:
        if not self._user.has_role(UserRoles.TEACHER):
            raise PermissionDenied("User must be teacher for create courses")
        course = self._created_course()
        if self._data["lessons"]:
            course_cycle = self._init_course_cycle(course=course)
            self.course_cycle_repos.store(course_cycle)
        self._create_lessons(course=course)
        return course


class BaseCourseUpdator:
    repository = BaseCourseRepository()

    def __init__(self, user: User, pk: int, data: CourseUpdateData):
        self._pk = pk
        self._user = user
        self._data = data

    def update(self) -> BaseCourse:
        base_course = self.repository.find_by_id_teacher(
            id_=self._pk, teacher_id=self._user.id
        )
        if not base_course:
            raise NotFound(f"Undefined base_course with pk {self._pk}")
        setup_resource_attributes(
            instance=base_course,
            validated_data=self._data,
            fields=list(CourseUpdateData.__annotations__.keys()),
        )
        self.repository.store(base_course=base_course)
        return base_course


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


class TicketBuyConfirmError(Exception):
    pass


class TicketBuy:
    repository = TicketRepository()
    course_repository = CourseRepository()
    transaction_repository = TicketTransactionRepository()

    def ticket(self, course: Course, user: User) -> Ticket:
        ticket = self.repository.ticket_for_course(course_id=course.id, user=user)
        if not ticket:
            ticket = self._init_ticket(course=course, user=user)
            self.repository.store(ticket=ticket)
        return ticket

    def _init_ticket(self, course: Course, user: User) -> Ticket:
        ticket = Ticket()
        ticket.course = course
        ticket.user = user
        ticket.amount = 0
        return ticket

    def _init_ticket_transaction(
        self, ticket: Ticket, amount: int
    ) -> TicketTransaction:
        ticket_transaction = TicketTransaction()
        ticket_transaction.ticket = ticket
        ticket_transaction.ticket_amount = amount
        ticket_transaction.amount = ticket.course.price * amount
        ticket_transaction.user = ticket.user
        return ticket_transaction

    def buy(self, course_id: int, user: User, amount: int) -> str:
        course = self.course_repository.find_by_id(id_=course_id, raise_exception=True)
        if course.payment != CoursePaymentTypes.PAYMENT:
            raise ValidationError("The course does not require tickets")
        ticket = self.ticket(course=course, user=user)
        ticket_transaction = self._init_ticket_transaction(ticket=ticket, amount=amount)
        self.transaction_repository.store(transaction=ticket_transaction)
        pay_info = TinkoffPaymentService().init_pay(
            amount=ticket_transaction.amount,
            transaction_id=ticket_transaction.id,
            description=ticket.course.base_course.name,
            success_url=furl(url=settings.BACKEND_URL)
            .join(f"api/courses/success-payment/{ticket_transaction.id}/")
            .url,
        )
        ticket_transaction.payment_id = pay_info.PaymentId
        self.transaction_repository.store(transaction=ticket_transaction)
        return pay_info.PaymentURL

    def ticket_transaction(self, transaction_id: str) -> TicketTransaction:
        ticket_transaction = self.transaction_repository.find_by_id(id_=transaction_id)
        if not ticket_transaction:
            logging.getLogger("daily_log").error(
                f"Undefined transaction with pk {transaction_id}"
            )
            raise TicketBuyConfirmError
        return ticket_transaction

    def update_tickets_amount(self, ticket_transaction: TicketTransaction) -> None:
        with transaction.atomic():
            ticket = self.repository.find_by_id_to_update(
                id_=ticket_transaction.ticket_id, user=ticket_transaction.user
            )
            ticket.amount += ticket_transaction.ticket_amount
            self.repository.store(ticket=ticket)

    def confirm(self, transaction_id: str) -> str:
        try:
            ticket_transaction = self.ticket_transaction(transaction_id=transaction_id)
            if ticket_transaction.status != TransactionStatuses.INITIAL:
                raise TicketBuyConfirmError
            payment_status = TinkoffPaymentService().payment_status(
                payment_id=ticket_transaction.payment_id
            )
            if payment_status != PaymentStatuses.CONFIRMED:
                ticket_transaction.status = TransactionStatuses.DECLINED
                self.transaction_repository.store(transaction=ticket_transaction)
                raise TicketBuyConfirmError
            self.update_tickets_amount(ticket_transaction=ticket_transaction)
        except TicketBuyConfirmError:
            return furl(settings.SITE_URL).join("failed-payment").url
        else:
            ticket_transaction.status = TransactionStatuses.CONFIRMED
            self.transaction_repository.store(transaction=ticket_transaction)
            return furl(settings.SITE_URL).join("success-payment").url


class CourseParticipateService:
    repository = TicketRepository()
    lesson_repository = LessonRepository()

    def __init__(self, lesson_id: int, user: User):
        self._lesson_id = lesson_id
        self._user = user

    @cached_property
    def lesson(self) -> Lesson:
        lesson = self.lesson_repository.find_by_id(id_=self._lesson_id)
        if not lesson:
            raise NotFound(f"Undefined lesson with id {self._lesson_id}")
        return lesson

    def participate(self) -> str:
        participant = self.lesson_repository.is_participant(
            lesson=self.lesson, user=self._user
        )
        if participant:
            return self.lesson.course.link

        with transaction.atomic():
            ticket = self.repository.ticket_for_course_to_update(
                course_id=self.lesson.course.id, user=self._user
            )
            if not ticket or ticket.amount < 1:
                raise NotFound("You dont have ticket for this course")
            ticket.amount = int(ticket.amount) - 1

            self.lesson_repository.add_participant(lesson=self.lesson, user=self._user)

            self.repository.store(ticket=ticket)
        return ticket.course.link
