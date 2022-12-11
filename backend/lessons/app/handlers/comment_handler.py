from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.app.http.requests.comment_requests import (
    CommentCreateRequest,
    CommentListRequest,
)
from lessons.app.http.resources.comment_resources import CommentResource
from lessons.app.repositories.comment_repository import CommentRepository
from lessons.app.services.comment_service import CommentCreate


@permission_classes([IsAuthenticated])
class CommentCreateHandler(GenericAPIView):
    serializer_class = CommentCreateRequest

    def post(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        comment = CommentCreate(
            data=data.validated_data, user=self.request.user
        ).create()
        return Response({"comment": CommentResource(comment).data})


class CommentListHandler(GenericAPIView):
    serializer_class = CommentListRequest

    def get(self, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=self.request.data)
        data.is_valid(raise_exception=True)

        comments = CommentRepository().find_by_lesson_id(
            lesson_id=data.validated_data["lesson_id"]
        )
        return Response({"comments": CommentResource(comments, many=True).data})
