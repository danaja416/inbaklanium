"""
Inline Keyboards
"""

from . import strings
from aiogram.types import InlineKeyboardMarkup as Keyboard, InlineKeyboardButton as Button


class Keyboards:
    @property
    def menu(self):
        """/start"""
        keyboard = Keyboard()
        keyboard.add(Button(strings.BUY_BUTTON, callback_data="buy_menu"))
        keyboard.add(
            Button(strings.CONTROL_BUTTON, callback_data="control_menu"),
            Button(strings.INSTALL_BUTTON, callback_data="install_menu"),
        )
        keyboard.add(Button(strings.HELP_BUTTON, url="https://t.me/x"))
        return keyboard

    @property
    def back(self):
        """Only the "Back" button"""
        keyboard = Keyboard()
        keyboard.add(Button(strings.BACK_BUTTON, callback_data="menu"))
        return keyboard

    @property
    def buy(self):
        """Choosing the payment method, or back in the menu"""
        keyboard = Keyboard()
        keyboard.add(
            Button(strings.DEPOSIT_CRYPTOBOT_BUTTON, callback_data="deposit_cryptobot"),
            Button(strings.DEPOSIT_CARD_BUTTON, callback_data="deposit_card"),
        )
        keyboard.add(Button(strings.BACK_BUTTON, callback_data="menu"))
        return keyboard

    @property
    def back_buy(self):
        """Back to buy menu"""
        keyboard = Keyboard()
        keyboard.add(Button(strings.BACK_BUTTON, callback_data="buy_menu"))
        return keyboard

    @property
    def install_userbot(self):
        """Choosing a userbot, user will click an inline button in the format of: `install_hikka`"""
        keyboard = Keyboard()
        keyboard.add(
            Button(strings.HIKKA, callback_data="install_hikka"),
            Button(strings.NETFOLL, callback_data="install_netfoll"),
            # Button(strings.FTG, callback_data="install_ftg"),
            # Button(strings.GEEKTG, callback_data="install_geektg"),
            # Button(strings.BLACKFOOT, callback_data="install_blackfoot")
        )
        return keyboard

    @property
    def install_link(self):
        """Done (actually a "Back" button) and Help buttons"""
        keyboard = Keyboard()
        keyboard.add(
            Button(strings.DONE_BUTTON, callback_data="back"),
            Button(strings.HELP_BUTTON, url="https://t.me/x")
        )
        return keyboard

    @property
    def no_userbot(self):
        """Shows when you enter a control panel without an userbot installed"""
        keyboard = Keyboard()
        keyboard.add(
            Button(strings.INSTALL_BUTTON, callback_data="install_menu"),
            Button(strings.BACK_BUTTON, callback_data="back"),
        )
        return keyboard

    @property
    def control_panel(self):
        """Basic controls of user's userbot"""
        keyboard = Keyboard()
        keyboard.add(
            Button(strings.START_BUTTON, callback_data="start_userbot"),
            Button(strings.STOP_BUTTON, callback_data="stop_userbot"),
            Button(strings.RESTART_BUTTON, callback_data="restart_userbot")
        )
        keyboard.add(
            Button(strings.LOGS_BUTTON, callback_data="logs_userbot"),
            Button(strings.BACK_BUTTON, callback_data="back")
        )
        return keyboard

    def deposit_cryptobot(self, payment):
        """A single button with payment url"""
        keyboard = Keyboard()
        keyboard.add(Button(strings.DEPOSIT_BUTTON, url=payment["pay_url"]))
        return keyboard
