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
        """Get data from the specified url extention of https://api.modrinth.com/v2

        :param url: url extention
        :type url: str
        :return: data from the url
        :rtype: list | dict | None
        """
        try:
            response = requests.get(self.base_url + url)
            if response.status_code == 404:
                return None
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None

    def download_mod(
        self, url: str, path: str, filename: str
    ) -> bool | requests.Response:
        """Download the mod using the url

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

    def get_old_version(self, mods_hashes: List[str]) -> str:
        """Gets the version of the current mods

        :param mods_hashes: The current mods hashes.
        :type mods_hashes: List[str]
        :return: The old version of the mods.
        :rtype: str
        """
        logging.info("Getting old version...")
        old_version = ""
        for hash in mods_hashes:
            mod: Mod = self.get(f"/version_file/{hash}")
            if not mod:
                continue
            if not old_version:
                old_version = mod["game_versions"][-1]
                break

        logging.info("Old version: %s", old_version)
        return old_version

    def download_mods(
        self, mod_hashes: Dict[str, str], path: str, version: str, loader: str
    ) -> None:
        """Download the mods using the dictionary of mod hashes.

        :param mod_list: Dictionary of mod_hashes as keys and filenames as values.
        :type mod_list: Dict[str, str]
        :param path: Path to download the mods.
        :type str: str
        :param version: Version of the game.
        :type version: str
        :param loader: The mod loader.
        :type loader: str
        """
        logging.info("Downloading mods...")
        count = 0
        mod_hashes_list = [*mod_hashes]

        latest_versions: dict = requests.post(
            "https://api.modrinth.com/v2/version_files/update",
            json={
                "hashes": mod_hashes_list,
                "algorithm": "sha1",
                "loaders": [loader],
                "game_versions": [version],
            },
        ).json()

        for hash, filename in mod_hashes.items():
            if hash not in latest_versions.keys():
                logging.error(
                    "Mod (%s) does not exist in modrinth servers. You probably haven't downloaded it from Modrinth or the mod doesnt support version %s for %s.",
                    filename,
                    version,
                    loader,
                )
                continue
            ver = latest_versions[hash]
            mod: Mod = self.get(f"/project/{ver["project_id"]}")
            filename = ver["files"][0]["filename"]

            if mod:
                title = mod["title"]
            else:
                title = filename

            logging.info("Downloading: %s", title)
            resp = self.download_mod(
                ver["files"][0]["url"], path=path, filename=filename
            )
            if resp[0]:
                count += 1
            else:
                logging.error("Failed to downlaod: %s", title)

        logging.info("Downloaded %s mods.", count)
