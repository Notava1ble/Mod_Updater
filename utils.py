import logging
import os
import sys
from typing import List

from ModrinthClient import ModrinthClient
from models.models import Mod


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


def check_version(version: str, modrinthClient: ModrinthClient) -> str:
    """If the version is "latest" get the latest version from Modrinth. Else return the version if it exists or sys.exit().

    :param version: The version to check.
    :type version: str
    :param modrinthClient: The ModrinthClient object.
    :type modrinthClient: ModrinthClient
    :return: The version
    :rtype: str
    """
    if version == "latest":
        logging.debug("Getting latest version.")
        return modrinthClient.latest_release_version()
    else:
        if modrinthClient.validate_version(version):
            logging.debug("Version (%s) is valid.", version)
            return version
        logging.error("Version (%s) is not valid.", version)
        return sys.exit(1)
