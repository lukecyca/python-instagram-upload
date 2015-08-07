import requests
import hmac
import random
import uuid
import urllib
import json
import hashlib
import time

try:
    # python 2
    urllib_quote_plus = urllib.quote
except:
    # python 3
    urllib_quote_plus = urllib.parse.quote_plus

def _generate_signature(data):
    return hmac.new('b4a23f5e39b5929e0666ac5de94c89d1618a2916'.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()


def _generate_user_agent():
    resolutions = ['720x1280', '320x480', '480x800', '1024x768', '1280x720', '768x1024', '480x320']
    versions = ['GT-N7000', 'SM-N9000', 'GT-I9220', 'GT-I9100']
    dpis = ['120', '160', '320', '240']

    ver = random.choice(versions)
    dpi = random.choice(dpis)
    res = random.choice(resolutions)

    return (
        'Instagram 4.{}.{} '
        'Android ({}/{}.{}.{}; {}; {}; samsung; {}; {}; smdkc210; en_US)'
    ).format(
        random.randint(1, 2),
        random.randint(0, 2),
        random.randint(10, 11),
        random.randint(1, 3),
        random.randint(3, 5),
        random.randint(0, 5),
        dpi,
        res,
        ver,
        ver,
    )


class InstagramSession(object):

    def __init__(self):
        self.guid = str(uuid.uuid1())
        self.device_id = 'android-{}'.format(self.guid)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': _generate_user_agent()})

    def login(self, username, password):

        data = json.dumps({
            "device_id": self.device_id,
            "guid": self.guid,
            "username": username,
            "password": password,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
        print(data)

        sig = _generate_signature(data)

        payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            sig,
            urllib_quote_plus(data)
        )

        r = self.session.post("https://instagram.com/api/v1/accounts/login/", payload)
        r_json = r.json()
        print(r_json)

        if r_json.get('status') != "ok":
            return False

        return True

    def upload_photo(self, filename):
        data = {
            "device_timestamp": time.time(),
        }
        files = {
            "photo": open(filename, 'rb'),
        }

        r = self.session.post("https://instagram.com/api/v1/media/upload/", data, files=files)
        r_json = r.json()
        print(r_json)

        return r_json.get('media_id')

    def configure_photo(self, media_id, caption):
        data = json.dumps({
            "device_id": self.device_id,
            "guid": self.guid,
            "media_id": media_id,
            "caption": caption,
            "device_timestamp": time.time(),
            "source_type": "5",
            "filter_type": "0",
            "extra": "{}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
        print(data)

        sig = _generate_signature(data)

        payload = 'signed_body={}.{}&ig_sig_key_version=4'.format(
            sig,
            urllib_quote_plus(data)
        )

        r = self.session.post("https://instagram.com/api/v1/media/configure/", payload)
        r_json = r.json()
        print(r_json)

        if r_json.get('status') != "ok":
            return False

        return True


