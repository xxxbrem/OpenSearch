import os
import shutil

db_folder = "test_database"
for file in os.listdir(db_folder):
    if file.endswith(".sqlite"):
        target_pth = os.path.join(db_folder, file.replace(".sqlite", ""))
        if not os.path.exists(target_pth):
            os.mkdir(target_pth)
        shutil.move(os.path.join(db_folder, file), target_pth)