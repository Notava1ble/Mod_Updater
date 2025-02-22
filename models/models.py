from typing import TypedDict


class GameVersion(TypedDict):
    """Game version object."""

    version: str
    version_type: str
    date: str
    major: bool


class Mod(TypedDict):
    """Mod object."""

    id: str
    slug: str
    title: str
    description: str
    loaders: list[str]
    versions: list[str]
    game_versions: list[str]
