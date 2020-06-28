'''
Base behaviours. Didn't name this mixins, as what's in a name?
'''


from django.db import models
from django.conf import settings
from common.uuid import unique_uuid4
from common.constants import Length

from django.contrib.postgres.fields import JSONField



class AbstractExternalFacing(models.Model):
    '''
    Used by classes to implement uuid as unique field. This is helpful for -
    1. Use external_id as external facing IDs shared with clients. Great as we will not leak information about models
     that would have happened with auto increment interger PK
    2. As FKs when we want to decouple apps into Microservices in future
    '''
    external_id = models.UUIDField(default=unique_uuid4, unique=True)

    class Meta:
        abstract = True

    def get_external_id(self):
        return self.external_id


class AbstractTimeStamped(models.Model):
    '''
    Provides created and updated time fields
    '''
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True



class AbstractVersioned(models.Model):
    '''
    Implented by models that require versioning.
    Provides is_deleted and version number fields
    '''
    is_deleted = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True


