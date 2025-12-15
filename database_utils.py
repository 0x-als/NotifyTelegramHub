import bcrypt

from database import connect_to_database
from logger import log_exceptions, logger_config


# User registration
async def user_registration(telegram_id):
    logger = await logger_config(name='user_registration', log_file="database_utils.log")

    try:
        connect, cursor = await connect_to_database()

        cursor.execute("INSERT INTO users (telegram_id) VALUES (%s) ON CONFLICT (telegram_id) DO NOTHING;", (telegram_id,))

    except Exception as ex:
        logger.error(ex)
    finally:
        connect.commit()
        cursor.close()
        connect.close()


# Create default password for role
async def init_role_passwords():
    logger = await logger_config(name='init_role_passwords', log_file="database_utils.log")

    try:

        connect, cursor = await connect_to_database()

        base_passwords = {
            "admin": "admin123",
            "moderator": "moderator123"
        }

        for role, plain_password in base_passwords.items():
            hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute("""
                INSERT INTO role_passwords (role_id, password_hash)
                VALUES ((SELECT id FROM roles WHERE name = %s), %s)
                ON CONFLICT (role_id) DO UPDATE
                SET password_hash = EXCLUDED.password_hash,
                    updated_at = CURRENT_TIMESTAMP;
            """, (role, hashed))

    except Exception as ex:
        logger.error(ex)
    finally:
        connect.commit()
        cursor.close()
        connect.close()


# Check role password
async def check_role_password(role_name: str, plain_password: str) -> bool:
    logger = await logger_config(name='check_role_password', log_file="database_utils.log")
    try:

        connect, cursor = await connect_to_database()

        cursor.execute("""
            SELECT password_hash 
            FROM role_passwords 
            WHERE role_id = (SELECT id FROM roles WHERE name = %s)
        """, (role_name,))
        row = cursor.fetchone()
        if row:
            stored_hash = row[0]
            return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))
        return False
    except Exception as ex:
        logger.error(ex)
    finally:
        connect.commit()
        cursor.close()
        connect.close()


# Updating the role for the user with the correct password
async def update_role_to_admin(telegram_id):
    logger = await logger_config(name='update_role_to_admin', log_file="database_utils.log")

    try:
        connect, cursor = await connect_to_database()

        cursor.execute("UPDATE users SET role_id = (SELECT id FROM roles WHERE name = 'admin') WHERE telegram_id = %s", (telegram_id,))
        return True
    except Exception as ex:
        logger.error(ex)
        return False
    finally:
        connect.commit()
        cursor.close()
        connect.close()


# get user role by telegram id
@log_exceptions(name='get_user_role_by_telegram_id', logfile="database_utils.log")
async def get_user_role_by_telegram_id(telegram_id):

    connect, cursor = await connect_to_database()
    cursor.execute("SELECT role_id FROM users WHERE telegram_id = %s", (telegram_id,))
    row_user = cursor.fetchone()
    if row_user:
        role_id = row_user[0]
        cursor.execute("SELECT name FROM roles WHERE id = %s", (role_id,))
        row_role = cursor.fetchone()
        if row_role:
            role_name = row_role[0]

            return role_id, role_name
    else:
        return None