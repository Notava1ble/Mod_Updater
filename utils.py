import hashlib
import logging
import os
import sys
from typing import TYPE_CHECKING, Dict


from ModrinthClient import ModrinthClient


def get_current_mod_hashes(path: str) -> Dict[str, str]:
    """Get all the mods names in the specified path.

    :param path: Path to the mods folder.
    :type path: str
    :return: Dictionary with the mods names and their hashes.
    :rtype: Dict[str: str]
    """
    files = os.listdir(path)

    mods = {}

    for file in files:
        if file.endswith(".jar"):
            sha1 = hashlib.sha1()  # You can use hashlib.md5() for MD5
            with open(os.path.join(path, file), "rb") as f:
                while chunk := f.read(8192):
                    sha1.update(chunk)
            hash = sha1.hexdigest()
            mods[file] = hash

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


def put_current_mods_in_folder(path: str, old_version: str) -> None:
    """Move the current mods to the old version folder inside the specified path.

    :param path: Path to the mods folder.
    :type str: path
    :param old_version: The old version of the mods.
    :type old_version: str
    """
    old_path = os.path.join(path, old_version)
    check_path(old_path)

    files = os.listdir(path)

    for file in files:
        if file.endswith(".jar"):
            os.rename(os.path.join(path, file), os.path.join(old_path, file))
            logging.debug("Moved mod: %s to: %s verion folder", file, old_version)
    logging.info("Moved current mods to %s version folder.", old_version)
