from database_utils import get_user_role_by_telegram_id
from logger import log_exceptions

# checking the user for the admin
@log_exceptions(name="checking_user_for_admin", logfile="bot_utils.log")
async def check_user_for_admin(telegram_id):
    role_id, role_name = await get_user_role_by_telegram_id(telegram_id)

    if role_id == 1 and role_name == "admin":
        return True
    else:
        return False