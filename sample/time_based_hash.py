import hmac
import time
import base64
import struct
import hashlib

from django.conf import settings


def get_hoth(secret, counter):
    """Return the HMAC-Based One-Time Password for the the given secret (base32 encoded) and the counter.
    """

    secret = base64.b32decode(secret)
    counter = struct.pack('>Q', counter)

    _hash = hmac.new(secret, counter, hashlib.sha1).digest()
    offset = _hash[19] & 0xF

    return (struct.unpack(">I", _hash[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000


def get_toth(service_name: str) -> str:
    """
    :param service_name:
    :return:
    """
    just_pay_key = base64.b32encode((settings.SERVICE_KEY_ONE + settings.SECRET_KEY).encode())
    top_up_service = base64.b32encode((settings.SERVICE_KEY_TWO + settings.SECRET_KEY).encode())

    secret_key = {"ServiceOne": just_pay_key, "ServiceTwo": top_up_service}
    secret = secret_key[service_name]

    tot = get_hoth(secret, int(time.time()) // 30)

    return hashlib.sha256('{}'.format(tot).encode() + settings.SERVICE_SECRET_KEY.encode()).hexdigest()
