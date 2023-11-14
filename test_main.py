import pytest
from main import extract_pictures


def test_extract_pictures_with_multiple_images():
    # Path to the sample PDF file with known images
    sample_pdf = 'test_pdfs/2bilder_5seiten.pdf'

    # Call the function
    extracted_pictures = extract_pictures(sample_pdf)
    print(extracted_pictures.keys())
    # Count total images extracted
    total_images = sum(len(page) for page in extracted_pictures.values())

    # Assert that the total number of extracted images is as expected
    assert total_images == 2, "Total images extracted does not match the expected number"


def test_extract_pictures_with_three_image():
    # Path to the sample PDF file with known images
    sample_pdf = 'test_pdfs/multiple_images.pdf'

    # Call the function
    extracted_pictures = extract_pictures(sample_pdf)
    print(extracted_pictures.keys())
    # Count total images extracted
    total_images = sum(len(page) for page in extracted_pictures.values())

    # Assert that the total number of extracted images is as expected
    assert total_images == 3, "Total images extracted does not match the expected number"


def test_extract_pictures_with_no_images():
    # Path to the sample PDF file with no images
    sample_pdf = 'test_pdfs/Präsentation1.pdf'

    # Call the function
    extracted_pictures = extract_pictures(sample_pdf)

    # Count total images extracted
    total_images = sum(len(page) for page in extracted_pictures.values())

    # Assert that the total number of extracted images is as expected
    assert total_images == 0, "Total images extracted does not match the expected number"


def test_extract_pictures_with_empty_pdf():
    # Path to the sample PDF file with no images
    sample_pdf = 'test_pdfs/empty.pdf'

    # Call the function
    extracted_pictures = extract_pictures(sample_pdf)

    # Count total images extracted
    total_images = sum(len(page) for page in extracted_pictures.values())

    # Assert that the total number of extracted images is as expected
    assert total_images == 0, "Total images extracted does not match the expected number"
