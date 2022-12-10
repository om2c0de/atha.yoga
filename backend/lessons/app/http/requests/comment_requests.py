from rest_framework import serializers
from core.app.utils.serializers import UnimplementedSerializer


class CommentCreateRequest(UnimplementedSerializer):
    text = serializers.CharField(max_length=512)
    lesson_id = serializers.IntegerField(min_value=1)


class CommentListRequest(UnimplementedSerializer):
    lesson_id = serializers.IntegerField(min_value=1)
