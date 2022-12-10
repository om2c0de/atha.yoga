from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from core.app.http.requests.user_requests import (
    UserRegisterRequest,
    UserLoginRequest,
    UserChangePassRequest,
    UserResetPassRequest,
    UserSendPwdResetMailRequest,
    UserFavoriteAddRemoveRequest,
)
from core.app.http.resources.user_resources import UserResource
from core.app.services.user_services import (
    UserRegister,
    UserLogin,
    UserChangePass,
    UserResetPass,
    UserFavoriteAdd,
    UserFavoriteRemove,
)

from lessons.app.http.resources.lesson_resources import LessonResource


class UserRegisterHandler(GenericAPIView):
    serializer_class = UserRegisterRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        user, token = UserRegister(data=data.validated_data).register()
        return Response(
            {"data": {"user": UserResource(user).data, "tokens": token._asdict()}}
        )


class UserLoginHandler(GenericAPIView):
    serializer_class = UserLoginRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        user, token = UserLogin(data=data.validated_data).login()
        return Response(
            {"data": {"user": UserResource(user).data, "tokens": token._asdict()}}
        )


class UserChangePassHandler(GenericAPIView):
    serializer_class = UserChangePassRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        user, token = UserChangePass(data=data.validated_data).change()
        return Response(
            {"data": {"user": UserResource(user).data, "tokens": token._asdict()}}
        )


class UserSendPwdResetMailHandler(GenericAPIView):
    serializer_class = UserSendPwdResetMailRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        UserResetPass().reset(email=data.validated_data["email"])
        return Response("Success")


class UserResetPassHandler(GenericAPIView):
    serializer_class = UserResetPassRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        user, token = UserResetPass().change(
            new_password=data.validated_data["new_password"],
            email=data.validated_data["email"],
            pwd_reset_token=data.validated_data["pwd_reset_token"],
        )
        return Response(
            {"data": {"user": UserResource(user).data, "tokens": token._asdict()}}
        )


@permission_classes([IsAuthenticated])
class UserFavoriteAddHandler(GenericAPIView):
    serializer_class = UserFavoriteAddRemoveRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        lesson = UserFavoriteAdd(
            user=self.request.user, lesson_id=data.validated_data["lesson_id"]
        ).add()
        return Response({"lesson": LessonResource(lesson).data})


@permission_classes([IsAuthenticated])
class UserFavoriteRemoveHandler(GenericAPIView):
    serializer_class = UserFavoriteAddRemoveRequest

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        lesson = UserFavoriteRemove(
            user=self.request.user, lesson_id=data.validated_data["lesson_id"]
        ).remove()
        return Response({"lesson": LessonResource(lesson).data})


@permission_classes([IsAuthenticated])
class UserFavoriteListHandler(GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        lessons = self.request.user.favorite_lessons.all()
        return Response({"lessons": LessonResource(lessons, many=True).data})
