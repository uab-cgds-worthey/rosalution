"""Testing endpoints for adding/updating/removing document and link attachments to an analysis."""

import json
from typing import List
import pytest

from pydantic import TypeAdapter

from src.models.analysis import Section

from ..test_utils import assets_fixture_filepath


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_update_analysis_sections(client, mock_access_token):
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

    response = await client.post(
        "/analysis/CPAM0047/sections/batch",
        headers={"Authorization": "Bearer " + mock_access_token},
        json=mock_updated_sections
    )

    assert response.status_code == 200
    # mock_repositories["analysis"].collection.update_one.assert_called()


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_update_individual_section_text_fields(client, mock_access_token):
    """Testing if the update analysis endpoint updates an existing analysis"""

    mock_section = {
        'header': 'Brief',
        'content': [{'fieldName': 'Decision', 'value': ['the quick brown fox jumps over the lazy dog.']},
                    {'fieldName': 'Nominator', 'value': ['Lorem ipsum dolor']}]
    }

    # mock_repositories["analysis"].collection.find_one.return_value = cpam0047_analysis_json
    response = await client.post(
        "/analysis/CPAM0047/sections?row_type=text",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={'updated_section': json.dumps(mock_section)}
    )

    assert response.status_code == 201
    # mock_repositories["analysis"].collection.update_one.assert_called()


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_attach_image_to_pedigree_section(client, mock_access_token):
    """ Testing attaching an image to the Pedigree section of an analysis """

    mock_section = {'header': 'Pedigree', 'content': [{'fieldName': 'Pedigree'}]}

    section_image_filepath = assets_fixture_filepath('pedigree-fake.jpg')
    with open(section_image_filepath, "rb") as phenotips_file:
        response = await client.post(
            "/analysis/CPAM0047/sections?row_type=image",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"upload_file": ("pedigree-fake.jpg", phenotips_file)},
            data=({"updated_section": json.dumps(mock_section)})
        )

        phenotips_file.close()

    assert response.status_code == 201

    returned_sections = TypeAdapter(List[Section]).validate_json(response.content)
    pedigree_section = next((section for section in returned_sections if section.header == "Pedigree"), None)
    assert pedigree_section is not None

    actual_updated_field_values = next(
        (field["value"] for field in pedigree_section.content if field['field'] == "Pedigree"), None
    )

    for image_files in actual_updated_field_values:
        assert "file_id" in image_files


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_update_existing_pedigree_section_image(client, mock_access_token):
    """ Testing the update pedigree attachment endpoint """
    mock_section = {'header': 'Pedigree', 'content': [{'fieldName': 'Pedigree'}]}

    # Need to send the file as raw binary instead of the processed content
    section_image_filepath = assets_fixture_filepath('pedigree-fake.jpg')
    with open(section_image_filepath, "rb") as image_file:
        response = await client.put(
            "/analysis/CPAM0002/sections/63505be22888347cf1c275db?row_type=image",
            headers={"Authorization": "Bearer " + mock_access_token},
            files={"upload_file": ("pedigree-fake.jpg", image_file)},
            data=({"updated_section": json.dumps(mock_section)})
        )
        image_file.close()

    assert response.status_code == 200


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_remove_existing_pedigree_section_image(client, mock_access_token):
    """ Tests removing an existing image from the pedigree section of CPAM0002 """
    pedigree_image_id = "63505be22888347cf1c275db"

    response = await client.delete(
        "/analysis/CPAM0002/sections/63505be22888347cf1c275db",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200
    # mock_repositories["bucket"].bucket.delete.assert_called_with(ObjectId(pedigree_image_id))
