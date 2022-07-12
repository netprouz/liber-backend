import random
import string


def generate_random_string():
    _str = "".join(random.choice(string.ascii_uppercase) for _ in range(4))
    _int = "".join(random.choice(string.digits) for _ in range(4))

    return f"{_str}-{_int}"
