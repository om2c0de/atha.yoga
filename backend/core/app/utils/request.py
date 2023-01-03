from typing import Union

from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request

from core.models import User


class APIRequest(Request):
    user: Union[User, AnonymousUser]
