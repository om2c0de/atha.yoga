from rest_framework import serializers
from core.app.utils.serializers import UnimplementedSerializer


class CourseCommentCreateRequest(UnimplementedSerializer):
    text = serializers.CharField(max_length=512)
