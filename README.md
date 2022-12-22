![](https://user-images.githubusercontent.com/7295363/160976635-1ca3a6ce-43b6-47c2-98e3-71d0fcb8e11f.png)

# ts4-modding-workspace

> :hammer_and_wrench: Scripting workspace for modding The Sims 4

## Features

This repository is designed to bootstrap your scripting process when making mods for The Sims 4. If you don't know where to start or can't seem to get your script files organized, check out this repository. It's designed as a boilerplate for you to customize for your own modding process. It provides the following:

- **Utility mods** (to be compiled and used as needed):
  - `hello_world`: example mod
    - `example_script.py`: includes a `hello_world` command and an example injection with a notification
    - `injector.py`: this mod's symlink to `./Utilities/injector.py`
  - `hotreload`: includes commands for reloading your `*.py` and `*.xml` files without restarting the game
    - `script_reloader.py`: hot-reloads the specified `*.py` file (e.g., `r.script hello_world example_script`)
    - `settings.py`: this mod's symlink to `./Utilities/injector.py`
    - `xml_reloader.py`: hot-reloads the `*.xml` file configured in `xml_reloader.py` (e.g., `r.xml`)
- **~~Bash scripts~~**:
  - The convenience scripts have been removed since we no longer require a Python symlink
- **Utility scripts** (to be [symlinked](https://www.google.com/search?q=how+to+make+a+symlink) into your mod folders/files as needed):
  - `get_dir.py`: easily fetch the directory of your mod, helpful for working with files your mod might generate or use
  - `injector.py`: inject your scripts into pre-existing game code (learn how to use [here](https://modthesims.info/showthread.php?p=4751246#post4751246) and see `@inject_to` in `./Mods/hello_world/example_script.py` for reference)

## Instructions

- Install the latest version of [miniconda](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links)
if you haven't already. Don't worry that it is bundled with the latest version of Python, we are specifically using `conda`
to manage a virtual environment.
- If this is the first time setting up a project, run `conda  env create --file environment.yaml` from the project root.
This will install the project dependencies as well as Python 3.7 in a virtual environment called `ts4_modding_workspace`.
  - If you have already created the environment, you can activate the existing environment with `conda activate ts4_modding_workspace`.
- Copy the `.env.dist` file to `.env` and adjust the values accordingly. Any that aren't necessary may be left blank and
default values will be used.
- Generate a configuration file for use with scripts by running `python Utilities/generate_config.py`. This config file
  will need to be re-generated if you make changes to any of the environment variables.
- Test your configuration with `python Utilities/validate_settings.py`. This will output your config or throw errors if
there are issues.

## Notes

- Don't use capital letters in mod folder or file names.
- Have ideas for improving the workspace? Fork and submit a PR back to the repository!
- Instead of duplicating your shared files, have one single source and [symlink](https://www.google.com/search?q=how+to+make+a+symlink)
  all references (e.g., `ln -s /path/to/original /path/to/link` on *nix, `mklink path\to\link path\to\original` on Windows
  (Command Prompt), `New-Item -ItemType SymbolicLink -Path "Link" -Target "Target"` on Windows (PowerShell))

## Acknowledgments

This repository was made possible by:

- [LOT51](https://lot51.cc/)
- [Scumbumbo](https://scumbumbomods.com/)
- [thepancake1 and MizoreYukii](https://www.patreon.com/pancakemizore)
- [Deaderpool](https://deaderpool-mccc.com/)
