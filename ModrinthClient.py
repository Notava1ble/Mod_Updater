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

    def search(self, query: str) -> dict:
        """search for mods on Modrinth

        :param query: search query
        :type query: str
        :return: search results
        :rtype: dict
        """
        return self.get(
            f"/search?limit=20&index=relevance&query={query}&facets=%5B%5B%22project_type%3Amod%22%5D%5D"
        )["hits"]

    def create_mod_list(self, current_mods: List[str]) -> List[Mod]:
        """Create a list of Mod Dicts from the current mods, searching in Modrinth.

        :param current_mods: List of current mods in the folder.
        :type current_mods: List[str]
        :return: List of Mod Dicts.
        :rtype: List[Mod]
        """
        mods_list: List[Mod] = []

        for mod in current_mods:
            logging.debug("Searching for: %s", mod)
            search = self.search(mod)
            if not search:
                logging.error("No mods found with search: %s", mod)
                continue
            mod_slug = search[0]["slug"]
            mod = self.get(f"/project/{mod_slug}")

            mod_dict = {
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

        return mods_list
