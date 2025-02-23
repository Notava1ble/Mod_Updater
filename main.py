import logging
from typing import List

from ModrinthClient import ModrinthClient
from logging_config import configure_logger
from parser import parse_args
from utils import (
    check_path,
    check_version,
    get_current_mod_hashes,
    put_current_mods_in_folder,
)

modrinthClient = ModrinthClient()


def main():
    args = parse_args()
    version = check_version(args.version, modrinthClient)
    path = args.path
    loader = args.loader

    logging.info("Started with version: (%s) and path: (%s)", version, path)

    check_path(path)

    mod_hashes: List[str] = get_current_mod_hashes(path)

    put_current_mods_in_folder(path, modrinthClient.get_old_version(mod_hashes))

    modrinthClient.download_mods(mod_hashes, path, version, loader)


if __name__ == "__main__":
    configure_logger(log_file="mod_updater.log", debug=False)
    logging.info("Starting mod updater.")
    main()
    logging.info("Mod updater finished.")
