from rest_framework import serializers

from core.app.utils.serializers import UnimplementedSerializer


class UserProfileRequest(UnimplementedSerializer):
    profile_photo = serializers.ImageField()
