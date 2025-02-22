import json
import logging
import requests


class ModrinthClient:
    def __init__(self):
        self.base_url = "https://api.modrinth.com/v2"

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
        game_versions = self.get("/tag/game_version")

        for version in game_versions:
            if version["version_type"] == "release":
                logging.debug("Latest version: %s", version["version"])
                return version["version"]
