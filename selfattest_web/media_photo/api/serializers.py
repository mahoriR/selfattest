from rest_framework import serializers
from ..models import UserPhotoMeta


class UserPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPhotoMeta
        fields = (
            'photo_url',
        )
