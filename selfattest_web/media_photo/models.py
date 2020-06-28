import uuid
from django.db import models


from common.abstract_models import AbstractExternalFacing, AbstractTimeStamped

from .validators import validator_file_size

import logging

logger = logging.getLogger(__name__)


class UserPhotoMeta(AbstractExternalFacing, AbstractTimeStamped):
    photo_url = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.photo_url

    class Meta:
        indexes = [
            models.Index(fields=['external_id']),
        ]

    @classmethod
    def create(cls, *, photo_url: str) -> 'UserPhotoMeta':
        photo_meta = cls(photo_url=photo_url,
                         )
        photo_meta.save()
        return photo_meta


class TempPhoto(models.Model):
    '''
    Why we have a temp photo?
    The .file.url changes on update to underlying Storage class params.

    So we are going to save files to another model and delete temporary storage.
    '''
    photo = models.ImageField()
    #photo = models.ImageField(storage=PublicMediaStorage())

    def __str__(self):
        return self.photo.url
