from rest_framework.permissions import BasePermission
from otp_app.models import UserModel

class IsAuthenticatedAndVerified(BasePermission):
    """
    Кастомное разрешение, проверяющее, что пользователь аутентифицирован и дополнительное поле (например, is_verified) равно True.
    """
    def has_permission(self, request, view):
        # Получаем user_id из данных запроса
        user_id = request.data.get('user_id')

        if not user_id:
            return False  # Если user_id не передан, отклоняем доступ

        try:
            # Ищем пользователя по переданному user_id
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return False  # Если пользователь не найден, отклоняем доступ

        print(user.is_active)
        print(user.otp_validated)
        print(user.email)
        print(user.is_authenticated)
        return bool(user.is_active and user.otp_validated and request.user.is_authenticated)