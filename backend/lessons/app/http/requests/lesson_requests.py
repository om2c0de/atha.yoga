from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.app.utils.serializers import UnimplementedSerializer
from lessons.models import (
    LessonComplexities,
    LessonTypes,
    LessonLevels,
    LessonPaymentTypes,
    RepetitionWeekdays,
)


class LessonFilterRequest(UnimplementedSerializer):
    query = serializers.CharField(max_length=100)
    complexity = serializers.ChoiceField(choices=LessonComplexities.choices)
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


class LessonCreateRequest(UnimplementedSerializer):
    name = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=150, allow_blank=True)
    lesson_type = serializers.ChoiceField(choices=LessonTypes.choices)
    complexity = serializers.ChoiceField(choices=LessonComplexities.choices)
    link = serializers.URLField()
    link_info = serializers.CharField(max_length=100, allow_blank=True)
    level = serializers.ChoiceField(choices=LessonLevels.choices)
    duration = serializers.DurationField()
    repeat_editing = serializers.BooleanField(default=False)
    start_datetime = serializers.DateTimeField()
    deadline_date = serializers.DateField(allow_null=True)
    payment = serializers.ChoiceField(choices=LessonPaymentTypes.choices)
    price = serializers.IntegerField(min_value=0)
    schedule = ScheduleCreateRequest(many=True, allow_null=True)


class FavoriteLessonAddRemoveRequest(UnimplementedSerializer):
    lesson_id = serializers.IntegerField(min_value=1)
