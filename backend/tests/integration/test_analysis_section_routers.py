"""Testing endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
from typing import List

from bson import ObjectId
from pydantic import TypeAdapter

from src.models.analysis import Section

from ..test_utils import fixture_filepath, read_test_fixture


def test_update_analysis_sections(client, mock_access_token, mock_repositories, cpam0047_analysis_json):
    """Testing if the update analysis endpoint updates an existing analysis"""

    mock_updated_sections = [{
        "header": "Brief",
        "content": [{"fieldName": "Decision", "value": ["the quick brown fox jumps over the lazy dog."]},
                    {"fieldName": "Nominator", "value": ["Lorem ipsum dolor"]}]
    }, {
        "header": "Medical Summary", "content": [{
            "fieldName": "Clinical Diagnosis",
            "value": ["Sed odio morbi quis commodo odio aenean sed. Hendrerit dolor magna eget lorem."]
        }]
    }]

    mock_repositories["analysis"].collection.find_one.return_value = cpam0047_analysis_json
    response = client.post(
        "/analysis/CPAM0047/sections/batch",
        headers={"Authorization": "Bearer " + mock_access_token},
        json=mock_updated_sections
    )

    assert response.status_code == 200
    mock_repositories["analysis"].collection.update_one.assert_called()


def test_update_individual_section_text_fields(client, mock_access_token, mock_repositories, cpam0047_analysis_json):
    """Testing if the update analysis endpoint updates an existing analysis"""

    mock_section = {
        'header': 'Brief',
        'content': [{'fieldName': 'Decision', 'value': ['the quick brown fox jumps over the lazy dog.']},
                    {'fieldName': 'Nominator', 'value': ['Lorem ipsum dolor']}]
    }

    mock_repositories["analysis"].collection.find_one.return_value = cpam0047_analysis_json
    response = client.post(
        "/analysis/CPAM0047/sections?row_type=text",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={'updated_section': json.dumps(mock_section)}
    )

    assert response.status_code == 201
    mock_repositories["analysis"].collection.update_one.assert_called()


def test_attach_image_to_pedigree_section(client, mock_access_token, mock_repositories):
    """ Testing attaching an image to the Pedigree section of an analysis """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0112.json")

    new_image_id = "633afb87fb250a6ea1569555"
    expected = read_test_fixture("analysis-CPAM0112.json")
    for section in expected["sections"]:
        if section["header"] == "Pedigree":
            for content in section["content"]:
                if content["type"] == "images-dataset":
                    content["value"].append({"file_id": new_image_id})
    mock_repositories['analysis'].collection.find_one_and_update.return_value = expected
    mock_repositories['bucket'].bucket.put.return_value = new_image_id

    mock_section = {'header': 'Pedigree', 'content': [{'fieldName': 'Pedigree'}]}

    section_image_filepath = fixture_filepath('pedigree-fake.jpg')
    with open(section_image_filepath, "rb") as phenotips_file:
        response = client.post(
            "/analysis/CPAM0112/sections?row_type=image",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"upload_file": ("pedigree-fake.jpg", phenotips_file)},
            data=({"updated_section": json.dumps(mock_section)})
        )

        phenotips_file.close()

    assert response.status_code == 201

    returned_sections = TypeAdapter(List[Section]).validate_json(response.content)
    pedigree_section = next((section for section in returned_sections if section.header == "Pedigree"), None)
    actual_updated_field = next((field for field in pedigree_section.content if field['field'] == "Pedigree"), None)
    assert actual_updated_field["value"] == [{'file_id': new_image_id}]


def test_update_existing_pedigree_section_image(client, mock_access_token, mock_repositories):
    """ Testing the update pedigree attachment endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    mock_repositories['bucket'].bucket.put.return_value = "633afb87fb250a6ea1569555"
    mock_analysis = read_test_fixture("analysis-CPAM0002.json")
    mock_repositories["analysis"].collection.find_one_and_update.return_value = mock_analysis

    # Need to send the file as raw binary instead of the processed content
    section_image_filepath = fixture_filepath('pedigree-fake.jpg')
    with open(section_image_filepath, "rb") as image_file:
        response = client.put(
            "/analysis/CPAM0002/section/update/633afb87fb250a6ea1569555",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"upload_file": ("pedigree-fake.jpg", image_file)},
            data=({"section_name": "Pedigree", "field_name": "Pedigree"})
        )
        image_file.close()

    expected = {'section': 'Pedigree', 'field': 'Pedigree', 'image_id': '633afb87fb250a6ea1569555'}

    assert expected == response.json()
    assert response.status_code == 200


def test_remove_existing_pedigree_section_image(client, mock_access_token, mock_repositories):
    """ Tests removing an existing image from the pedigree section of CPAM0002 """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    mock_repositories["bucket"].bucket.delete.return_value = None

    response = client.request(
        'DELETE',
        "/analysis/CPAM0002/section/remove/63505be22888347cf1c275db",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"section_name": "Pedigree", "field_name": "Pedigree"},
    )

    mock_repositories["bucket"].bucket.delete.assert_called_with(ObjectId("63505be22888347cf1c275db"))

    assert response.status_code == 200
