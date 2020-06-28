import uuid

from typing import Tuple
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser, FormParser




from .serializers import UserPhotoMeta, UserPhotoSerializer
from ..models import TempPhoto

from services.media_photo import svc_get_attested_files_url

import logging

logger = logging.getLogger(__name__)


class UserPhotoListView(generics.GenericAPIView):
    '''
        POST - Upload document and signature and returns URL for attested document
    '''

    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        logger.debug(">>")
        try:
            return Response(svc_get_attested_files_url(request.data), status=status.HTTP_200_OK)
        except (ValueError, ValidationError, KeyError) as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
