from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.app.utils.serializers import UnimplementedSerializer
from lessons.models import (
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


class ScheduleCreateRequest(UnimplementedSerializer):
    weekday = serializers.ChoiceField(choices=RepetitionWeekdays.choices)
    start_time = serializers.TimeField()


class CourseCreateRequest(UnimplementedSerializer):
    name = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=150, allow_blank=True)
    course_type = serializers.ChoiceField(choices=CourseTypes.choices)
    complexity = serializers.ChoiceField(choices=CourseComplexities.choices)
    link = serializers.URLField()
    link_info = serializers.CharField(max_length=100, allow_blank=True)
    level = serializers.ChoiceField(choices=CourseLevels.choices)
    duration = serializers.DurationField()
    repeat_editing = serializers.BooleanField(default=False)
    start_datetime = serializers.DateTimeField()
    deadline_datetime = serializers.DateTimeField(allow_null=True)
    payment = serializers.ChoiceField(choices=CoursePaymentTypes.choices)
    price = serializers.IntegerField(min_value=0)
    schedule = ScheduleCreateRequest(many=True, allow_null=True)


class CourseUpdateRequest(UnimplementedSerializer):
    description = serializers.CharField(max_length=150, allow_blank=True)
    complexity = serializers.ChoiceField(choices=CourseComplexities.choices)
    level = serializers.ChoiceField(choices=CourseLevels.choices)
    duration = serializers.DurationField()


class FavoriteCourseAddRemoveRequest(UnimplementedSerializer):
    course_id = serializers.IntegerField(min_value=1)


class CourseTicketBuyRequest(UnimplementedSerializer):
    course_id = serializers.IntegerField(min_value=1)
    amount = serializers.IntegerField(min_value=1)


class CourseTicketUseRequest(UnimplementedSerializer):
    schedule_id = serializers.IntegerField(min_value=1)
