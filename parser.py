import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Update mods from Modrinth.")
    parser.add_argument(
        "-p",
        "--path",
        default="./mods/",
        required=False,
        type=str,
        help="Path where to update mods(default: appdata/roaming/.minecraft/mods).",
    )
    parser.add_argument(
        "-v",
        "--version",
        default="latest",
        required=False,
        type=str,
        help="The version of the mod to download. Example: 1.21.1 (default: latest)",
    )
    return parser.parse_args()
