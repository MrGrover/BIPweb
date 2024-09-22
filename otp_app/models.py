import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils import timezone
from django.contrib.sessions.models import Session

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

BLOOD_TYPE_CHOICES = [
    ('I', 'First'),
    ('II', 'second'),
    ('III', 'third'),
    ('IV', 'fourth')
]


def get_user_id(request):
    # Получаем user_id из данных запроса
    # user_id = request.data.get('user_id')
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
    user_id = session_data.get('_auth_user_id')
    return user_id


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, default=False)
    second_name = models.CharField(max_length=50, default=False)
    last_name = models.CharField(max_length=50, default=False)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=False)
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES, default=False)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=32)
    otp_validated = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    username = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
