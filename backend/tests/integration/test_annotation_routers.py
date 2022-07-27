"""Routes dedicated for annotation within the system"""
from unittest.mock import patch
from fastapi import BackgroundTasks

from src.annotation import AnnotationService

from ..test_utils import read_database_fixture


def test_queue_annotations_for_sample(client, database_collections, mock_annotation_queue):
    """Testing that the correct number of analyses were returned and in the right order"""
    analysis_collection_json = read_database_fixture("analyses.json")
    database_collections['analysis'].collection.find.return_value = analysis_collection_json
    database_collections['analysis'].collection.find_one.return_value = next(
        (analysis for analysis in analysis_collection_json if analysis['name'] == "CPAM0002"), None)
    database_collections['annotation'].collection.find.return_value = read_database_fixture("dataset-sources.json")
    database_collections['genomic_unit'].collection.find.return_value = read_database_fixture(
        "genomic-units-collection.json")

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = client.post("/annotate/CPAM0002")
        assert response.status_code == 202
        assert mock_annotation_queue.put.call_count == 29
        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks,
            mock_annotation_queue,
            database_collections['genomic_unit']
        )
