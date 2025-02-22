import hashlib
import json
import logging
from typing import List
import requests

from models.models import GameVersion, Mod


class ModrinthClient:
    def __init__(self):
        self.base_url = "https://api.modrinth.com/v2"
        self.game_versions: List[GameVersion] = self.get("/tag/game_version")

    def get(self, url: str) -> list | dict | None:
        """get data from the specified url extention of https://api.modrinth.com/v2

        :param url: url extention
        :type url: str
        :return: data from the url
        :rtype: list | dict | None
        """
        try:
            response = requests.get(self.base_url + url)
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None

    def latest_release_version(self) -> str:
        """get the latest release version of the game

        :return: latest version of Minecraft
        :rtype: str
        """
        for version in self.game_versions:
            if version["version_type"] == "release":
                logging.debug("Latest version: %s", version["version"])
                return version["version"]

    def validate_version(self, version: str) -> bool:
        """Validates the version of the game, and sys.exit() if it does not exist

        :param version: version of the game
        :type version: str
        :return: version of the game
        :rtype: bool
        """
        for game_version in self.game_versions:
            if game_version["version"] == version:
                return True

        return False

    def get_mod_from_hash(self, file_hash: str) -> dict:
        """Gets the mod from the hash of the file

        :param query: hash of the file
        :type query: str
        :return: information about the mod
        :rtype: dict
        """
        response = requests.post(
            f"{self.base_url}/version_files",
            json={"hashes": [file_hash], "algorithm": "sha1"},
        )

        if response.status_code == 200:
            data = response.json()
            return data  # Contains information about the mod
        else:
            logging.error("Error: %s %s", response.status_code, response.text)
            return None

    def create_mod_list(self, current_mod_hashes: List[str]) -> List[Mod]:
        """Create a list of Mod Dicts from the current mods, using the hash of the files.

        :param current_mods: List of current mods in the folder.
        :type current_mods: List[str]
        :return: List of Mod Dicts.
        :rtype: List[Mod]
        """
        logging.info("Finding mods...")
        mods_list: List[Mod] = []
        version: str = ""

        for hash in current_mod_hashes:
            logging.debug("Getting mod from hash: %s", hash)
            mod = self.get_mod_from_hash(hash)
            if not mod:
                continue

            old_version = mod[hash]["game_versions"][-1]
            mod_id = mod[hash]["project_id"]
            mod = self.get(f"/project/{mod_id}")

            mod_dict: Mod = {
                "id": mod["id"],
                "slug": mod["slug"],
                "title": mod["title"],
                "description": mod["description"],
                "loaders": mod["loaders"],
                "versions": mod["versions"],
                "game_versions": mod["game_versions"],
            }
            mods_list.append(mod_dict)
            logging.info("Found: %s", mod["title"])

        logging.info("Found %s mods.", len(mods_list))
        return mods_list, old_version

    def download_mods(self, mod_list: List[Mod], path: str, version: str) -> None:
        """Download the mods from the list of mods.

        :param mod_list: List of mods to download.
        :type mod_list: List[Mod]
        :param path: Path to download the mods.
        :type str: str
        :param version: Version of the game.
        :type version: str
        """
        pass
