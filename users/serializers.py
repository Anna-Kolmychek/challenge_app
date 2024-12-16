from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser"""

    class Meta:
        model = CustomUser
        fields = (
            'telegram_id',
            'username',
        )
