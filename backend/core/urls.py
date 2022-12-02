from django.urls import path

from core.app.handlers.user_handlers import UserRegisterHandler, UserLoginHandler, UserChangePassHandler
from core.app.handlers.user_profile_handlers import UserProfilePhotoHandler

urlpatterns = [
    path("register/", UserRegisterHandler.as_view(), name="registration"),
    path("login/", UserLoginHandler.as_view(), name="login"),
    path("edit-profile/avatar/", UserProfilePhotoHandler.as_view(), name="avatar"),
    path("changepass/", UserChangePassHandler.as_view(), name="changepass"),
]
