import string
from random import randint


def generate_verification_code():
    return int(randint(1000, 9999))

print(generate_verification_code())