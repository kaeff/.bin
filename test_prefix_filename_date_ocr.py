import os
import shutil
import tempfile
import unittest
from prefix_filename_date_ocr import get_new_filename
import datetime
import fpdf #pip3 intall fpdf

def write_pdf_with_static_text(file_path, text):
    pdf = fpdf.FPDF(format='letter') #pdf format
    pdf.add_page() #create new page
    pdf.set_font("Arial", size=12) # font and textsize
    pdf.cell(200, 10, txt=text, ln=1, align="L")
    pdf.output(file_path)

class TestGetNewFilename(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.tmp_dir, "temp_file.pdf")
    
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
    
    def test_use_date_from_text_in_file(self):
        write_pdf_with_static_text(self.temp_file, "01.02.2022")
        new_filename = get_new_filename(self.temp_file, False)
        self.assertEqual("2022-02-01_temp_file.pdf", os.path.basename(new_filename))
    
    def test_use_last_modified_date_if_text_contains_no_date(self):
        write_pdf_with_static_text(self.temp_file, "")
        # Set the last modified date of the file to a specific date
        specific_date = datetime.datetime(2022, 3, 15)
        os.utime(self.temp_file, (specific_date.timestamp(), specific_date.timestamp()))

        new_filename = get_new_filename(self.temp_file, True)
        self.assertEqual("2022-03-15_temp_file.pdf", os.path.basename(new_filename))

if __name__ == "__main__":
    unittest.main()