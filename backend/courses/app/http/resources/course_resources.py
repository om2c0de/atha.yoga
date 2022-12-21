from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class LessonResource(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "start_at",
        ]


class CourseResource(ModelSerializer):
    lessons = LessonResource(many=True)

    def to_representation(self, instance: Course) -> dict:
        result = super().to_representation(instance=instance)
        teacher = result["teacher"]
        current_user = self.context.get("user")
        if current_user == teacher:
            result["link"] = instance.link
            result["link_info"] = instance.link_info
        return result

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
            "lessons",
        ]
