from rest_framework import serializers
from otp_app.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', "first_name", "second_name", "last_name", 'age', 'gender', 'blood_type',
                  'email', 'password', 'otp_verified', 'otp_mode',
                  'otp_base32', 'otp_auth_url']
        #fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Если пользователь не администратор
        user = self.Meta.model(**validated_data)
        print(validated_data)
        if not user.is_superuser:  # Проверка: является ли пользователь администратором
            if 'id' in validated_data:
                raise serializers.ValidationError({"username": "Изменение id пользователя запрещено."})
            if 'otp_verified' in validated_data or 'otp_validated' in validated_data\
                    or 'otp_base32' in validated_data or 'otp_auth_url' in validated_data:
                raise serializers.ValidationError({"email": "Изменение otp полей запрещено."})

        # Обновляем остальные поля
        return super().update(instance, validated_data)
