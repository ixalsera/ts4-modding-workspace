import io
import fnmatch
import os
import shutil
import settings
from zipfile import PyZipFile
from unpyc3 import decompile


def extract_folder(src_dir, target_dir):
    """ Extracts Sims 4 gameplay resources

    Recursively walks the Sims 4 'Gameplay' folder (<Sims4Base>/Data/Simulation/Gameplay),
    extracting any .zip or .ts4script files it finds to the designated output folder.
    """
    for root, dirs, files in os.walk(src_dir):
        for ext_filter in ['*.zip', '*.ts4script']:
            for filename in fnmatch.filter(files, ext_filter):
                extract_subfolder(root, filename, target_dir)


def extract_subfolder(root, filename, assets_dir):
    """ Extracts the assets from the Sims 4 Gameplay folder """
    src = os.path.join(root, filename)
    dst = os.path.join(assets_dir, filename)
    if src != dst:
        shutil.copyfile(src, dst)
    data_zip = PyZipFile(dst)
    out_folder = os.path.join(assets_dir, os.path.splitext(filename)[0])
    data_zip.extractall(out_folder)
    decompile_dir(out_folder)


def decompile_dir(root_path):
    pattern = '*.pyc'
    for root, dirs, files in os.walk(root_path):
        for filename in fnmatch.filter(files, pattern):
            p = str(os.path.join(root, filename))
            try:
                py = decompile(p)
                with io.open(p.replace('.pyc', '.py'), 'w', encoding='utf-8') as output_py:
                    for statement in py.statements:
                        output_py.write(str(statement) + '\r')
                print("SUCCESS: %s" % p)
            except Exception as ex:
                print(ex)
                print("FAIL: %s" % p)


if not os.path.exists(settings.extracted_assets_dir):
    os.mkdir(settings.extracted_assets_dir)

extract_folder(settings.data_dir, settings.extracted_assets_dir)
extract_folder(settings.python_dir, settings.extracted_assets_dir)
