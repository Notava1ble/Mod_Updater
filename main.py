import requests, json, os, sys, logging
from logging_config import configure_logger
from utils import parse_args


def main():
    args = parse_args()


if __name__ == "__main__":
    configure_logger(log_file="mod_updater.log", debug=True)
    logging.info("Starting mod updater.")
    main()
    logging.info("Mod updater finished.")
