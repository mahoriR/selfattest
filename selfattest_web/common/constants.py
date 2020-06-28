import enum
import uuid
from typing import List, Tuple


class Length:
    '''
    Changing constants may require DB migrations. Think before changing.
    '''
    UUID_LEN = 36

    EMAIL = 64


class BaseIntEnum(enum.IntEnum):
    @classmethod
    def tokentype_from_string(cls, token_type: str) -> 'BaseIntEnum':
        '''
        Override if call caps standard names won't work

        throws: KeyError for invalid token_type
        '''
        return cls.__members__[token_type]

    @classmethod
    def get_string_for_type(cls, token_type: 'BaseIntEnum') -> str:
        '''
        Override if call caps standard names won't work
        '''
        return token_type.name

    @classmethod
    def get_choices(cls) -> List[Tuple]:
        '''
        To be used as choices field in model definition
        '''
        return [(member.value, member.name) for member in cls]


class ContentType(BaseIntEnum):
    '''
    Changing constants may require DB migrations. Think before changing.
    '''
    PHOTO = 1
    VIDEO = 2
