from rest_framework import serializers

from tg_bot.models import InitData


class InitDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitData
        fields = '__all__'