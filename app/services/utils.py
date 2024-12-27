import os
import base64


def generate_challenge():
    return base64.b64encode(os.urandom(32)).decode()
