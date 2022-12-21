import random
import time
from datetime import timedelta

import pytz
from django.utils.timezone import now
from faker import Faker

from core.models import User
from lessons.models import Course, CourseTypes, CourseLevels, CoursePaymentTypes
from lessons.models import CourseComplexities


class CourseSeeder:
    def __init__(self, user: User) -> None:
        self.faker = Faker("ru-RU")
        self.user = user

    def seed(self) -> Course:
        random.seed(time.time())
        start_datetime = self.faker.date_time(tzinfo=pytz.UTC)
        return Course(
            name=" ".join(self.faker.words(self.faker.random_int(1, 5))),
            start_datetime=start_datetime,
            description=self.faker.sentence(),
            course_type=random.choice([i[0] for i in CourseTypes.choices]),
            complexity=random.choice([i[0] for i in CourseComplexities.choices]),
            level=random.choice([i[0] for i in CourseLevels.choices]),
            single=random.choice([False, True]),
            duration=timedelta(minutes=random.randint(60, 300)),
            price=random.randint(1000, 100000),
            teacher=self.user,
            deadline_datetime=self.faker.date_time_between(
                start_datetime, now() + timedelta(days=30), tzinfo=pytz.UTC
            ),
            link=self.faker.url(),
            link_info=self.faker.sentence()[:100],
            repeat_editing=False,
            payment=random.choice([i[0] for i in CoursePaymentTypes.choices]),
        )
