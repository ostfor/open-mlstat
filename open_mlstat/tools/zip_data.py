import os
import zipfile


def zip_directory(path_to_dir):
    f_zip = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path_to_dir):
        for file in files:
            f_zip.write(os.path.join(root, file))
    f_zip.close()
