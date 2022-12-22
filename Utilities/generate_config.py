from configparser import ConfigParser
from dotenv import load_dotenv
from os import getenv, path
from sys import platform

load_dotenv()


def determine_mods_directory() -> str:
    """ Determines the location of the Mods directory

    While the location of the users Mods directory for The Sims 4 (not WIP mods) is constant
    across platforms - EA doesn't let you customise this path - we need to cater for things
    like Documents folder redirection in Windows (for cases like OneDrive).
    """
    base_mods_dir = path.join('Electronic Arts', 'The Sims 4', 'Mods')
    mods_path = path.join(path.expanduser('~'), 'Documents', base_mods_dir)
    if not path.isdir(mods_path):
        mods_path = getenv('CUSTOM_MODS_DIR', False)
        if not mods_path:
            raise RuntimeError('Cannot locate Sims 4 Mods directory; please set a location under CUSTOM_MODS_DIR in '
                               '.env')
        if not path.isdir(mods_path):
            raise RuntimeError('Unable to locate or resolve custom mods directory: ' + mods_path)
    return mods_path


def determine_game_directory() -> str:
    """ Determines the location of the Sims 4 base path

    The base path is used to determine a number of other paths within the scripts
    such as where to grab the gameplay zips. There are a number of standard
    locations, but a user is able to override this with CUSTOM_GAME_DIR in .env
    """
    # If the user has provided a custom game directory, set it here
    custom_game_dir = getenv('CUSTOM_GAME_DIR', False)
    if custom_game_dir:
        game_path = path.realpath(custom_game_dir)
        if not path.isdir(game_path):
            raise RuntimeError('Unable to locate or resolve custom game directory: ' + game_path)
    else:
        if platform == 'win32':
            game_path = path.join(path.expandvars('%programfiles%'), 'Origin', 'The Sims 4')
        else:
            game_path = path.join(path.expanduser('~'), 'Applications', 'The Sims 4.app', 'Contents')

    return game_path


def generate_config():
    # Where mods are installed to
    mods_dir = determine_mods_directory()
    # The base Sims 4 game path
    game_dir = determine_game_directory()
    data_dir = path.join(game_dir, 'Data', 'Simulation', 'Gameplay')
    python_dir = path.join(game_dir, 'Python')
    # Where Sims 4 extracted data should go
    extracted_assets_dir = getenv('ASSETS_DIR', path.realpath(__file__ + '/../../EA'))
    interim_mods_dir = getenv('WIP_MODS', path.realpath(__file__ + '/../../Mods'))
    hotreload_dir = path.join(interim_mods_dir, 'hotreload')

    config = ConfigParser()
    # Store the config file next to the scripts for easier linking
    config_file = path.realpath(__file__ + '/../config.ini')

    # The user's mod creator name
    config['basic'] = {
        'creator': getenv('CREATOR', 'ACoolSims4Modder'),
    }

    config['paths'] = {
        'mods_dir': mods_dir,
        'game_dir': game_dir,
        'data_dir': data_dir,
        'python_dir': python_dir,
        'extracted_assets_dir': extracted_assets_dir,
        'interim_mods_dir': interim_mods_dir,
        'hotreload_dir': hotreload_dir,
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    return config_file


generate_config()
