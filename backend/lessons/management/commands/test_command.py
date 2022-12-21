from typing import Any

from django.core.management import BaseCommand

from core.seeders.user_seeder import UserSeeder
from lessons.seeders.lesson_seeder import CourseSeeder


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        user = UserSeeder().seed()
        user.save()

        CourseSeeder(user=user).seed().save()
