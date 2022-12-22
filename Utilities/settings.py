import configparser
from os import path

config = configparser.ConfigParser()
config_file = path.realpath('config.ini')
config.read(config_file)

# Where mods are installed to
mods_dir = config['path']['mods_dir']
# The base Sims 4 game path
game_dir = config['path']['game_dir']
data_dir = config['path']['data_dir']
python_dir = config['path']['python_dir']
# Where Sims 4 extracted data should go
extracted_assets_dir = config['path']['extracted_assets_dir']
interim_mods_dir = config['path']['interim_mods_dir']
hotreload_dir = config['path']['hotreload_dir']
