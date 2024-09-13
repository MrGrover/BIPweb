
from rest_framework.permissions import BasePermission
from otp_app.models import UserModel, get_user_id


class IsAuthenticatedAndVerified(BasePermission):

    #    Кастомное разрешение, проверяющее, что пользователь аутентифицирован и прошел вторую аутентификацию
    def has_permission(self, request, view):
        '''# Получаем user_id из данных запроса
        #user_id = request.data.get('user_id')
        session_id = request.COOKIES.get('sessionid')
        if not session_id:
            return False
        # Находим сессию по session_id
        session = Session.objects.get(session_key=session_id)
        # Проверяем, не истекла ли сессия
        if session.expire_date < timezone.now():
            return False
        # Получаем данные сессии
        session_data = session.get_decoded()
        # Извлекаем user_id из данных сессии
        '''
        user_id = get_user_id(request)
        if not user_id:
            print('false')
            return False  # Если user_id не передан, отклоняем доступ


        try:
            # Ищем пользователя по переданному user_id
            user = UserModel.objects.get(id=user_id)
            print(user.is_active)
            print(user.otp_validated)
            print(user.email)
            print(user.is_authenticated)
        except UserModel.DoesNotExist:
            return False  # Если пользователь не найден, отклоняем доступ


        return bool(user.is_active and user.otp_validated and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print('1')
        return True
