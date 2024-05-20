import os
from pathlib import Path
from convert_filename_date import rename_files_in_directory


class TestRenameFilesInDirectory:

    def test_rename_files_in_directory(self, tmp_path: Path):
        file1_name = '20220429_file1.pdf'
        file2_name = '20220429_file2.pdf'
        file3_name = 'random_file.pdf'
        file1_path, file2_path, file3_path = _create_files(
            tmp_path, file1_name, file2_name, file3_name)

        # Confirm that files are not yet renamed
        assert os.path.exists(file1_path)
        assert os.path.exists(file2_path)
        assert os.path.exists(file3_path)

        # Rename files
        rename_files_in_directory(
            tmp_path, "YYYYMMDD", "YY-MM-DD", ask_for_consent=False)

        # Confirm that files are now renamed
        assert os.path.exists(tmp_path / "22-04-29_file1.pdf")
        assert os.path.exists(tmp_path / "22-04-29_file2.pdf")
        assert os.path.exists(file3_path)


def _create_files(tmp_dir, *file_names):
    file_paths = [os.path.join(tmp_dir, file_name) for file_name in file_names]

    for file_path in file_paths:
        with open(file_path, 'w') as f:
            f.write(file_path)
    return file_paths
