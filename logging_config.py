import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors based on log level."""

    COLORS = {
        logging.DEBUG: "\033[90m",  # Gray
        logging.INFO: "\033[94m",  # Blue
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[1;91m",  # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"


def configure_logger(log_file: str = "Mod_updater.log", debug: bool = False):
    """
    Configures and returns a logger.

    :param log_file: File to write logs to.
    :type log_file: str
    :param debug: Controls whether to show debug messages in console.
    :type debug: bool
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Ensure all levels are captured

    # File handler
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler for INFO and below (stdout)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    stdout_formatter = ColoredFormatter("%(levelname)s - %(message)s")
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    logger.addHandler(stdout_handler)

    # Console handler for ERROR and above (stderr)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_formatter = ColoredFormatter("%(levelname)s - %(message)s")
    stderr_handler.setFormatter(stderr_formatter)
    logger.addHandler(stderr_handler)
