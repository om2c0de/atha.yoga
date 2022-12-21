from rest_framework.serializers import ModelSerializer

from lessons.models import Course, Lesson


class LessonResource(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "start_at",
        ]


class CourseResource(ModelSerializer):
    lesson = LessonResource(many=True)

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
            "lesson",
        ]
