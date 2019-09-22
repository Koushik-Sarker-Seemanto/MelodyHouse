from string import ascii_uppercase, digits
import random as _rand
def random_string(prefix='', size=12):
	return prefix.join(_rand.choices(ascii_uppercase+digits, k=size))


from django.conf import settings
from jwt import decode as __decode
from jwt import encode as __encode
from jwt.exceptions import InvalidTokenError

from time import time


def decode(token):
	try:
		data = __decode(token, settings.SECRET_KEY, algorithms=['HS256'])
		return data
	except InvalidTokenError as e:
		return None


def encode(data, time_stamp=None):
	if time_stamp:
		data['time_stamp'] = int(time())
	token = __encode(data, settings.SECRET_KEY, algorithm='HS256')
	return token.decode()