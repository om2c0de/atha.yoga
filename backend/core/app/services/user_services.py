from functools import cached_property
from typing import Tuple
import uuid
from django.conf import settings

from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    PermissionDenied,
)

from core.app.repositories.user_repository import UserRepository
from core.app.services.types import (
    UserRegisterData,
    UserLoginData,
    UserChangePassData,
)
from core.app.services.email_services import SimpleEmailTextService
from core.app.utils.jwt import UserToken, get_tokens_for_user
from core.models import User
from core.app.services.types import TextMailData


class UserRegister:
    repository = UserRepository()

    def __init__(self, data: UserRegisterData):
        self.data = data

    @cached_property
    def user(self) -> User:
        user = User()
        if self.repository.find_user_by_email(self.data["email"]):
            raise ValidationError("User with this email already exists")
        user.username = user.email = self.data["email"]
        user.set_password(self.data["password"])
        self.repository.store(user=user)
        return user

    def register(self) -> Tuple[User, UserToken]:
        token_data = get_tokens_for_user(user=self.user)
        return self.user, token_data


class UserLogin:
    repository = UserRepository()

    def __init__(self, data: UserLoginData):
        self.data = data

    @cached_property
    def user(self) -> User:
        user = self.repository.find_user_by_email(self.data["email"])
        if not user or not user.check_password(self.data["password"]):
            raise AuthenticationFailed()
        return user

    def login(self) -> Tuple[User, UserToken]:
        token_data = get_tokens_for_user(self.user)
        return self.user, token_data


class UserChangePass:
    repository = UserRepository()

    def __init__(self, data: UserChangePassData):
        self.data = data

    @cached_property
    def user(self) -> User:
        user = self.repository.find_user_by_email(self.data["email"])
        if not user or not user.check_password(self.data["password"]):
            raise AuthenticationFailed()
        user.set_password(self.data["new_password"])
        self.repository.store(user=user)
        return user

    def change(self) -> Tuple[User, UserToken]:
        token_data = get_tokens_for_user(self.user)
        return self.user, token_data


class UserResetPass:
    repository = UserRepository()

    def reset(self, email: str) -> None:
        user = self.repository.find_user_by_email(email)
        if not user:
            raise PermissionDenied("User with this email does not exist")
        pwd_reset_token = str(uuid.uuid4())
        SimpleEmailTextService(
            data=TextMailData(
                subject="Please reset your password",
                message=f"""Reset your Atha.Yoga password
            Click here: {settings.SITE_PROTOCOL_URL}/?token={pwd_reset_token}/""",
                receivers=[email],
            )
        ).send()
        user.pwd_reset_token = pwd_reset_token
        self.repository.store(user=user)

    def change(
        self, new_password: str, email: str, pwd_reset_token: str
    ) -> Tuple[User, UserToken]:
        user = self.repository.find_user_by_email(email=email)
        if not user:
            raise PermissionDenied("User with this email does not exist")
        if pwd_reset_token != user.pwd_reset_token:
            raise AuthenticationFailed("Tokens don't match")
        user.set_password(new_password)
        self.repository.store(user=user)
        token_data = get_tokens_for_user(user)
        return user, token_data
