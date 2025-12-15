import psycopg2

from config import database_config
from logger import logger_config


# Connect to database postgresql
async def connect_to_database():
    logger = await logger_config(name="connect_to_database", log_file="database.log")

    try:

        connect = psycopg2.connect(
            user=database_config["user"],
            password=database_config["password"],
            host=database_config["host"],
            port=database_config["port"],
            database=database_config["database"],
        )
        cursor = connect.cursor()
        return connect, cursor

    except Exception as ex:
        logger.error(ex)
        return None, None


# Create table's for database
async def create_table():
    logger = await logger_config(name="create_table", log_file="database.log")

    try:

        connect, cursor = await connect_to_database()

        # Table for save hash-password
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS role_passwords (
            id SERIAL PRIMARY KEY,
            role_id INT UNIQUE NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Table for save default-user role
        cursor.execute("""CREATE TABLE IF NOT EXISTS roles (
            Id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        # Table for save telegram users
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            Id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            role_id INT NOT NULL DEFAULT 3 REFERENCES roles(id),
            status BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )

        # Table for save service
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS service (
            Id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            description TEXT,
            price BIGINT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )

        # Table for save link user -> service
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS user_service (
            Id SERIAL PRIMARY KEY,
            inviter_id BIGINT NOT NULL REFERENCES users(id) on DELETE CASCADE,
            invitee_id BIGINT NOT NULL REFERENCES users(id) on DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )

        # Table for save reminders by admin
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS reminders (
            Id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            schedule TIMESTAMP NOT NULL,
            user_id BIGINT REFERENCES users(id) on DELETE CASCADE,
            service_id BIGINT REFERENCES service(id) on DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )

        # SQL function for automatic updating of the update_at string
        cursor.execute(
            """
        CREATE OR REPLACE FUNCTION update_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
        )

        for table in ["users", "service", "user_service", "reminders"]:
            cursor.execute(
                f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger WHERE tgname = 'set_timestamp_{table}'
                    ) THEN
                        CREATE TRIGGER set_timestamp_{table}
                        BEFORE UPDATE ON {table}
                        FOR EACH ROW
                        EXECUTE FUNCTION update_timestamp();
                    END IF;
                END $$;
                """
            )

            # Create roles for telegram-bot
            cursor.execute("INSERT INTO roles (name, description) VALUES ('admin', 'Full access') ON CONFLICT DO NOTHING;")
            cursor.execute("INSERT INTO roles (name, description) VALUES ('moderator', 'Limited modertion rights') ON CONFLICT DO NOTHING;")
            cursor.execute("INSERT INTO roles (name, description) VALUES ('user', 'Default role for all new users') ON CONFLICT DO NOTHING;")

    except Exception as ex:
        logger.error(ex)
    finally:
        connect.commit()
        cursor.close()
        connect.close()
