from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from core.app.http.requests.profile_requests import UserProfileRequest
from core.app.services.profile_services import ProfilePhotoCreator


@permission_classes([IsAuthenticated])
class UserProfilePhotoHandler(GenericAPIView):
    serializer_class = UserProfileRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        ProfilePhotoCreator(user=request.user, data=data)

        return Response("Successfully uploaded a new avatar.")
