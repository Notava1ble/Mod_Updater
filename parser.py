import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Update mods using the Modrinth API.")
    parser.add_argument(
        "-p",
        "--path",
        default="./mods/",
        required=False,
        type=str,
        help="Path where to update mods(default: ./mods/).",
    )
    parser.add_argument(
        "-v",
        "--version",
        default="latest",
        required=False,
        type=str,
        help="The version of the mod to download. Example: 1.21.1 (default: latest)",
    )
    parser.add_argument(
        "-l",
        "--loader",
        default="fabric",
        required=False,
        type=str,
        help="The mod loader to use. (default: fabric)",
    )
    return parser.parse_args()
