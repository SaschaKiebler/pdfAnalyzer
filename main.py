# parse the pdf in a structured output json format and save it in a file
# example format:
# {"page1":
# {"text": "text",
# "title": "title",
# "subtitle": "subtitle",
# "tables": ["table1","table2"],
# "pictures": ["pic1", "pic2"]
# },
# "page2": {...}
# }
import io

from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


def extract_pictures(pdf_file_name):
    pictures = {}
    reader = PdfReader(pdf_file_name)
    count = 0
    pagecount = 0

    for page in reader.pages:
        pictures_in_page = {}
        for image_file_object in page.images:
            pictures_in_page.update({f"picture_{count}": image_file_object.data})
            count += 1
        pictures.update({f"page_{pagecount}": pictures_in_page})
        pagecount += 1

    return pictures


def extract_text(pdf_file_name):
    reader = PdfReader(pdf_file_name)
    text = {}
    count = 0
    for page in reader.pages:
        text.update({f"page_{count}": page.extract_text()})
        count += 1
    return text


def extract_all_data(pdf_file_name):
    text = extract_text(pdf_file_name)
    pictures = extract_pictures(pdf_file_name)

    data = {}
    for page_num in range(len(text)):
        page_key = f"page_{page_num}"
        data[page_key] = {
            "text": text.get(page_key, ""),
            "pictures": pictures.get(page_key, {})
        }

    return data
