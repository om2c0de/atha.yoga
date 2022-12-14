from rest_framework.serializers import ModelSerializer

from core.models import User
from courses.models import CourseComment


class CourseCommentUserResource(ModelSerializer):
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


class CourseCommentResource(ModelSerializer):
    user = CourseCommentUserResource()

    class Meta:
        model = CourseComment
        fields = [
            "id",
            "base_course",
            "text",
            "user",
            "created_at",
        ]
