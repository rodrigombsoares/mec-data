import os
import shutil

from mec_data.data_lake.base import DataLakeBase
from mec_data.utils.download_manager import create_if_not_exists


class LocalDL(DataLakeBase):
    data_lake = os.path.join(os.getcwd(), "data_lake")

    def store(self, bucket, prefix, file):
        path = os.path.join(self.data_lake, bucket, prefix)
        create_if_not_exists(path)
        print(path)
        shutil.move(file, path)
        return True

    def get_files(self, bucket, prefix):
        folder = os.path.join(self.data_lake, bucket, prefix)
        paths = []
        for root, subdirs, files in os.walk(folder):
            for file in files:
                paths.append(os.path.join(root, file))
        return paths
