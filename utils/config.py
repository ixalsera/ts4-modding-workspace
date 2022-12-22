from configparser import ConfigParser
from os import path

config = ConfigParser()
config_file = path.realpath(path.join(__file__, '..', 'config.ini'))
config.read(config_file)

creator_name = config['basic']['creator']
# Where mods are installed to
mods_dir = config['paths']['mods_dir']
# The base Sims 4 game path
game_dir = config['paths']['game_dir']
data_dir = config['paths']['data_dir']
python_dir = config['paths']['python_dir']
# Where Sims 4 extracted data should go
extracted_assets_dir = config['paths']['extracted_assets_dir']
interim_mods_dir = config['paths']['interim_mods_dir']
hotreload_dir = config['paths']['hotreload_dir']
