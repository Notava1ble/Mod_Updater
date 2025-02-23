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
            with open(f"{os.path.join(path, filename)}.jar", "wb") as file:
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

    def get_old_version(self, mods_hashes: List[str]) -> str:
        """Get the old version of the mods.

        :param mods_hashes: The current mods hashes.
        :type mods_hashes: List[str]
        :return: The old version of the mods.
        :rtype: str
        """
        logging.info("Getting old version...")
        old_version = ""
        for hash in mods_hashes:
            mod: Mod = self.get_mod_from_hash(hash)
            if not mod:
                continue
            if not old_version:
                old_version = mod[hash]["game_versions"][-1]
                break

        logging.info("Old version: %s", old_version)
        return old_version

    def download_mods(
        self, mod_hashes: List[str], path: str, version: str, loader: str
    ) -> None:
        """Download the mods from the list of mods.

        :param mod_list: List of mod_hashes.
        :type mod_list: List[str]
        :param path: Path to download the mods.
        :type str: str
        :param version: Version of the game.
        :type version: str
        :param loader: The mod loader.
        :type loader: str
        """
        logging.info("Downloading mods...")
        count = 0

        latest_versions: dict = requests.post(
            "https://api.modrinth.com/v2/version_files/update",
            json={
                "hashes": mod_hashes,
                "algorithm": "sha1",
                "loaders": [loader],
                "game_versions": [version],
            },
        ).json()

        for hash, ver in latest_versions.items():
            name = ver["files"][0]["filename"]
            resp = self.download_mod(ver["files"][0]["url"], path=path, filename=name)
            if resp[0]:
                count += 1
                logging.info("%s Downloaded: %s", count, name)
            else:
                logging.error("Failed to downlaod: %s", name)

        logging.info("Downloaded %s mods.", count)
