# Minecraft Mod Updater

A simple and barebones Command Line Tool to automatically update all minecraft mods in a folder, using the Modrinth API.

To get started, install the executable file from [Releases](https://github.com/Notava1ble/Mod_Updater/releases) page. After downloading the executable, put it inside the .minecraft folder (or where your Minecraft instance is located) and just double click to update to latest version. For more control, open the terminal in the executable directory, and run it using: `Modupdater.exe` and optionally add any argument. The run logs will be saved at `./mod_updater.log`. If you want to have access to the script everywhere, put it inside a folder of your choice and add the folder to PATH.

Otherwise, if you want even more control, or don't want to run random executables, follow the steps below. 


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

To update your Minecraft mods, simply run the following command in your terminal. It will look for a mods folder where the script itself is located. The old mods will be backed up in a folder named after the version they are, in case you want to revert back.

```terminal
python main.py
```

If you want update the mods in the minecraft mods folder, provide its absolute path.

```terminal
python main.py -p [absolute_path_to_your_mods_folder]
```

### Options

- `--path`: Path to the directory containing Minecraft mods. Default: the ‘mods’ folder in the script's directory.
- `--version`: The version to update to. Default: latest game release.
- `--loader`: The loader to use, Default: fabric.

## Examples

Update mods to the latest game version in the default mods folder for Minecraft:

```terminal
python main.py -p "C:\Users\your_name\AppData\Roaming\.minecraft\mods"
```

Downgrade the mods to 1.20, forge:

```terminal
python main.py -v 1.20 -l forge
```

## Contributing and Issues

If you encounter a bug, open an Issue in the [Issues](https://github.com/Notava1ble/Mod_Updater/issues) page. If you’d like to contribute, feel free to submit a pull request with improvements or fixes.
