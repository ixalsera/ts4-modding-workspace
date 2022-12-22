import getopt
import os
import settings
import sys
from zipfile import PyZipFile, ZIP_STORED

_compile_with_injector = False
_compile_with_settings = False


def compile_module(creator, mod, mods_path):
    """ Compiles the provided mod name to .ts4script

    Generates a FQMN (Fully Qualified Mod Name) from a provided creator and mod name,
    then compiles the scripts and resources in the mod's directory to a .ts4script
    archive, storing it in the user's Sims 4 Mods directory.
    """
    mod_path = os.path.join(settings.interim_mods_dir, mod)
    fully_qualified_mod_name = creator + '_' + mod

    mod_folder_copy = os.path.join(mods_path, fully_qualified_mod_name + '.ts4script')

    zip_file = PyZipFile(mod_folder_copy, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
    for folder, subs, files in os.walk(mod_path):
        zip_file.writepy(folder)
        for file in files:
            if '__pycache__' not in folder:
                zip_file.write(os.path.join(mod_path, file), str(mod + file))
    zip_file.close()


def show_help():
    """ Displays the help text for this script """
    print(os.path.basename(__file__) + ' [-h|i|s] mod_name')
    print("""
Compiling a module is as simple as running compile.py and providing the name of the mod to compile!

To facilitate easier management of mods, since there are two helpers - injector.py and settings.py -
if you would like to compile your module with support for these modules, you can use the convenience
options provided.

Options:

-h|--help               Display this help text
-i|--compile-injector   Include the injector.py helper when compiling the mod
-s|--compile-settings   Include the settings.py and config.ini when compiling the mod
""")


def main(argv):
    global _compile_with_injector
    global _compile_with_settings
    try:
        opts, args = getopt.getopt(argv, "his", [
            'help',
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
        if opt in ('-i', '--compile-injector'):
            _compile_with_injector = True
        if opt in ('-s', '--compile-settings'):
            _compile_with_settings = True
    if not len(args):
        print('Insufficient arguments provided; at least one mod name must be specified')
        show_help()
        sys.exit(2)
    for mod_name in args:
        compile_module(settings.creator_name, mod_name, settings.mods_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
