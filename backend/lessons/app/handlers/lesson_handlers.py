from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.app.utils.pagination import paginate
from core.app.utils.permissions import IsTeacher
from lessons.app.http.requests.lesson_requests import (
    CourseFilterRequest,
    CourseCreateRequest,
    CourseUpdateRequest,
    FavoriteCourseAddRemoveRequest,
    CourseTicketBuyRequest,
    CourseTicketUseRequest,
)
from lessons.app.http.resources.lesson_resources import CourseResource
from lessons.app.repositories.lesson_repository import CourseRepository
from lessons.app.services.lesson_service import (
    CourseCreator,
    FavoriteCoursesWork,
    TicketWorkService,
)
from lessons.app.services.lesson_service import (
    courseUpdator,
    CourseParticipateService,
)


class CourseFilterHandler(GenericAPIView):
    serializer_class = CourseFilterRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data, partial=True)
        data.is_valid(raise_exception=True)

        courses = CourseRepository().filter(data=data.validated_data)

        return Response(
            paginate(data=courses, request=self.request, resource=CourseResource)
        )


class CourseRetrieveHandler(APIView):
    repository = CourseRepository()

    def get(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        course = self.repository.find_by_id(id_=pk)
        if not course:
            raise NotFound(f"Undefined course with pk {pk}")
        return Response({"data": CourseResource(course).data})


@permission_classes([IsTeacher])
class CourseCreateHandler(GenericAPIView):
    serializer_class = CourseCreateRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        course = CourseCreator(
            data=data.validated_data, user=self.request.user
        ).create()

        return Response({"data": CourseResource(course).data})


@permission_classes([IsTeacher])
class CourseUpdateHandler(GenericAPIView):
    serializer_class = CourseUpdateRequest

    def patch(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data, partial=True)
        data.is_valid(raise_exception=True)

        course = courseUpdator(
            user=request.user, data=data.validated_data, pk=pk
        ).update()

        return Response({"data": CourseResource(course).data})


@permission_classes([IsAuthenticated])
class FavoriteCourseAddHandler(GenericAPIView):
    serializer_class = FavoriteCourseAddRemoveRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        course = FavoriteCoursesWork(
            user=self.request.user, course_id=data.validated_data["course_id"]
        ).add()

        return Response({"data": CourseResource(course).data})


@permission_classes([IsAuthenticated])
class FavoriteCourseRemoveHandler(GenericAPIView):
    serializer_class = FavoriteCourseAddRemoveRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        course = FavoriteCoursesWork(
            user=self.request.user, course_id=data.validated_data["course_id"]
        ).remove()

        return Response({"data": CourseResource(course).data})


@permission_classes([IsAuthenticated])
class FavoriteCourseListHandler(APIView):
    def get(self, *args: Any, **kwargs: Any) -> Response:
        courses = CourseRepository().find_user_favorite_courses(user=self.request.user)
        return Response({"data": CourseResource(courses, many=True).data})


@permission_classes([IsAuthenticated])
class CourseTicketBuyHandler(GenericAPIView):
    serializer_class = CourseTicketBuyRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        TicketWorkService().buy(
            course_id=data.validated_data["course_id"],
            user=self.request.user,
            amount=data.validated_data["amount"],
        )

        return Response("Ticket obtained")


@permission_classes([IsAuthenticated])
class CourseTicketUseHandler(GenericAPIView):
    serializer_class = CourseTicketUseRequest

    def put(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        link = CourseParticipateService(
            lesson_id=data.validated_data["lesson_id"], user=self.request.user
        ).participate()

        return Response({"data": {"course_link": link}})
