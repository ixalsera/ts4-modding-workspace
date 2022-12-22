import os
import settings
import sys
from zipfile import PyZipFile, ZIP_STORED


def compile_module(creator_name, root, mods_folder):
    mod_name = creator_name + '_' + os.path.basename(root)

    mod_folder_copy = os.path.join(mods_folder, mod_name + '.ts4script')

    zf = PyZipFile(mod_folder_copy, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
    for folder, subs, files in os.walk(root):
        zf.writepy(folder)
        for file in files:
            if '__pycache__' not in folder:
                zf.write(os.path.join(root, file), str(os.path.basename(root) + '/' + file))
    zf.close()


root = os.path.join(settings.interim_mods_dir, str(sys.argv[1]))
compile_module(settings.creator_name, root, settings.mods_dir)
