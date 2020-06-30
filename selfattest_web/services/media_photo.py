
import logging
import uuid
from typing import List,  Any

from io import BytesIO
from PIL import Image, UnidentifiedImageError

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


from media_photo.api.serializers import UserPhotoSerializer
from media_photo.models import UserPhotoMeta, TempPhoto


logger = logging.getLogger(__name__)

MAX_WIDTH = 720


def _get_file_from_request_data(image_data) -> Any:

    # We need to get a file object for Pillow. We might have a path or we might
    # have to read the data into memory.
    if hasattr(image_data, 'temporary_file_path'):
        file = image_data.temporary_file_path()
    else:
        if hasattr(image_data, 'read'):
            file = BytesIO(image_data.read())
        else:
            file = BytesIO(image_data['content'])
    try:
        # load() could spot a truncated JPEG, but it loads the entire
        # image in memory, which is a DoS vector. See #3848 and #18520.
        origial_image = Image.open(file)
        # verify() must be called immediately after the constructor.
        image = origial_image.copy()
        image.verify()
    except UnidentifiedImageError as e:
        raise ValidationError('Not an image')
    return origial_image


def _remove_white_pixel(img):
    pixdata = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    return img


def _black_and_white_dithering(color_image, output_image_path=None, dithering=False):
    # color_image = Image.open(color_doc)
    if dithering:
        bw = color_image.convert('1')
    else:
        bw = color_image.convert('1', dither=Image.NONE)
    bw = bw.convert("RGBA")
    return bw


def _svc_media_upload_user_photo(file_data: Any) -> dict:
    logger.debug(">>")
    buffer = BytesIO()
    file_data.save(fp=buffer, format='PNG')  # we always save as PNG
    file_name = str(uuid.uuid4())+".png"

    temp_photo = TempPhoto()
    image_field = temp_photo.photo
    image_field.save(file_name, InMemoryUploadedFile(
        ContentFile(buffer.getvalue()),       # file
        None,               # field_name
        file_name,           # file name
        'image/png',       # content_type
        file_data.tell,  # size
        None))

    temp_photo.save()

    user_photo_meta = UserPhotoMeta.create(photo_url=temp_photo.photo.url)
    temp_photo.delete()  # delete temp instance used to upload and retrieve file url
    return UserPhotoSerializer(user_photo_meta, many=False).data


def svc_get_attested_files_url(request_data: dict) -> dict:
    '''
    1. Verify that all required parameters exist
    2. Get both files
    3. Scale down document if required
    4. Make sure signature is smaller than document (else paste fails)
    5. bw and remove white pixels
    6. paste.
    7. 

    '''
    required_keys: List[str] = ['document', 'signature']
    for required_key in required_keys:
        if required_key not in request_data:
            raise KeyError(f'parameter missing - {required_key}')
        if not request_data[required_key]:
            raise KeyError(f'Invalid {required_key}')

    document = _get_file_from_request_data(request_data['document'])
    signature = _get_file_from_request_data(request_data['signature'])

    # scale down to max 720*720 (Keeps aspect)
    document.thumbnail((MAX_WIDTH, MAX_WIDTH))

    signature_size_constraint = min(document.size)

    # Image needs to be smaller than document
    signature.thumbnail((signature_size_constraint, signature_size_constraint))

    # Photo copy both
    signature = _black_and_white_dithering(signature)
    # document = black_and_white_dithering(document)

    # make signature transparent
    signature = _remove_white_pixel(signature)

    # get pasting pos.
    # TODO: Can do better with boxing here
    position = ((document.width - signature.width),
                (document.height - signature.height))
    document.paste(signature, position, signature)
    return _svc_media_upload_user_photo(document)
