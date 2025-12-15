from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot_utils import check_user_for_admin
from config_message import command_msg
from database_utils import check_role_password, update_role_to_admin, user_registration
from logger import log_exceptions
from register_config import keyboard_admin

route = Router()


# Start TGBot and register user
@route.message(Command("start"))
async def command_start(message: Message):
    await user_registration(message.from_user.id)
    await message.answer(command_msg["start_msg"])


# Insert admin password
@route.message(Command("admin"))
@log_exceptions(name="command_admin", logfile="bot_route.log", error_message="Ошибка при вводе пароля!")
async def command_admin(message: Message):

    kb_admin = await keyboard_admin.keyboard_admin_main()

    # --- Сначала проверяем роль пользователя ---
    if await check_user_for_admin(message.from_user.id):
        await message.answer(
            f"{message.from_user.username}, добро пожаловать в административную панель!",
            reply_markup=kb_admin
        )
        return

    # --- Если не админ, тогда проверяем пароль ---
    message_args = message.text.split(maxsplit=1)
    if len(message_args) < 2:
        await message.answer("Вы неверно указали пароль! Используйте: /admin <PASSWORD>")
        return

    password = message_args[1]
    if await check_role_password("admin", password):
        await message.answer("Пароль введен верно!")

        if await update_role_to_admin(message.from_user.id):
            await message.answer("Ваша роль успешно обновлена до администратора")
            await message.answer(
                f"{message.from_user.username}, добро пожаловать в административную панель!",
                reply_markup=kb_admin
            )
        else:
            await message.answer("При обновлении вашей роли произошла ошибка!")
    else:
        await message.answer("Пароль введен не верно!")
