from typing import Optional

from core.app.repositories.base_repository import BaseRepository
from core.models import User


class UserRepository(BaseRepository):
    model = User

    def store(self, user: User) -> None:
        user.save()

    def find_user_by_email(self, email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()
