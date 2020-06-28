from django.core.exceptions import ValidationError

def validator_file_size(fieldfile_obj):  # add this to some file where you can import it from
    max_limit = 4 * 1024 * 1024  # 2Mb
    min_limit = 100  # 100 Bytes
    if fieldfile_obj.size > max_limit:
        raise ValidationError('File too large. Size should not exceed 4 MiB.')
    if fieldfile_obj.size < min_limit:
        raise ValidationError(
            'File too small. Size should be atleast 100 bytes.')
