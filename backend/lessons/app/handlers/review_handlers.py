from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lessons.app.http.requests.review_requests import CourseReviewCreateRequest
from lessons.app.http.resources.review_resources import CourseReviewResource
from lessons.app.repositories.review_repository import CourseReviewRepository
from lessons.app.services.review_service import CourseReviewCreate, CourseReviewRemove


class CourseReviewListHandler(APIView):
    def get(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        reviews = CourseReviewRepository().find_by_course_id(course_id=pk)
        return Response({"reviews": CourseReviewResource(reviews, many=True).data})


@permission_classes([IsAuthenticated])
class CourseReviewCreateHandler(GenericAPIView):
    serializer_class = CourseReviewCreateRequest

    def post(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        review = CourseReviewCreate(
            course_id=pk, data=data.validated_data, user=request.user
        ).create()
        return Response({"review": CourseReviewResource(review).data})


@permission_classes([IsAuthenticated])
class CourseReviewRemoveHandler(APIView):
    def delete(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        review = CourseReviewRemove(review_id=pk, user=request.user).remove()
        return Response({"review": CourseReviewResource(review).data})
