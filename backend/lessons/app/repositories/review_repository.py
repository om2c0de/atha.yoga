from django.db.models import QuerySet

from core.app.repositories.base_repository import BaseRepository
from lessons.models import CourseReview, Course


class CourseReviewRepository(BaseRepository):
    model = CourseReview

    def store(self, review: CourseReview) -> None:
        review.save()

    def find_by_course_id(self, course_id: int) -> QuerySet[CourseReview]:
        return self.model.objects.filter(course_id=course_id)

    def find_by_id(self, id_: int) -> CourseReview:
        return self.model.objects.filter(pk=id_).first()

    def check_for_user_review(self, user_id: int, course: Course) -> bool:
        return course.reviews.filter(user_id=user_id).exists()

    def remove(self, review: CourseReview) -> None:
        review.delete()
