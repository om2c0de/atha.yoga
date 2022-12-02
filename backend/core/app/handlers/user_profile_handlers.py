from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from core.app.http.requests.profile_requests import UserProfileRequest
from core.app.services.create_profile_photo import create_profile_photo_from_file


class UserProfilePhotoHandler(GenericAPIView):
    serialzer_class = UserProfileRequest

    @permission_classes([IsAuthenticated])
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        image = request.FILES['profile_photo']
        profile_photo = create_profile_photo_from_file(image)
        profile_photo.save(fp="media/user_profile_foto/" + str(request.user) + ".png")
        return Response("Successfully uploaded a new avatar.")
