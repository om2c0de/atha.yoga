from django.db.models import QuerySet

from core.app.repositories.base_repository import BaseRepository
from lessons.models import CourseComment


class CourseCommentRepository(BaseRepository):
    model = CourseComment

    def store(self, comment: CourseComment) -> None:
        comment.save()

    def find_by_course_id(self, course_id: int) -> QuerySet[CourseComment]:
        return self.model.objects.filter(course_id=course_id)

    def find_by_id(self, id_: int) -> CourseComment:
        return self.model.objects.filter(pk=id_).first()

    def remove(self, comment: CourseComment) -> None:
        comment.delete()
