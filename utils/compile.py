import getopt
import os
import shutil
import config
import sys
from zipfile import PyZipFile, ZIP_STORED

_compile_with_get_dir = False
_compile_with_injector = False
_compile_with_settings = False

_helper_directory = os.path.realpath(os.path.join(__file__, '..', '..', 'helpers'))


def compile_module(creator, mod, mods_path):
    """ Compiles the provided mod name to .ts4script

    Generates a FQMN (Fully Qualified Mod Name) from a provided creator and mod name,
    then compiles the scripts and resources in the mod's directory to a .ts4script
    archive, storing it in the user's Sims 4 Mods directory.
    """
    # Grab our global variables
    global _compile_with_injector
    global _compile_with_settings

    mod_path = os.path.join(config.interim_mods_dir, mod)
    fully_qualified_mod_name = creator + '_' + mod

    if _compile_with_injector:
        include_injector(mod_path)

    if _compile_with_settings:
        include_settings(mod_path)

    if _compile_with_get_dir:
        include_get_dir(mod_path)

    mod_folder_copy = os.path.join(mods_path, fully_qualified_mod_name + '.ts4script')

    zip_file = PyZipFile(mod_folder_copy, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
    for folder, subs, files in os.walk(mod_path):
        zip_file.writepy(folder)
        for file in files:
            if '__pycache__' not in folder:
                zip_file.write(os.path.join(mod_path, file), str(mod + file))
    zip_file.close()


def include_injector(mod_path):
    """ Copies the injector script in to the mod directory """
    global _helper_directory

    target = os.path.join(mod_path, 'injector.py')
    if os.path.exists(target):
        os.unlink(target)
    shutil.copy(os.path.realpath(os.path.join(_helper_directory, 'injector.py')), target)


def include_get_dir(mod_path):
    """ Copies the injector script in to the mod directory """
    global _helper_directory

    target = os.path.join(mod_path, 'get_dir.py')
    if os.path.exists(target):
        os.unlink(target)
    shutil.copy(os.path.realpath(os.path.join(_helper_directory, 'get_dir.py')), target)


def include_settings(mod_path):
    """ Copies the settings script in to the mod directory

    Since the game is unable to load non-Python files from the .ts4script,
    we need to inject our variables in to our settings script at compile time.
    """
    global _helper_directory

    # Check for the existence of the settings file, removing it if it exists
    target = os.path.join(mod_path, 'settings.py')
    if os.path.exists(target):
        os.unlink(target)

    settings_strings = ''
    # Notice the double quoting of the below strings. This is to perform exact match and
    # replace to avoid substring matching. I didn't want to deal with regex right now.
    # Also notice the `r` prefix to the substitution value. This ensures that the resultant
    # string is treated as a literal to prevent escape sequencing with Windows paths
    settings_strings_dict = {
        "'CREATOR'": "r'" + config.creator_name + "'",
        "'MODS_DIR'": "r'" + config.mods_dir + "'",
        "'GAME_DIR'": "r'" + config.game_dir + "'",
        "'DATA_DIR'": "r'" + config.data_dir + "'",
        "'PYTHON_DIR'": "r'" + config.python_dir + "'",
        "'EXTRACTED_ASSETS_DIR'": "r'" + config.extracted_assets_dir + "'",
        "'INTERIM_MODS_DIR'": "r'" + config.interim_mods_dir + "'",
        "'HOTRELOAD_DIR'": "r'" + config.hotreload_dir + "'",
    }

    # Read in the contents of the settings.py helper
    settings_helper_path = os.path.realpath(os.path.join(_helper_directory, 'settings.py'))
    settings_helper_handle = open(settings_helper_path, 'r')
    template_settings = settings_helper_handle.read()

    # Iterate through the settings and replace values
    for line in template_settings.split('\n'):
        if line.startswith('#'):
            # Skip comments
            continue
        for find, replace in settings_strings_dict.items():
            if line.find(find) != -1:
                settings_strings += line.replace(find, replace) + '\n'

    # Close the file descriptor
    settings_helper_handle.close()

    target_handle = open(target, 'w')
    target_handle.write(settings_strings)
    target_handle.close()


def show_help():
    """ Displays the help text for this script """
    print("""
Usage:
compile.py [-h|i|s] mod_name

Compiling a module is as simple as running compile.py and providing the name of the mod to compile!

To facilitate easier management of mods, since there are three helpers - get_dir.py, injector.py and
settings.py - if you would like to compile your module with support for these modules, you can use
the convenience options provided.

Options:

-h|--help               Display this help text
-d|--compile-dir        Include the get_dir.py helper when compiling the mod
-i|--compile-injector   Include the injector.py helper when compiling the mod
-s|--compile-settings   Include the settings.py and config.ini when compiling the mod
""")


def main(argv):
    global _compile_with_get_dir
    global _compile_with_injector
    global _compile_with_settings
    try:
        opts, args = getopt.getopt(argv, "hdis", [
            'help',
            'compile-dir',
            'compile-injector',
            'compile-settings',
        ])
    except getopt.GetoptError as error:
        print(error)
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
            sys.exit()
        elif opt in ('-i', '--compile-injector'):
            _compile_with_injector = True
        elif opt in ('-s', '--compile-settings'):
            _compile_with_settings = True
        elif opt in ('-d', '--compile-dir'):
            _compile_with_get_dir = True
    if not len(args):
        print('Insufficient arguments provided; at least one mod name must be specified')
        show_help()
        sys.exit(2)
    if len(args) > 1:
        print('Too many arguments provided; please specify only one mod name')
        show_help()
        sys.exit(2)
    for mod_name in args:
        compile_module(config.creator_name, mod_name, config.mods_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
