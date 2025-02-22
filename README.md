# Minecraft Mod Updater

A Command Line Tool to automatically update all minecraft mods in a folder, using the Modrinth API.

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository using git, or download the files:

```terminal
git clone https://github.com/username/MinecraftModUpdater.git
```

2. Navigate to the project folder, and open the terminal there:

3. Install dependencies:

```terminal
pip install -r requirements.txt
```

## Usage

To update your Minecraft mods, run the following command in your terminal. It will look for a mods folder where the script itself is located. The old mods will be put in a folder named after the version they are.

```terminal
python main.py
```

If you want update the mods in the minecraft mods folder, provide the absolute path.

```terminal
python main.py -p [absolute_path_to_your_mods_folder]
```

### Options

- `--path`: Path to the directory containing Minecraft mods, which defaults to a mods folder in the folder where the script is itself.
- `--version`: The version to update to, which defaults to the latest release.
- `--loader`: The loader to use, which defaults to fabric.

## Examples

Update mods in the default mods folder:

```terminal
python main.py -p "C:\Users\your_name\AppData\Roaming\.minecraft\mods"
```

Downgrade the mods to 1.20, forge:

```terminal
python main.py -v 1.20 -l forge
```

## Contributing and Issues

If you encounter a bug, open an issue in the issues tab. You're welcome to contribute!

## License

Distributed under the MIT License. See `LICENSE` for more information.
