# {"datei_name":"test_pdf",
# "datei_typ":"pdf",
# "autor":"test_autor",
# "titel":"test_titel",
# "page_count":2,
# "topics":["test_topic1","test_topic2"],
# "pages":[
#     {"page_num":1,
#     "text":"test_text",
#     "pictures":[
#         {"pic_num":1,
#         "pic_description":"test_pic_description"}
#         ],
#     "topics":["test_topic1","test_topic2"]},
#     {"page_num":2,
#     "text":"test_text",
#     "pictures":[
#         {"pic_num":1,
#         "pic_description":"test_pic_description"}
#         ],
#     "topics":["test_topic1","test_topic2"]}
#     ]
# }
# needed functions:
# - extract_text
# - extract_pictures
# - extract_metadata
# - find_topics
# - describe_pictures
import base64
import os

from PyPDF2 import PdfReader
from PIL import Image
import json
import requests

pdfDict = {"datei_name": "test_pdf",
           "datei_typ": "pdf",
           "autor": "test_autor",
           "titel": "test_titel",
           "page_count": 2,
           "topics": ["test_topic1", "test_topic2"],
           "pages": [
               {"page_num": 1,
                "text": "test_text",
                "pictures": [

                ],
                "topics": ["test_topic1", "test_topic2"]
                }
           ]
           }


def create_page(page_num, text, pictures, topics):
    page = {"page_num": page_num,
            "text": text,
            "pictures": pictures,
            "topics": topics
            }
    return page


def extract_text(pdf_file_name):
    reader = PdfReader(pdf_file_name)
    text = {}
    count = 0
    for page in reader.pages:
        text.update({f"page_{count}": page.extract_text()})
        count += 1
    return text


def extract_pictures(pdf_file_name):
    pictures = {}
    pictures_as_bytes = {}
    reader = PdfReader(pdf_file_name)
    count = 0
    pagecount = 0
    title = reader.metadata.get("/Title", pdf_file_name)
    title = title.split("/")[-1]
    title = title.split(".")[0]
    for page in reader.pages:
        pictures_in_page = {}
        if not os.path.exists("images/" + title):
            os.mkdir("images/" + title)

        for image_file_object in page.images:
            img_adress = "images/" + title + "/" + str(count) + image_file_object.name
            with open(img_adress, "wb") as fp:
                fp.write(image_file_object.data)

            pictures_as_bytes.update({f"picture_{count}": base64.b64encode(image_file_object.data).decode("utf-8")})
            pictures_in_page.update({f"picture_{count}": img_adress})
            count += 1

        pictures.update({f"page_{pagecount}": pictures_in_page})
        pagecount += 1

    with open("images/" + title + "/" + title + "_pictures_as_bytes" + ".json", "w") as fp:
        json.dump(pictures_as_bytes, fp)

    return pictures


def extract_metadata(pdf_file_name):
    reader = PdfReader(pdf_file_name)
    metadata = reader.metadata
    return metadata


def find_topics(text):
    topics = []
    return topics


def describe_pictures(pictures):
    descriptions = {}

    return descriptions


def extract_all_data(pdf_file_name):
    text = extract_text(pdf_file_name)
    pictures = extract_pictures(pdf_file_name)
    metadata = extract_metadata(pdf_file_name)
    topics = find_topics(text)
    descriptions = describe_pictures(pictures)
    title = metadata.get("/Title", pdf_file_name)
    title = title.split("/")[-1]
    title = title.split(".")[0]

    data = {}
    data.update({"datei_name": pdf_file_name})
    data.update({"datei_typ": "pdf"})
    data.update({"autor": metadata.get("/Author", "unknown")})
    data.update({"titel": title})
    for page_num in range(len(text)):
        page_key = f"page_{page_num}"
        data[page_key] = {
            "text": text.get(page_key, ""),
            "pictures": pictures.get(page_key, {})
        }

    with open("images/" + title + "/" + title + ".json", "w") as fp:
        json.dump(data, fp)
    return data


print(extract_all_data("test_pdfs/41-swen-2-refactoring.pdf"))

with open("images/41-swen-2-refactoring/41-swen-2-refactoring_pictures_as_bytes.json", "r") as fp:
    data = json.load(fp)
    print(requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llava:13b",
            "prompt": "descibe the picture",
            "stream": False,
            "images": [data["picture_10"]]},

    ).text)
