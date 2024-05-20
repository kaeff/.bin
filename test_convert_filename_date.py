from convert_filename_date import convert_date_format


class TestConvertDateFormat:
    def test_convert_date_format_1(self):
        filename = '20220429_filename.pdf'
        old_format = 'YYYYMMDD'
        new_format = 'YY-MM-DD'
        expected_filename = '22-04-29_filename.pdf'

        assert convert_date_format(
            filename, old_format, new_format) == expected_filename

    def test_convert_date_format_2(self):
        filename = '2022-04-29_filename.pdf'
        old_format = 'YYYY-MM-DD'
        new_format = 'DD-MM-YY'
        expected_filename = '29-04-22_filename.pdf'

        assert convert_date_format(
            filename, old_format, new_format) == expected_filename

    def test_convert_date_format_3(self):
        filename = '22-04-29_filename.pdf'
        old_format = 'YY-MM-DD'
        new_format = 'YYYYMMDD'
        expected_filename = '20220429_filename.pdf'

        assert convert_date_format(
            filename, old_format, new_format) == expected_filename

    def test_convert_date_format_with_space(self):
        filename1 = '20220429 filename.pdf'
        old_format1 = 'YYYYMMDD'
        new_format1 = 'YY-MM-DD'
        expected_filename1 = '22-04-29 filename.pdf'
        assert convert_date_format(
            filename1, old_format1, new_format1) == expected_filename1

    def test_convert_date_format_only_year(self):
        filename1 = '18 filename.pdf'
        old_format1 = 'YY'
        new_format1 = 'YYYY-MM-DD'
        expected_filename1 = '2018-01-01 filename.pdf'
        assert convert_date_format(
            filename1, old_format1, new_format1) == expected_filename1
