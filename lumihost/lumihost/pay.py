"""
Payment related things
"""

from . import db, config, strings
from random import randint
from crypto_pay_api_sdk import cryptopay


class CryptoPay:
    def __init__(self):
        self.crypto_db = db.crypto_db
        self.cp = cryptopay.Crypto(config.CRYPTOPAY_TOKEN, testnet=config.CRYPTOPAY_TESTNET)

    def get_price(self, rub, round_to=5):
        """Converts Rubles in TONs"""
        rate = next(item for item in self.cp.getExchangeRates()["result"] if (item["source"] == "TON") and (item["target"] == "RUB"))
        return round(rub / float(rate["rate"]), round_to)

    def create_payment(self, user_id, payment_id=None):
        """Creates a payment"""
        if payment_id is None:
            payment_id = str(randint(10000, 99999))

        self.crypto_db.create_payment(payment_id, user_id)

        return self.cp.createInvoice(
            "TON", str(self.get_price(config.PRICE)),
            params={
                "description": strings.CRYPTOPAY_DESCRIPTION,
                "expires_in": config.CRYPTOPAY_EXPIRE,
                "paid_btn_name": "openBot",
                "paid_btn_url": f"https://t.me/x?start=pay-{payment_id}",
                "allow_anonymous": False
            }
        )["result"]

    def find_payment(self, payment_id):
        """Find a payment which specified id"""
        return self.crypto_db.cur.execute(
            """SELECT * FROM cryptopays WHERE id = ?""",
            (payment_id,)
        ).fetchone()
