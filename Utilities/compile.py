import getopt
import os
import settings
import sys
from zipfile import PyZipFile, ZIP_STORED


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
    print(os.path.basename(__file__) + ' [] mod_name')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError as error:
        print(error)
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
    if not len(args):
        print('Insufficient arguments provided; at least one mod name must be specified')
        show_help()
        sys.exit(2)
    for mod_name in args:
        compile_module(settings.creator_name, mod_name, settings.mods_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
