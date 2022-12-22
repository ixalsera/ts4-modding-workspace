from configparser import ConfigParser
from os import path

config = ConfigParser()
config_file = path.realpath(path.join(__file__, '..', 'config.ini'))
print(config_file)
config.read(config_file)

green = '\033[33;1m'
reset = '\033[0m'

print(green + 'Current Settings:\n' + reset)
print(green + 'Creator Name: ' + reset + config['basic']['creator'])
print(green + 'Sims 4 Directory: ' + reset + config['paths']['game_dir'])
print(green + 'Sims 4 Mods Directory: ' + reset + config['paths']['mods_dir'])
print(green + 'Extracted assets will be saved in: ' + reset + config['paths']['extracted_assets_dir'])
print(green + 'Work-In-Progress Mods can be located in: ' + reset + config['paths']['interim_mods_dir'])
