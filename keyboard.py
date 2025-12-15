from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from logger import log_exceptions


# --- Клавиатура для администратора --- #
class KeyboardAdmin:
    def __init__(self, config):
        self.config = config["admin"]

    # password keyboard admin
    @log_exceptions(name="keyboard_password", logfile="keyboard_utils.log", error_message="Ошибка при создании клавиатуры паролей")
    async def keyboard_password(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.config["password"]["update"]),
                    KeyboardButton(text=self.config["password"]["view"])
                ]
            ],
            resize_keyboard=True
        )

    # users keyboard admin
    @log_exceptions(name="keyboard_users", logfile="keyboard_utils.log", error_message="Ошибка при создании клавиатуры пользователей")
    async def keyboard_users(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.config["users"]["list"]),
                    # если появится вторая кнопка для блока "users", добавь её сюда
                ]
            ],
            resize_keyboard=True
        )

    # services keyboard admin
    @log_exceptions(name="keyboard_service", logfile="keyboard_utils.log", error_message="Ошибка при создании клавиатуры услуг")
    async def keyboard_service(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.config["service"]["list"]),
                    KeyboardButton(text=self.config["service"]["rate_list"])
                ],
                [
                    KeyboardButton(text=self.config["service"]["change_service"]),
                    KeyboardButton(text=self.config["service"]["change_rate"])
                ]
            ],
            resize_keyboard=True
        )

    # main keyboard admin
    @log_exceptions(name="keyboard_admin_main", logfile="keyboard_utils.log", error_message="Ошибка при создании главной клавиатуры админа")
    async def keyboard_admin_main(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.config["users"]["list"]),
                    KeyboardButton(text=self.config["service"]["list"])
                ],
                [
                    KeyboardButton(text=self.config["service"]["rate_list"]),
                    KeyboardButton(text=self.config["service"]["change_service"])
                ],
                [
                    KeyboardButton(text=self.config["password"]["view"]),
                    KeyboardButton(text=self.config["password"]["update"]),
                ],
                [
                    KeyboardButton(text=self.config["service"]["change_rate"]),
                ],
            ],
            resize_keyboard=True
        )


# --- Клавиатура для пользователя --- #
class KeyboardUser:
    def __init__(self, config):
        self.config = config["user"]

    @log_exceptions(name="keyboard_menu", logfile="keyboard_utils.log", error_message="Ошибка при создании меню пользователя")
    async def keyboard_menu(self) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(
            KeyboardButton(self.config["menu"]["faq"]),
            KeyboardButton(self.config["menu"]["help"]),
            KeyboardButton(self.config["menu"]["my_services"])
        )
        return kb

    @log_exceptions(name="keyboard_invitee", logfile="keyboard_utils.log", error_message="Ошибка при создании клавиатуры приглашений")
    async def keyboard_invitee(self) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(
            KeyboardButton(self.config["invitee"]["invite"]),
            KeyboardButton(self.config["invitee"]["list"]),
            KeyboardButton(self.config["invitee"]["delete"])
        )
        return kb

    @log_exceptions(name="keyboard_user_main", logfile="keyboard_utils.log", error_message="Ошибка при создании главной клавиатуры пользователя")
    async def keyboard_user_main(self) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        kb.add(
            KeyboardButton(self.config["menu"]["faq"]),
            KeyboardButton(self.config["menu"]["help"]),
            KeyboardButton(self.config["menu"]["my_services"]),
            KeyboardButton(self.config["invitee"]["invite"]),
            KeyboardButton(self.config["invitee"]["list"]),
            KeyboardButton(self.config["invitee"]["delete"])
        )
        return kb
