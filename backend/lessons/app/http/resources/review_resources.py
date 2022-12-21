from rest_framework.serializers import ModelSerializer

from core.models import User
from lessons.models import CourseReview


class CourseReviewUserResource(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "about",
            "avatar",
        ]


class CourseReviewResource(ModelSerializer):
    user = CourseReviewUserResource()

    class Meta:
        model = CourseReview
        fields = [
            "id",
            "text",
            "star_rating",
            "user",
            "created_at",
        ]
