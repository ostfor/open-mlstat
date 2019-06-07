import os
import zipfile


def zip_data(path_to_data):
    nm = os.path.basename(path_to_data)
    assert os.path.exists(path_to_data)

    result = os.path.join("/tmp", nm + ".zip")

    f_zip = zipfile.ZipFile(result, 'w', zipfile.ZIP_DEFLATED)

    if os.path.isdir(path_to_data):
        for root, dirs, files in os.walk(path_to_data):
            for file in files:
                f_zip.write(os.path.join(root, file))
    else:
        f_zip.write(path_to_data)

    f_zip.close()
    return result

if __name__ == '__main__':
    print (zip_data("data/test.txt"))