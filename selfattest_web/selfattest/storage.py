from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage




class PublicMediaStorage(S3Boto3Storage):
    #Changing this at later point also leads to problem
    location = 'selfattested'
    default_acl = 'public-read'
    file_overwrite = False
    bucket_name = settings.MEDIA_BUCKET_NAME
