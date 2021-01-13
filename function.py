import os
from urllib import request

def check_resorce(url, expected_code):
    response = request.urlopen(url)
    if response.status != expected_code:
        raise Exception(response.status)

