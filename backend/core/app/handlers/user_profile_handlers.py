from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from core.app.http.requests.profile_requests import UserProfileRequest
from core.app.services.create_profile_photo import create_profile_photo_from_file


@permission_classes([IsAuthenticated])
class UserProfilePhotoHandler(GenericAPIView):
    serializer_class = UserProfileRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        profile_photo = create_profile_photo_from_file(data.validated_data["profile_photo"])
        profile_photo.save(fp="media/user_profile_foto/" + str(request.user) + ".png")
        return Response("Successfully uploaded a new avatar.")
