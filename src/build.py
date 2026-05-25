import os, shutil

source_directory = "./static/"
build_directory = "./public/"

def copy_static_to_public():
    # Clean the destination directory
    if os.path.exists(build_directory):
        for filename in os.listdir(build_directory):
            file_path = os.path.join(build_directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    print(f"Deleting file {file_path}")
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    print(f"Deleting folder {file_path}")
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.mkdir(build_directory)

    shutil.copytree(source_directory, build_directory, dirs_exist_ok=True)

