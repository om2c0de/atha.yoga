from django.urls import path

from lessons.app.handlers.comment_handlers import (
    CourseCommentListHandler,
    CourseCommentCreateHandler,
    CourseCommentRemoveHandler,
)
from lessons.app.handlers.lesson_handlers import (
    CourseFilterHandler,
    CourseCreateHandler,
    CourseUpdateHandler,
    FavoriteCourseAddHandler,
    FavoriteCourseRemoveHandler,
    FavoriteCourseListHandler,
    CourseTicketBuyHandler,
    CourseTicketUseHandler,
    CourseRetrieveHandler,
)
from lessons.app.handlers.review_handlers import (
    CourseReviewListHandler,
    CourseReviewCreateHandler,
    CourseReviewRemoveHandler,
)

urlpatterns = [
    path("", CourseCreateHandler.as_view(), name="course_create"),
    path("<int:pk>/", CourseRetrieveHandler.as_view(), name="course_retrieve"),
    path("<int:pk>/", CourseUpdateHandler.as_view(), name="course_update"),
    path("filter/", CourseFilterHandler.as_view(), name="courses_filter"),
    path("favorites/", FavoriteCourseListHandler.as_view(), name="favorite_course_list"),
    path(
        "favorites/add/", FavoriteCourseAddHandler.as_view(), name="favorite_course_add"
    ),
    path(
        "favorites/remove/",
        FavoriteCourseRemoveHandler.as_view(),
        name="favorite_course_remove",
    ),
    path("ticket/buy/", CourseTicketBuyHandler.as_view()),
    path("ticket/use/", CourseTicketUseHandler.as_view()),
    path("<int:pk>/comments/", CourseCommentListHandler.as_view(), name="comment_list"),
    path(
        "<int:pk>/comments/create/",
        CourseCommentCreateHandler.as_view(),
        name="comment_create",
    ),
    path(
        "comments/<int:pk>/remove/",
        CourseCommentRemoveHandler.as_view(),
        name="comment_remove",
    ),
    path(
        "<int:pk>/course-reviews/",
        CourseReviewListHandler.as_view(),
        name="course_review_list",
    ),
    path(
        "<int:pk>/course-reviews/create/",
        CourseReviewCreateHandler.as_view(),
        name="course_review_create",
    ),
    path(
        "course-reviews/<int:pk>/remove/",
        CourseReviewRemoveHandler.as_view(),
        name="course_review_remove",
    ),
]
