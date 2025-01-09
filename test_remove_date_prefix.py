import os
from pathlib import Path

from remove_date_prefix import main


class TestRenameFilesInDirectory:

    def test_rename_files_in_directory(self, tmp_path: Path):
        file1_name = '20220429_file1.pdf'
        file2_name = '22-04-29_file2.pdf'
        file3_name = 'random_file.pdf'
        _create_files(tmp_path, file1_name, file2_name, file3_name)

        main(tmp_path.as_uri(), True)

        # Confirm that files are now renamed
        assert os.path.exists(tmp_path / "file1.pdf")
        assert os.path.exists(tmp_path / "file2.pdf")
        assert os.path.exists(tmp_path / "random_file.pdf")


def _create_files(tmp_dir, *file_names):
    file_paths = [os.path.join(tmp_dir, file_name) for file_name in file_names]

    for file_path in file_paths:
        with open(file_path, 'w') as f:
            f.write(file_path)
    return file_paths
