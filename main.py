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




# images = extract_pictures("test_pdfs/01 Einführung.pdf").get("page_4").items()
# print(images)
# for image in images:
#     Image.open(io.BytesIO(image[1])).show()
