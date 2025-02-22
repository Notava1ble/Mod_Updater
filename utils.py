import logging
import os
from typing import List


def get_current_mod_names(path: str) -> List[str]:
    """Get all the mods names in the specified path.

    :param path: Path to the mods folder.
    :type path: str
    :return: List of mod names.
    :rtype: List[str]
    """
    files = os.listdir(path)

    mods = []

    for file in files:
        if file.endswith(".jar"):
            mods.append(file)

    logging.debug("Current mods: %s", mods)
    return mods


def check_path(path: str) -> None:
    """Check if the specified path exists, if not create it.

    :param path: Path to check.
    :type path: str
    """
    logging.debug("Checking path: %s", path)
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info("Created path: %s", path)
    else:
        logging.debug("Path exists: %s", path)
