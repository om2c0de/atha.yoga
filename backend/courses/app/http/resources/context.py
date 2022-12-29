from typing import TypedDict

from core.models import User


class BaseCourseResourceContext(TypedDict):
    user: User
