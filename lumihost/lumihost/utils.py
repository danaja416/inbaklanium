"""
Common used functions, also known as utilities
"""

import random
from . import config


def generate_port():
    port = random.randint(1000, 9999)
    if port in config.FORBIDDEN_PORTS:
        return generate_port()
    return port

