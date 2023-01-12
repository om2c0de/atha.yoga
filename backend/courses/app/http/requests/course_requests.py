import datetime

from django.conf import settings
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.app.utils.serializers import UnimplementedSerializer
from courses.models import (
    CourseComplexities,
    CourseTypes,
    CourseLevels,
    CoursePaymentTypes,
    RepetitionWeekdays,
)


class CourseFilterRequest(UnimplementedSerializer):
    query = serializers.CharField(max_length=100)
    complexity = serializers.ChoiceField(choices=CourseComplexities.choices)
    start_datetime = serializers.DateTimeField()
    day = serializers.IntegerField(min_value=1, max_value=7)
    end_datetime = serializers.DateTimeField()

    def validate(self, attrs: dict) -> dict:
        if "end_datetime" in attrs and "start_datetime" in attrs:
            if attrs["end_datetime"] < attrs["start_datetime"]:
                raise ValidationError("start_datetime must be less than end_datetime")
        return attrs


class LessonCreateRequest(UnimplementedSerializer):
    weekday = serializers.ChoiceField(choices=RepetitionWeekdays.choices)
    start_time = serializers.TimeField()


class BaseCourseUpdateRequest(UnimplementedSerializer):
    description = serializers.CharField(max_length=150)
    complexity = serializers.ChoiceField(choices=CourseComplexities.choices)
    level = serializers.MultipleChoiceField(choices=CourseLevels.choices)


class CourseCreateRequest(UnimplementedSerializer):
    name = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=150)
    complexity = serializers.ChoiceField(choices=CourseComplexities.choices)
    level = serializers.MultipleChoiceField(choices=CourseLevels.choices)
    duration = serializers.DurationField(min_value=datetime.timedelta(minutes=1))
    course_type = serializers.ChoiceField(choices=CourseTypes.choices)
    link = serializers.URLField()
    link_info = serializers.CharField(max_length=100, allow_blank=True)
    start_datetime = serializers.DateTimeField()
    deadline_datetime = serializers.DateTimeField(allow_null=True)
    payment = serializers.ChoiceField(choices=CoursePaymentTypes.choices)
    price = serializers.IntegerField(min_value=0)
    lessons = LessonCreateRequest(many=True, allow_null=True)
    is_draft = serializers.BooleanField(default=False)

    def validate(self, attrs: dict) -> dict:
        if (
            attrs.get("payment", None) == CoursePaymentTypes.PAYMENT
            and attrs.get("price", 0) <= 0
        ):
            raise ValidationError({"price": "Price must be more then 0"})
        if attrs["start_datetime"] <= now():
            raise ValidationError(
                {"start_date": f"start_datetime attribute must be greater then {now()}"}
            )
        if attrs.get("deadline_datetime"):
            if attrs["start_datetime"] >= attrs["deadline_datetime"]:
                raise ValidationError(
                    {
                        "start_date": "start_datetime attribute must be less then deadline_datetime"
                    }
                )
            if (
                attrs["start_datetime"] + settings.COURSE_LESSONS_CYCLE
                <= attrs["deadline_datetime"]
            ):
                raise ValidationError(
                    {
                        "start_date": f"Max course lessons cycle = {settings.COURSE_LESSONS_CYCLE}"
                    }
                )
        return attrs


class FavoriteCourseAddRemoveRequest(UnimplementedSerializer):
    course_id = serializers.IntegerField(min_value=1)


class CourseTicketBuyRequest(UnimplementedSerializer):
    course_id = serializers.IntegerField(min_value=1)
    amount = serializers.IntegerField(min_value=1)


class CourseTicketUseRequest(UnimplementedSerializer):
    lesson_id = serializers.IntegerField(min_value=1)
