import hmac
import time
import base64
import struct
import hashlib


def get_hoth(secret, counter):
    """Return the HMAC-Based One-Time Password for the the given secret (base32 encoded) and the counter.
    [755224, 287082, 359152, 969429, 338314, 254676, 287922, 162583, 399871, 520489]
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

    just_pay_key = base64.b32encode('JustPay0123456789'.encode())
    top_up_service = base64.b32encode('TOPUP0123456789'.encode())

    making_strong = b'132123sfdfjsdlfsdfn45412^^&%%%$$$'

    secret_key = {"JustPay": just_pay_key, "TopUp": top_up_service}
    secret = secret_key[service_name]
    print(get_hoth(secret, int(time.time()) // 30))

    tot = get_hoth(secret, int(time.time()) // 30)

    return hashlib.sha256('{}'.format(tot).encode() + making_strong).hexdigest()
