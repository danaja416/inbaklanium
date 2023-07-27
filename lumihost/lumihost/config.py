"""
All the things that should be easibly changable
"""

from . import strings

# bot
BOT_TOKENS = {
    "main": "x",
    "test": "6226974960:AAHZFcShxfm3YQ2ALNJiObf9rlkq00QjkmY"
}
BOT_TOKEN = BOT_TOKENS["test"]

# cryptopay
CRYPTOPAY_TOKENS = {
    "mainnet": "111373:AATXUhwOMhTHi0yulJiYr2077IdGdDBIIvu",
    "testnet": "111373:AATXUhwOMhTHi0yulJiYr2077IdGdDBIIvu"
}
CRYPTOPAY_TOKEN = CRYPTOPAY_TOKENS["testnet"]
CRYPTOPAY_TESTNET = CRYPTOPAY_TOKEN == CRYPTOPAY_TOKENS["testnet"]
CRYPTOPAY_EXPIRE = 3600  # crypto bot payments expire time in seconds

# other
IP = "151.115.37.198"
FORBIDDEN_PORTS = [1]
ADMINS = [2]
PRICE = 0  # in RUB
CARD = "x"
USERBOTS = {
    "hikka": strings.HIKKA,
    "netfoll": strings.NETFOLL
}
