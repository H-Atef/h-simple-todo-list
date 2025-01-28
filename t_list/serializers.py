from rest_framework.serializers import ModelSerializer
from . import models

class TODOListSerializer(ModelSerializer):
    class Meta:
        model=models.TODOListModel
        fields="__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['hashtags'] = list(instance.hashtags.values_list('name', flat=True))

        return representation