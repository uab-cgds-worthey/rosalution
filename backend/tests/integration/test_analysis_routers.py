"""Analysis Routes Integration test"""

import json
import datetime

from unittest.mock import patch
from bson import ObjectId

import pytest
from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService

from ..test_utils import fixture_filepath, read_database_fixture, read_test_fixture


def test_get_analyses(client, mock_access_token, mock_repositories):
    """Testing that the correct number of analyses were returned and in the right order"""
    mock_repositories['analysis'].collection.find.return_value = read_database_fixture("analyses.json")

    response = client.get("/analysis", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 6
    assert response.json()[2]["name"] == "CPAM0047"


def test_get_analysis_summary(client, mock_access_token, mock_repositories):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    mock_repositories['analysis'].collection.find.return_value = read_test_fixture(
        "analyses-summary-db-query-result.json"
    )
    response = client.get("/analysis/summary", headers={"Authorization": "Bearer " + mock_access_token})
    assert len(response.json()) == 5


def test_get_summary_by_name(client, mock_access_token, mock_repositories):
    """Tests the summary_by_name endpoint"""
    mock_repositories['analysis'].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")

    response = client.get("/analysis/CPAM0002/summary", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert response.json()["name"] == "CPAM0002"


def test_import_analysis_with_phenotips_json(
    client,
    mock_access_token,
    mock_repositories,
    mock_annotation_queue,
    mock_security_get_current_user,  # pylint: disable=unused-argument
):
    """ Testing if the create analysis function works with file upload """
    mock_repositories["analysis"].collection.insert_one.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = None
    mock_repositories["genomic_unit"].collection.find_one.return_value = None
    mock_repositories['annotation_config'].collection.find.return_value = read_database_fixture(
        "annotations-config.json"
    )
    mock_repositories['genomic_unit'].collection.find.return_value = read_database_fixture("genomic-units.json")

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        analysis_import_json_filepath = fixture_filepath('phenotips-import.json')
        with open(analysis_import_json_filepath, "rb") as phenotips_file:
            response = client.post(
                "/analysis",
                headers={"Authorization": "Bearer " + mock_access_token},
                files={"phenotips_file": ("phenotips-import.json", phenotips_file.read())}
            )

            phenotips_file.close()

            assert mock_annotation_queue.put.call_count == 50

            mock_background_add_task.assert_called_once_with(
                AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['genomic_unit']
            )

    assert response.status_code == 200
    response_data = json.loads(response.text)
    assert response_data['latest_status'] == "Preparation"
    assert response_data['timeline'][0]['username'] == 'johndoe'


def test_update_analysis_sections(client, mock_access_token, mock_repositories, cpam0047_analysis_json):
    """Testing if the update analysis endpoint updates an existing analysis"""

    mock_updated_sections = [{
        "header": "Brief",
        "content": [{"fieldName": "Reason", "value": ["the quick brown fox jumps over the lazy dog."]},
                    {"fieldName": "Nominated", "value": ["Lorem ipsum dolor"]}]
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


# We will come back to this later:
# def test_download(client, mock_access_token, mock_repositories):
#     """ Testing the file download endpoint, does it return a file stream """
#     mock_repositories['bucket'].bucket.find_one.return_value =   {
#         "filename": '4d4331dc8a3006e068ced8f0057dde50.jpg',
#         "chunkSize": 261120,
#     }

#     mock_repositories.['bucket'].bucket.GridOut

#     response = client.get(
#         "/download/testfile.png",
#         headers={"Authorization": "Bearer " + mock_access_token}
#     )

#     assert response

def test_attaching_supporting_evidence_link_to_analysis(
    client, mock_access_token, mock_repositories, cpam0002_analysis_json
):
    """Testing if the supporting evidence gets added to the analysis"""

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['supporting_evidence_files'].append(query['$push']['supporting_evidence_files'])
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis

    mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

    response = client.post(
        "/analysis/CPAM0002/attach/link",
        headers={"Authorization": "Bearer " + mock_access_token},
        data=({
            "link_name": "Interesting Article",
            "link": "http://sites.uab.edu/cgds/",
            "comments": "Serious Things in here",
        })
    )

    result = json.loads(response.text)
    assert len(result['supporting_evidence_files']) == 1
    assert response.status_code == 200

def test_get_genomic_units_success(client, mock_access_token, mock_repositories, genomic_unit_success_response):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200
    assert response.json() == genomic_unit_success_response

def test_get_genomic_units_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404

def test_get_genomic_units_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the get genomic units endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json"
                                                                                      ).pop("genomic_units")

    response = client.get("/analysis/CPAM0002/genomic_units", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 404

def test_remove_supporting_evidence_file(client, mock_access_token, mock_repositories):
    """ Testing the remove attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = True
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.delete(
        "/analysis/CPAM0002/attachment/633afb87fb250a6ea1569555/remove",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    mock_repositories['bucket'].bucket.exists.assert_called()
    mock_repositories['bucket'].bucket.delete.assert_called()
    assert response.status_code == 200
    assert response.json() == expected

def test_remove_supporting_evidence_link(client, mock_access_token, mock_repositories, supporting_evidence_link_json):
    """ Testing the remove attachment endpoint """
    mock_repositories["bucket"].bucket.exists.return_value = False
    mock_repositories["analysis"].collection.find_one.return_value = supporting_evidence_link_json
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.delete(
        "/analysis/CPAM0002/attachment/a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8/remove",
        headers={"Authorization": "Bearer " + mock_access_token}
    )

    assert response.status_code == 200
    assert response.json() == expected

# def test_attach_image_to_pedigree_section(client, mock_access_token, mock_repositories):
#     """ Testing attaching an image to the Pedigree section of an analysis """
#     mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0112.json")
#     expected = read_test_fixture("analysis-CPAM0112.json")
#     for section in expected["sections"]:
#         if section["header"] == "Pedigree":
#             for content in section["content"]:
#                 if content["type"] == "images-dataset":
#                     content["value"].append({"file_id": "633afb87fb250a6ea1569555"})
#     mock_repositories['analysis'].collection.find_one_and_update.return_value = expected
#     mock_repositories['bucket'].bucket.put.return_value = "633afb87fb250a6ea1569555"

#     section_image_filepath = fixture_filepath('pedigree-fake.jpg')
#     with open(section_image_filepath, "rb") as phenotips_file:
#         response = client.post(
#             "/analysis/CPAM0112/section/attach/image",
#             headers={"Authorization": "Bearer " + mock_access_token},
#             files={"upload_file": ("pedigree-fake.jpg", phenotips_file)},
#             data=({"section_name": "Pedigree", "field_name": "Pedigree"})
#         )

#         phenotips_file.close()

#     assert response.status_code == 201
#     mock_repositories["analysis"].collection.find_one_and_update.assert_called_with({"name": "CPAM0112"},
#                                                                                     {"$set": expected})

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

def test_attach_third_party_link(client, mock_access_token, mock_repositories):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["third_party_links"] = [{"type": "monday_com", "link": "https://monday.com"}]
    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected
    response = client.put(
        "/analysis/CPAM0002/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "https://monday.com"}
    )

    assert response.status_code == 200
    assert response.json()["third_party_links"] == [{"type": "monday_com", "link": "https://monday.com"}]

def test_attach_third_party_link_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None
    response = client.put(
        "/analysis/CPAM0002/attach/monday_com",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 409

def test_attach_third_party_link_invalid_enum(client, mock_access_token, mock_repositories):
    """ Testing the attach third party link endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    response = client.put(
        "/analysis/CPAM0002/attach/BAD_ENUM",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={"link": "monday.com"}
    )

    assert response.status_code == 422

def test_mark_ready(client, mock_access_token, mock_repositories):
    """ Testing the update analysis event endpoint """
    staging_analysis_timeline = read_test_fixture("analysis-CPAM0002.json")
    staging_analysis_timeline["timeline"] = [{
        'event': 'create',
        'timestamp': datetime.datetime(2022, 11, 10, 16, 52, 43, 910000),
        'username': 'johndoe',
    }]
    mock_repositories["analysis"].collection.find_one.return_value = staging_analysis_timeline

    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["timeline"] = [
        {
            'event': 'create',
            'timestamp': '2022-11-10T16:52:43.910000',
            'username': 'johndoe',
        },
        {
            'event': 'ready',
            'timestamp': '2022-11-10T16:52:52.301003',
            'username': 'johndoe',
        },
    ]

    mock_repositories["analysis"].collection.find_one_and_update.return_value = expected

    response = client.put("/analysis/CPAM0002/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 200

def test_mark_ready_analysis_does_not_exist(client, mock_access_token, mock_repositories):
    """ Testing the mark ready endpoint """
    mock_repositories["analysis"].collection.find_one.return_value = None

    response = client.put("/analysis/CPAM2222/event/ready", headers={"Authorization": "Bearer " + mock_access_token})

    assert response.status_code == 409
    assert response.json() == {'detail': 'Analysis with name CPAM2222 does not exist.'}

@pytest.fixture(name="analysis_updates_json")
def fixture_analysis_updates_json():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return read_test_fixture("analysis-update.json")

@pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")

@pytest.fixture(name="genomic_unit_success_response")
def fixture_genomic_unit_success_response():
    """The JSON that is being sent from a client to the endpoint with updates in it"""
    return {
        "genes": {"VMA21": ["NM_001017980.3:c.164G>T(p.Gly55Val)"], "DMD": []},
        "variants": ["NM_001017980.3:c.164G>T(p.Gly55Val)"]
    }

@pytest.fixture(name="supporting_evidence_link_json")
def fixture_supporting_evidence_link_json():
    """The JSON that is being returned to the endpoint with a link in the supporting evidence"""
    setup_return_value = read_test_fixture("analysis-CPAM0002.json")
    setup_return_value["supporting_evidence_files"] = [{
        "name": "this is a silly link name", "data": "http://local.rosalution.cgds/rosalution/api/docs",
        "attachment_id": "a1ea5c7e-1c13-4d14-a3d7-297f39f11ba8", "type": "link", "comments": "hello link world"
    }]
    return setup_return_value

@pytest.fixture(name="empty_pedigree")
def fixture_empty_pedigree():
    """returns an analysis with an empty pedigree"""
    return read_test_fixture("empty-pedigree.json")
