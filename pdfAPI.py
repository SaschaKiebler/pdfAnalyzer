
import base64
import os
import io
from PyPDF2 import PdfReader
from PIL import Image
import json
import requests
import fitz

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
    doc = fitz.open(pdf_file_name)
    pictures = {}
    image_count = 0
    page_count = 0
    title = os.path.splitext(os.path.basename(pdf_file_name))[0]

    images_dir = "images/" + title
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for page in doc:
        pictures_in_page = {}
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Use PIL to handle the image
            img = Image.open(io.BytesIO(image_bytes))
            img_adress = f"{images_dir}/{image_count}_{img_index}.png"

            # Save the image
            img.save(img_adress, format="PNG")
            pictures_in_page.update({f"picture_{image_count}": {"path": img_adress, "description": ""}})
            image_count += 1

        pictures.update({f"page_{page_count}": pictures_in_page})
        page_count += 1

    doc.close()
    return pictures


def extract_metadata(pdf_file_name):
    reader = PdfReader(pdf_file_name)
    metadata = reader.metadata
    return metadata


def find_topics(text):
    topics = []
    return topics


def describe_pictures(pictures):

    for page in pictures:
        for pic in pictures[page]:
            # open the pictures as bytes from the path in pictures
            image = Image.open(pictures[page][pic]["path"])

            # Save the image to a bytes buffer
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Convert to base64
            img_str = base64.b64encode(buffer.getvalue()).decode()

            description = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llava:13b",
                    "prompt": "Analyze the following picture and describe it in a few sentences. If there is any text in the "
                              "picture, please also extract it.",
                    "stream": False,
                    "images": [img_str]},

            ).json()
            pictures[page][pic]["description"] = description.get("response", "no description found")
    return pictures


def extract_all_data(pdf_file_name):
    text = extract_text(pdf_file_name)
    pictures = extract_pictures(pdf_file_name)
    metadata = extract_metadata(pdf_file_name)
    topics = find_topics(text)

    title = metadata.get("/Title", pdf_file_name)
    title = title.split("/")[-1]
    title = title.split(".")[0]

    descripted_pics = describe_pictures(pictures)

    data = {}
    data.update({"datei_name": pdf_file_name})
    data.update({"datei_typ": "pdf"})
    data.update({"autor": metadata.get("/Author", "unknown")})
    data.update({"titel": title})
    for page_num in range(len(text)):
        page_key = f"page_{page_num}"
        data[page_key] = {
            "text": text.get(page_key, ""),
            "pictures": descripted_pics.get(page_key, {})
        }

    with open("images/" + title + "/" + title + ".json", "w") as fp:
        json.dump(data, fp)
    return data


print(extract_all_data("test_pdfs/Kommunikation im Medizinwesen.pdf"))


