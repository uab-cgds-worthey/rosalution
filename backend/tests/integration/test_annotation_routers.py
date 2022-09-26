"""Routes dedicated for annotation within the system"""
from unittest.mock import patch
from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService

from ..test_utils import read_database_fixture, read_test_fixture


def test_queue_annotations_for_sample(client, database_collections, mock_annotation_queue):
    """Testing that the correct number of analyses were returned and in the right order"""
    analysis_collection_json = read_database_fixture("analyses.json")
    database_collections['analysis'].collection.find.return_value = analysis_collection_json
    database_collections['analysis'].collection.find_one.return_value = next(
        (analysis for analysis in analysis_collection_json if analysis['name'] == "CPAM0002"), None)
    database_collections['annotation_config'].collection.find.return_value = read_database_fixture(
        "annotations-config.json")
    database_collections['genomic_unit'].collection.find.return_value = read_database_fixture(
        "genomic-units.json")

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = client.post("/annotate/CPAM0002")
        assert response.status_code == 202
        assert mock_annotation_queue.put.call_count == 29
        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks,
            mock_annotation_queue,
            database_collections['genomic_unit']
        )

def test_get_annotations_by_gene(client, mock_access_token, database_collections):
    """Testing that the annotations by gene endpoint returns the annotations correctly"""

    gene_annotations_fixture = read_test_fixture("annotations-VMA21.json")
    database_collections['genomic_unit'].collection.find_one.return_value = gene_annotations_fixture
    response = client.get("annotate/gene/VMA21", headers={"Authorization": "Bearer " + mock_access_token})

    assert len(response.json()) == 2

def test_get_annotations_by_hgvs_variant(client, mock_access_token, database_collections):
    """Testing that the annotations by HGVS variant endpoint returns the annotations correctly"""

    variant_annotations_fixture = read_test_fixture("annotations-HGVS-Variant.json")
    database_collections['genomic_unit'].collection.find_one.return_value = variant_annotations_fixture
    response = client.get("annotate/hgvsVariant/NM_001017980.3:c.164G>T",
        headers={"Authorization": "Bearer " + mock_access_token})

    assert len(response.json()) == 2
