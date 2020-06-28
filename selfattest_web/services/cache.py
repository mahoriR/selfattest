import logging
from typing import Optional, Union
import uuid

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


logger = logging.getLogger(__name__)


# example
# def get_address(address_id:uuid.UUID)
#   cache_key = f"address.{address_id}"
#   if cache_key in cache:
#       return cache.get(cache_key)
#   address = serialized(get_address_from_db(address_id))
#   set_to_cache(cache_key, address)
#   return address
#
# def set_address(address_id:uuid.UUID, address:dict)
#   cache_key = f"address.{address_id}"
#   invalidate_cache(cache_key)
#   address = serialized(get_address_from_db(address_id))
#   set_to_cache(cache_key, address)
#   return address


def invalidate_cache(cache_key):
    cache.delete(cache_key)


def set_to_cache(cache_key, cache_val):
    cache.set(cache_key, cache_val, timeout=CACHE_TTL)
