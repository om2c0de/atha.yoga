from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.app.utils.pagination import paginate
from lessons.app.http.requests.lesson_requests import (
    LessonFilterRequest,
    LessonCreateRequest, LessonTicketUseRequest, LessonTicketBuyRequest,
)
from lessons.app.http.resources.lesson_resources import LessonResource, TicketResource
from lessons.app.repositories.lesson_repository import LessonRepository, TicketRepository
from lessons.app.services.lesson_service import LessonCreator, TicketCreator
from lessons.seeders.lesson_seeder import LessonSeeder


class LessonsFilterHandler(GenericAPIView):
    serializer_class = LessonFilterRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data, partial=True)
        data.is_valid(raise_exception=True)

        lessons = LessonRepository().filter(data=data.validated_data)

        return Response(
            paginate(data=lessons, request=self.request, resource=LessonResource)
        )


@permission_classes([IsAuthenticated])  # TODO Add IsTeacher permission
class LessonCreateHandler(GenericAPIView):
    serializer_class = LessonCreateRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        lesson = LessonCreator(
            data=data.validated_data, user=self.request.user
        ).create()

        return Response({"data": LessonResource(lesson).data})


@permission_classes([IsAuthenticated])
class LessonTicketBuyHandler(GenericAPIView):
    serializer_class = LessonTicketBuyRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        ticket = TicketCreator(
            data=data.validated_data, user=self.request.user
        ).create()

        return Response({"data": TicketResource(ticket).data})


@permission_classes([IsAuthenticated])
class LessonTicketUseHandler(GenericAPIView):
    serializer_class = LessonTicketUseRequest

    def put(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        ticket = TicketRepository().find_amount_of_ticket(name=data.validated_data["name"])

        x = LessonSeeder(user=self.request.user).seed()
        x.save()

        if not ticket:
            raise PermissionDenied("dont have ticket for this lesson")
        if int(ticket.amount) > 0:
            ticket.amount = int(ticket.amount) - 1
            ticket.save()
        else:
            raise PermissionDenied("dont have ticket for this lesson")

        return Response({"data": TicketResource(ticket).data["name"]})
