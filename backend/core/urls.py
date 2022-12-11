from django.urls import path
from core.app.handlers.user_handlers import (
    UserRegisterHandler,
    UserLoginHandler,
    UserChangePassHandler,
    UserSendPwdResetMailHandler,
    UserResetPassHandler,
)

urlpatterns = [
    path("register/", UserRegisterHandler.as_view(), name="registration"),
    path("login/", UserLoginHandler.as_view(), name="login"),
    path("changepass/", UserChangePassHandler.as_view(), name="changepass"),
    path("resetpass/", UserSendPwdResetMailHandler.as_view(), name="resetpass"),
    path("resetpass/confirm/", UserResetPassHandler.as_view(), name="resetpass_change"),
]
