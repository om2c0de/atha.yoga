from functools import cached_property

from rest_framework.exceptions import NotFound, PermissionDenied

from core.app.repositories.user_repository import UserRepository
from core.models import User
from lessons.app.repositories.comment_repository import CourseCommentRepository
from lessons.app.repositories.lesson_repository import CourseRepository
from lessons.models import CourseComment


class CourseCommentCreate:
    repository = CourseCommentRepository()
    user_repository = UserRepository()
    course_repository = CourseRepository()

    def __init__(self, course_id: int, user: User, text: str):
        self.text = text
        self.user = user
        self.course_id = course_id

    @cached_property
    def comment(self) -> CourseComment:
        course = self.course_repository.find_by_id(id_=self.course_id)
        if not course:
            raise NotFound(f"Undefined course with id {self.course_id}")

        comment = CourseComment()
        comment.user = self.user
        comment.course = course
        comment.text = self.text

        return comment

    def create(self) -> CourseComment:
        self.repository.store(comment=self.comment)
        return self.comment


class CourseCommentRemove:
    repository = CourseCommentRepository()

    def __init__(self, comment_id: int, user: User):
        self.comment_id = comment_id
        self.user = user

    @cached_property
    def comment(self) -> CourseComment:
        comment = self.repository.find_by_id(id_=self.comment_id)
        if not comment:
            raise NotFound(f"Undefined comment with id {self.comment_id}")
        if comment.user.id != self.user.id:
            raise PermissionDenied(
                f"User with id {self.user.id} can't remove comment with id {self.comment_id}"
            )

        return comment

    def remove(self) -> CourseComment:
        self.repository.remove(comment=self.comment)
        return self.comment
