from django.conf import settings
from django.core.cache import cache
from datetime import datetime, timedelta
from typing import TypedDict
from functools import wraps

from rest_framework.exceptions import Throttled
import requests
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from collections.abc import Callable

from core.models import UserRoles
from typing import Any, Union
from core.models import User


class SenderInfo(TypedDict):
    count: int
    time: datetime


class ReCaptcha(object):
    captcha_url = "https://www.google.com/recaptcha/api/siteverify"

    def __init__(self, decorated_method_name: str):
        self.decorated_method_name = decorated_method_name

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            self_: Any, request: Request, *args: Any, **kwargs: Any
        ) -> Callable:
            sender = self.sender(request)
            sender_info = self.sender_info(sender)
            time = sender_info["time"] - datetime.now()
            sender_info["count"] += 1
            if sender_info["count"] >= 5:
                captcha = self.check_recaptcha(request)
                if not captcha and time < timedelta(days=1):
                    raise Throttled
                sender_info["count"] = -1
                sender_info["time"] = datetime.now()
            cache.set(f"{sender}", sender_info)
            return func(self_, request, *args, **kwargs)

        return wrapper

    def sender(self, request: Request) -> Union[User, str]:
        if isinstance(request.user, AnonymousUser):
            return self.ip(request)
        return request.user

    def sender_info(self, sender: Union[User, str]) -> SenderInfo:
        info = cache.get(f"{sender}", {})
        return SenderInfo(
            count=info.get("count", 0), time=info.get("time", datetime.now())
        )

    def ip(self, request: Request) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def check_recaptcha(self, request: Request) -> bool:
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": recaptcha_response,
        }
        r = requests.post(self.captcha_url, data=data)
        result = r.json()
        return result["success"]


class IsTeacher(BasePermission):
    """
    Allows access only to users with TEACHER role.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRoles.TEACHER)
        )
