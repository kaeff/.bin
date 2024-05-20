import os
import shutil
import tempfile
import pytest
from prefix_filename_date_ocr import get_new_filename
import datetime

import fpdf  # pip3 intall fpdf


def write_pdf_with_static_text(file_path, text):
    pdf = fpdf.FPDF(format='letter')  # pdf format
    pdf.add_page()  # create new page
    pdf.set_font("Arial", size=12)  # font and textsize
    pdf.cell(200, 10, txt=text, ln=1, align="L")
    pdf.output(file_path)


@pytest.fixture
def temp_file():
    tmp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(tmp_dir, "temp_file.pdf")
    yield temp_file
    shutil.rmtree(tmp_dir)


def test_use_date_from_text_in_file(temp_file):
    write_pdf_with_static_text(temp_file, "01.02.2022")
    new_filename = get_new_filename(temp_file, False)
    assert os.path.basename(new_filename) == "2022-02-01_temp_file.pdf"


def test_use_last_modified_date_if_text_contains_no_date(temp_file):
    write_pdf_with_static_text(temp_file, "")
    # Set the last modified date of the file to a specific date
    specific_date = datetime.datetime(2022, 3, 15)
    os.utime(temp_file, (specific_date.timestamp(), specific_date.timestamp()))

    new_filename = get_new_filename(temp_file, True)
    assert os.path.basename(new_filename) == "2022-03-15_temp_file.pdf"
