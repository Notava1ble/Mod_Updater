import logging
import sys


def configure_logger(log_file: str = "Mod_updater.log", debug: bool = False):
    """
    Configures and returns a logger with console and optional file logging.

    :param name: Name of the logger (default: "app").
    :type name: str
    :param log_file: Optional file to write logs to.
    :type log_file: str
    :param level: Logging level (default: logging.INFO).
    :type level: int
    """
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)

    logger.addHandler(console_handler)
    logger.setLevel(level=logging.DEBUG)
    logger.addHandler(file_handler)
