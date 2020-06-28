from rest_framework import serializers
from ..models import UserPhotoMeta


class UserPhotoSerializer(serializers.ModelSerializer):
    photo_id = serializers.SerializerMethodField()

    class Meta:
        model = UserPhotoMeta
        fields = (
            'photo_id',
            'photo_url',
        )

    def get_photo_id(self, obj):
        return str(obj.get_external_id())
