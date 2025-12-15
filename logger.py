import functools
import logging
import os
from logging.handlers import RotatingFileHandler


# --- Запись логов ---
async def logger_config(
    name: str,
    log_file: str,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """
    Настраивает и возвращает логгер с ротацией файлов и выводом в консоль.

    :param name: Имя логгера.
    :param log_file: Имя файла, в который будут записываться логи.
    :param level: Уровень логирования (по умолчанию logging.INFO).
    :param max_bytes: Максимальный размер файла лога перед ротацией (по умолчанию 10 МБ).
    :param backup_count: Количество архивных файлов (по умолчанию 5).
    :return: Настроенный логгер.

    Пример использования:
    """
    # Создаем каталог для логов, если его нет
    log_folder = os.path.join("files", "logs")
    os.makedirs(log_folder, exist_ok=True)

    # Полный путь к файлу логов
    log_file_path = os.path.join(log_folder, log_file)

    # Формат логирования
    log_format = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d in %(funcName)s] - %(message)s"
    formatter = logging.Formatter(log_format)

    # Настройка обработчика с ротацией файлов
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
        delay=True,  # Важно для избежания блокировки файлов на Windows
    )
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Получаем или создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем существующие обработчики во избежание дублирования
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Добавляем наши обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Отключаем распространение логов к родительским логгерам
    logger.propagate = False

    return logger

# Create logger decorator
def log_exceptions(name: str, logfile: str, error_message: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = await logger_config(name=name, log_file=logfile)
            try:
                return await func(*args, **kwargs)
            except Exception as ex:
                logger.exception(ex)
                if args and hasattr(args[0], "answer"):
                    await args[0].answer(error_message)
        return wrapper
    return decorator