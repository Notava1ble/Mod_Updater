import logging

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

    logging.info("Started with version: (%s) and path: (%s)", version, path)

    check_path(path)

    current_mod_hashes = get_current_mod_hashes(path)
    mod_list, old_version = modrinthClient.create_mod_list(current_mod_hashes)
    put_current_mods_in_folder(path, old_version)
    modrinthClient.download_mods(mod_list, path, version, "fabric")


if __name__ == "__main__":
    configure_logger(log_file="mod_updater.log", debug=False)
    logging.info("Starting mod updater.")
    main()
    logging.info("Mod updater finished.")
