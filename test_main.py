import pytest
from main import extract_pictures, extract_text, extract_all_data


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


def test_extract_pictures_with_no_pdf():
    answer = ""
    # Path to the sample PDF file with no images
    try:
        sample_pdf = 'test_pdfs/does_not_exist.pdf'

        # Call the function
        extracted_pictures = extract_pictures(sample_pdf)
    except FileNotFoundError:
        answer = "File not found"

    # Assert that the total number of extracted images is as expected
    assert answer == "File not found", "Total images extracted does not match the expected number"


def test_extract_text_with_one_word():
    sample_pdf = 'test_pdfs/Präsentation1.pdf'

    # Call the function
    extracted_text = extract_text(sample_pdf)
    print(extracted_text)

    # Assert that the total number of extracted images is as expected
    assert extracted_text == {'page_0': 'test'}, "Total text extracted does not match the expected number"


def test_extract_text_with_valid_pdf():
    # Load a known PDF file and check its content
    result = extract_text('test_pdfs/lotsOfText.pdf')
    # Verify that the result is as expected
    assert isinstance(result, dict)
    assert "page_0" in result
    assert "page_1" in result


def test_extract_text_with_empty_pdf():
    result = extract_text('test_pdfs/empty.pdf')
    assert isinstance(result, dict)
    assert len(result) == 0


def test_extract_text_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        extract_text('nonexistent_file.pdf')


def test_extract_text_page_count():
    result = extract_text('test_pdfs/lotsOfText.pdf')
    expected_page_count = 5
    assert len(result) == expected_page_count


def test_extract_text_specific_page_content():
    result = extract_text('test_pdfs/lotsOfText.pdf')
    # Check the content of a specific page
    assert "DIETARY HABITS IN LATVIA" in result["page_0"]


def test_extract_all_data_with_valid_pdf():
    # Load a known PDF file and check its content
    result = extract_all_data('test_pdfs/Text_und_Bilder.pdf')
    # Verify that the result is as expected
    assert isinstance(result, dict)
    assert "page_0" in result
    assert "text" in result["page_0"]
    assert "pictures" in result["page_0"]
    assert len(result["page_0"]["pictures"]) == 1


def test_extract_all_data_with_empty_pdf():
    result = extract_all_data('test_pdfs/empty.pdf')
    assert isinstance(result, dict)
    assert len(result) == 0


def test_extract_all_data_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        extract_all_data('nonexistent_file.pdf')


def test_extract_all_data_page_count():
    result = extract_all_data('test_pdfs/Text_und_Bilder.pdf')
    expected_page_count = 4
    assert len(result) == expected_page_count


def test_extract_all_data_specific_page_content():
    result = extract_all_data('test_pdfs/Text_und_Bilder.pdf')
    # Check the content of a specific page
    assert "testtest" in result["page_0"]["text"]
    assert "picture_0" in result["page_0"]["pictures"]