# pylint: disable=duplicate-code
"""Testing endpoints for adding/updating/removing omic units to an analysis."""
from unittest.mock import patch

import json
from urllib import response
import pytest

from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService


@pytest.mark.usefixtures("mock_security_get_project_authorization")
def test_adding_and_annotating_new_omic_unit_to_analysis( # pylint: disable=too-many-arguments
      client,
      mock_access_token,
      mock_repositories,
      successfully_added_genomic_units,
      mock_annotation_queue,
      annotations_config_collection_json,
      genomic_units_collection_json):
    """Test adding and annotating an added omic unit to the analysis"""

    new_genomic_unit = {
        'transcript': "NM_004972.3",
        'gene': "JAK2",
        'cdna': "c.1694G>C",
        'protein': "p.Arg565Thr",
        'reason_of_interest': ["Find this variant interesting to explore."],
    }

    mock_repositories["analysis"].collection.find_one_and_update.return_value = successfully_added_genomic_units
    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['genomic_unit'].collection.find.return_value = genomic_units_collection_json

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = client.post(
            "/analysis/CPAM0002/genomic_unit",
            headers={"Authorization": "Bearer " + mock_access_token},
            content=json.dumps(new_genomic_unit)
        )

        assert mock_annotation_queue.put.call_count == 9

        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['genomic_unit'],
            mock_repositories['analysis']
        )

    assert response.status_code == 200
    actual_genomic_units = json.loads(response.text)
    assert len(actual_genomic_units) == 2

@pytest.mark.usefixtures("mock_security_get_project_authorization")
def test_editing_manual_omic_unit_in_analysis(
      client,
      mock_access_token,
      mock_repositories,
      successfully_added_genomic_units):
    """Test editing a manually added omic unit in the analysis"""

    updated_genomic_unit = {
        'reason_of_interest': ["Unit Was Edited.", "Additional reason added."],
    }

    mock_repositories["analysis"].collection.find_one_and_update.return_value = successfully_added_genomic_units

    response = client.put(
        "/analysis/CPAM0002/genomic_unit/JAK2/NM_004972.3:c.1694G>C",
        headers={"Authorization": "Bearer " + mock_access_token},
        content=json.dumps(updated_genomic_unit)
    )

    actual_calls = mock_repositories["analysis"].collection.find_one_and_update.call_args.args
    assert actual_calls[1]['$set'] == {
        'genomic_units.$[unit].variants.$[variant].case': [
            {"field": "Reason of Interest", "value": ["Unit Was Edited.", "Additional reason added."]}
        ]
    }
    assert response.status_code == 200
    actual_genomic_units = json.loads(response.text)
    assert len(actual_genomic_units) == 2

@pytest.mark.usefixtures("mock_security_get_project_authorization")
def test_successfully_deleting_manual_omic_unit_in_analysis(
      client,
      mock_access_token,
      mock_repositories,
      cpam0002_analysis_json
    ):
    """Test deleting a manually added omic unit in the analysis"""

    mock_repositories["analysis"].collection.count_documents.return_value = 1
    mock_repositories["analysis"].collection.find_one.return_value = cpam0002_analysis_json
    
    response = client.delete(
        "/analysis/CPAM0002/genomic_unit/JAK2/NM_004972.3:c.1694G>C",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert mock_repositories["analysis"].collection.update_one.call_count == 2

    assert response.status_code == 200

@pytest.mark.usefixtures("mock_security_get_project_authorization")
def test_deleting_non_manual_omic_unit_in_analysis(client,mock_access_token,mock_repositories):
    """Test deleting a non-manually added omic unit in the analysis, which should raise an HTTP 405 Method Not Allowed error"""
    mock_repositories["analysis"].collection.count_documents.return_value = 0
    
    response = client.delete(
        "/analysis/CPAM0002/genomic_unit/VMA21/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert mock_repositories["analysis"].collection.update_one.call_count == 0
    assert response.status_code == 405


@pytest.fixture(name="successfully_added_genomic_units")
def fixture_success_adding_genomic_units():
    """Fixture for updated analysis with added genomic unit"""
    return {
        "_id": "fake-mongo-object-id",
        "name": 'CPAM0002',
        "description": 'Vacuolar myopathy with autophagy, X-linked vacuolar myopathy with autophagy',
        "project_id": {"$oid": "695d5b157709ebcd1c7325c1"},
        "project_name": "CPAM",
        "nominated_by": 'Dr. Person One',
        "genomic_units": [{
            "gene": 'VMA21', "transcripts": [{"transcript": 'NM_001017980.3'}], "variants": [{
                "hgvs_variant": 'NM_001017980.3:c.164G>T', "c_dot": 'c.164G>T', "p_dot": 'p.Gly55Val', "build": 'hg19',
                'case': [{"field": 'Evidence', "value": ['PVS1', 'PM2']}]
            }]
        }, {
            "gene": 'JAK2', "transcripts": [{"transcript": 'NM_004972.3'},], "variants": [{
                "hgvs_variant": 'NM_004972.3:c.1694G>C', "c_dot": 'c.1694G>C', "p_dot": 'p.Arg565Thr',
                "build": 'GRCh38',
                'case': [{"field": 'Reason of Interest', "value": ['Find this variant interesting to explore.']}]
            },]
        }],
    }
