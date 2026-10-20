# pylint: disable=duplicate-code
"""Testing endpoints for adding/updating/removing omic units to an analysis."""
from unittest.mock import patch

import json
import pytest

from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_adding_and_annotating_new_omic_unit_to_analysis(
    client, mock_access_token, mock_annotation_queue, mock_settings
):
    """Test adding and annotating an added omic unit to the analysis"""

    new_genomic_unit = {
        'transcript': "NM_004972.3",
        'gene': "JAK2",
        'cdna': "c.1694G>C",
        'protein': "p.Arg565Thr",
        'reason_of_interest': ["Find this variant interesting to explore."],
    }

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = await client.post(
            "/analysis/CPAM0002/genomic_unit",
            headers={"Authorization": "Bearer " + mock_access_token, "Content-Type": "application/json"},
            content=json.dumps(new_genomic_unit)
        )

        assert mock_annotation_queue.put.call_count == 9

        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks, mock_annotation_queue, mock_settings
        )

        assert response.status_code == 200
        actual_genomic_units = json.loads(response.text)
        assert len(actual_genomic_units) == 2


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_editing_manual_omic_unit_in_analysis(client, mock_access_token):
    """Test editing a manually added omic unit in the analysis"""

    updated_genomic_unit = {
        'reason_of_interest': ["Unit Was Edited.", "Additional reason added."],
    }

    response = await client.put(
        "/analysis/CPAM0047/genomic_unit/JAK2/NM_004972.3:c.1694G>C",
        headers={"Authorization": "Bearer " + mock_access_token, "Content-Type": "application/json"},
        content=json.dumps(updated_genomic_unit)
    )

    assert response.status_code == 200
    actual_genomic_units = json.loads(response.text)
    assert len(actual_genomic_units) == 2


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_successfully_deleting_manual_omic_unit_in_analysis(client, mock_access_token):
    """Test deleting a manually added omic unit in the analysis"""

    response = await client.delete(
        "/analysis/CPAM0047/genomic_unit/JAK2/NM_004972.3:c.1694G>C",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert response.status_code == 200
    actual_genomic_units = json.loads(response.text)
    assert len(actual_genomic_units) == 2
    jak2_gene = next((gene for gene in actual_genomic_units if gene["gene"] == "JAK2"), None)
    assert jak2_gene is not None
    assert len(jak2_gene["variants"]) == 0


@pytest.mark.anyio
@pytest.mark.usefixtures("mock_repositories")
@pytest.mark.usefixtures("mock_security_get_project_authorization")
async def test_deleting_non_manual_omic_unit_in_analysis(client, mock_access_token):
    """
    Test deleting an original unit in the analysis resulting in the response returning a
    HTTP 405 Method Not Allowed error.
    """
    response = await client.delete(
        "/analysis/CPAM0002/genomic_unit/VMA21/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token},
    )

    assert response.status_code == 405
