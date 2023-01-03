from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from core.app.utils.request import APIRequest
from core.models import UserRoles


class IsTeacher(BasePermission):
    """
    Allows access only to users with TEACHER role.
    """

    def has_permission(self, request: APIRequest, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRoles.TEACHER)
        )
