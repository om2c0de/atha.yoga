import random

from faker import Faker

from core.models import User
from lessons.models import CourseComment, Course


class CourseCommentSeeder:
    def __init__(self) -> None:
        self.faker = Faker("ru-RU")

    def seed(self) -> CourseComment:
        user_ids = User.objects.all().values("id")
        if not user_ids.exists():
            raise Exception("no users in db")
        random_user_id = random.choice(user_ids)["id"]
        course_ids = Course.objects.all().values("id")
        if not course_ids.exists():
            raise Exception("no courses in db")
        random_course_id = random.choice(course_ids)["id"]

        return CourseComment(
            user=User.objects.get(pk=random_user_id),
            text=" ".join(self.faker.words(self.faker.random_int(1, 20))),
            course=Course.objects.get(pk=random_course_id),
        )
