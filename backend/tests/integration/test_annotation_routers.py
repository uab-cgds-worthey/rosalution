"""Routes dedicated for annotation within the system"""
from unittest.mock import patch
from fastapi import BackgroundTasks

from src.annotation import AnnotationService

def test_queue_annotations_for_sample(client, database_collections, mock_annotation_queue):
    """Testing that the correct number of analyses were returned and in the right order"""
    # Future Database Mock Example
    # mock_database_collections.db['analysis'].find()
    # mock_database_collections.db['analysis'].find.return_value = JSON Fixture
    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:
        response = client.post("/annotate/CPAM0002")
        assert response.status_code == 202
        assert mock_annotation_queue.put.call_count == 29   
        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks,
            database_collections['genomic_unit'],
            mock_annotation_queue
        )