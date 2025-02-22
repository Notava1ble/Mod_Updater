import json
import logging
import os
from typing import Dict, List
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

    def download_mod(
        self, url: str, path: str, filename: str
    ) -> bool | requests.Response:
        """Download the mod from the url

        :param url: url of the mod
        :type url: str
        :param path: path to download the mod
        :type path: str
        :param filename: name of the file to save
        :type filename: str
        :return: True if the mod was downloaded successfully
        :rtype: bool
        """
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(os.path.join(path, filename), "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return True, "placeholder"
        else:
            return False, response

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

    def get_mod_version(self, mod_id: str) -> dict:
        """Get the version of the mod

        :param mod_id: id of the mod
        :type mod_id: str
        :return: version of the mod
        :rtype: dict
        """
        return self.get(f"/project/{mod_id}/version")

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

    def create_mod_list(self, current_mod_hashes: Dict[str, str]) -> List[Mod]:
        """Create a list of Mod Dicts from the current mods, using the hash of the files.

        :param current_mods: A dictionary of the current mods hashes with the file name as the key.
        :type current_mods: Dict[str, str]
        :return: List of Mod Dicts.
        :rtype: List[Mod]
        """
        logging.info("Finding mods...")
        mods_list: List[Mod] = []
        old_version: str = ""

        for index, (filename, hash) in enumerate(current_mod_hashes.items()):
            logging.debug("Getting mod from hash: %s", hash)
            mod = self.get_mod_from_hash(hash)
            if not mod:
                logging.error("Mod not found: %s", filename)
                continue
            if not old_version:
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

    def get_latest_version(self, mod: Mod, version: str, loader: str) -> str:
        """Get the latest version of the mod compatible with the specified version and loader.

        :param mod_id: The mod dict.
        :type mod_id: Mod
        :param version: The version of the game.
        :type version: str
        :param loader: The mod loader.
        :type loader: str
        :return: The latest version of the mod.
        :rtype: str
        """
        mod_id = mod["id"]
        mod_name = mod["title"]

        mod_versions_data = self.get_mod_version(mod_id)

        filtered_mod_versions_data = [
            mod_version
            for mod_version in mod_versions_data
            if version in mod_version["game_versions"]
            and loader in mod_version["loaders"]
        ]

        if not filtered_mod_versions_data:
            logging.error(
                f"No version found for {mod_name} with MC_VERSION={version} and LOADER={loader}"
            )
            return None

        return filtered_mod_versions_data[0]["files"][0]

    def download_mods(
        self, mod_list: List[Mod], path: str, version: str, loader: str
    ) -> None:
        """Download the mods from the list of mods.

        :param mod_list: List of mods to download.
        :type mod_list: List[Mod]
        :param path: Path to download the mods.
        :type str: str
        :param version: Version of the game.
        :type version: str
        :param loader: The mod loader.
        :type loader: str
        """
        logging.info("Downloading mods...")
        for mod in mod_list:
            latest_version_file = self.get_latest_version(mod, version, loader)
            if not latest_version_file:
                continue
            response = self.download_mod(
                latest_version_file["url"], path, latest_version_file["filename"]
            )
            if response[0]:
                logging.info("Downloaded: %s", mod["title"])

            else:
                logging.error(
                    "Error downloading mod %s: %s %s",
                    mod["title"],
                    response.status_code,
                    response.text,
                )

        logging.info("Downloaded %s mods.", len(mod_list))
