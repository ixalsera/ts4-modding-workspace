import settings

green = '\033[33;1m'
reset = '\033[0m'

print(green + 'Current Settings:\n' + reset)
print(green + 'Creator Name: ' + reset + settings.creator_name)
print(green + 'Sims 4 Directory: ' + reset + settings.game_dir)
print(green + 'Sims 4 Mods Directory: ' + reset + settings.mods_dir)
print(green + 'Extracted assets will be saved in: ' + reset + settings.extracted_assets_dir)
print(green + 'Work-In-Progress Mods can be located in: ' + reset + settings.interim_mods_dir)
