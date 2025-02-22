import requests, json, os, sys, logging
from ModrinthClient import ModrinthClient
from logging_config import configure_logger
from parser import parse_args
from utils import check_path, get_current_mod_names

modrinthClient = ModrinthClient()


def main():
    args = parse_args()
    vesrion = (
        args.version
        if args.version != "latest"
        else modrinthClient.latest_release_version()
    )
    path = args.path

    logging.info("Started with version: (%s) and path: (%s)", vesrion, path)

    check_path(path)

    current_mods = get_current_mod_names(path)


if __name__ == "__main__":
    configure_logger(log_file="mod_updater.log", debug=False)
    logging.info("Starting mod updater.")
    main()
    logging.info("Mod updater finished.")
