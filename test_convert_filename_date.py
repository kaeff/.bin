import os
import tempfile
import shutil
import unittest
from datetime import datetime
from convert_filename_date import convert_date_format, rename_files_in_directory

class TestConvertDateFormat(unittest.TestCase):
    def test_convert_date_format(self):
        filename1 = '20220429_filename.pdf'
        old_format1 = 'YYYYMMDD'
        new_format1 = 'YY-MM-DD'
        expected_filename1 = '22-04-29_filename.pdf'
        self.assertEqual(convert_date_format(filename1, old_format1, new_format1), expected_filename1)

        filename2 = '2022-04-29_filename.pdf'
        old_format2 = 'YYYY-MM-DD'
        new_format2 = 'DD-MM-YY'
        expected_filename2 = '29-04-22_filename.pdf'
        self.assertEqual(convert_date_format(filename2, old_format2, new_format2), expected_filename2)

        filename3 = '22-04-29_filename.pdf'
        old_format3 = 'YY-MM-DD'
        new_format3 = 'YYYYMMDD'
        expected_filename3 = '20220429_filename.pdf'
        self.assertEqual(convert_date_format(filename3, old_format3, new_format3), expected_filename3)

    def test_convert_date_format_with_space(self):
        filename1 = '20220429 filename.pdf'
        old_format1 = 'YYYYMMDD'
        new_format1 = 'YY-MM-DD'
        expected_filename1 = '22-04-29 filename.pdf'
        self.assertEqual(convert_date_format(filename1, old_format1, new_format1), expected_filename1)

    def test_convert_date_format_only_year(self):
        filename1 = '18 filename.pdf'
        old_format1 = 'YY'
        new_format1 = 'YYYY-MM-DD'
        expected_filename1 = '2018-01-01 filename.pdf'
        self.assertEqual(convert_date_format(filename1, old_format1, new_format1), expected_filename1)


class TestRenameFilesInDirectory(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

        self.current_date_format = 'YYYYMMDD'
        self.new_date_format = 'YYYY-MM-DD'

        self.file1_name = '20220429_file1.pdf'
        self.file2_name = '20220429_file2.pdf'
        self.file3_name = 'random_file.pdf'

        self.file1_path = os.path.join(self.tmp_dir, self.file1_name)
        self.file2_path = os.path.join(self.tmp_dir, self.file2_name)
        self.file3_path = os.path.join(self.tmp_dir, self.file3_name)

        self.file1_path_expected = os.path.join(self.tmp_dir, "22-04-29_file1.pdf")
        self.file2_path_expected = os.path.join(self.tmp_dir, "22-04-29_file2.pdf")


        with open(self.file1_path, 'w') as f1, open(self.file2_path, 'w') as f2, open(self.file3_path, 'w') as f3:
            f1.write('file1')
            f2.write('file2')
            f3.write('file3')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)


    def test_rename_files_in_directory(self):
        # Confirm that files are not yet renamed
        self.assertTrue(os.path.exists(self.file1_path))
        self.assertTrue(os.path.exists(self.file2_path))
        self.assertTrue(os.path.exists(self.file3_path))

        # Rename files
        renamings = rename_files_in_directory(self.tmp_dir, "YYYYMMDD", "YY-MM-DD", ask_for_consent=False)

        # Confirm that files are now renamed
        self.assertTrue(self.file1_path_expected)
        self.assertTrue(self.file2_path_expected)
        self.assertTrue(os.path.exists(self.file3_path))
if __name__ == '__main__':
    unittest.main()
