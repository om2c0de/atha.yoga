from rest_framework.serializers import ModelSerializer

from lessons.models import Course, Schedule


class ScheduleResource(ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "id",
            "course",
            "start_at",
        ]


class CourseResource(ModelSerializer):
    schedules = ScheduleResource(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "course_type",
            "level",
            "single",
            "duration",
            "start_datetime",
            "deadline_datetime",
            "complexity",
            "teacher",
            "repeat_editing",
            "payment",
            "price",
            "schedules",
        ]
