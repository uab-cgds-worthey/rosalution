"""Tests Annotation Tasks and the creation of them"""
from datetime import date
from unittest.mock import Mock, patch

import copy
import subprocess
import pytest
import requests

from src.core.annotation_task import AnnotationTaskFactory, ForgeAnnotationTask, SubprocessAnnotationTask, \
    HttpAnnotationTask, VersionAnnotationTask
from src.enums import GenomicUnitType
from src.core.annotation_unit import AnnotationUnit


@pytest.mark.parametrize(
    "genomic_unit,dataset_name", [('VMA21', 'Entrez Gene Id'), ('NM_001017980.3:c.164G>T', 'ClinVar_Variantion_Id')]
)
def test_annotation_versioning_task_created(genomic_unit, dataset_name, get_annotation_unit):
    """Verifies that the annotation task factory creates the correct version annotation task for the annotation unit"""
    annotation_unit = get_annotation_unit(genomic_unit, dataset_name)
    actual_task = AnnotationTaskFactory.create_version_task(annotation_unit)
    assert isinstance(actual_task, VersionAnnotationTask)


@pytest.mark.parametrize(
    "genomic_unit,dataset_name,expected", [
        ('VMA21', 'Entrez Gene Id', {"rosalution": "rosalution-manifest-00"}),
        ('NM_001017980.3:c.164G>T', 'ClinVar_Variantion_Id', {"rosalution": "rosalution-manifest-00"}),
        ('VMA21', 'Ensembl Gene Id', {"releases": [112]}),
        ('NM_001017980.3:c.164G>T', 'Polyphen Prediction', {"releases": [112]}),
        ('VMA21', 'HPO_NCBI_GENE_ID', {"date": "2024-09-16"}),
        ('LMNA', 'OMIM', {"date": "2024-09-16"}),
    ]
)
def test_process_annotation_versioning_all_types(genomic_unit, dataset_name, expected, get_version_task):
    """Verifies that Version Annotation Tasks process and annotate for all 3 versioning types- date, rest, rosalution"""

    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {"releases": [112]}

    with (patch("requests.get", return_value=mock_response), patch('src.core.annotation_task.date') as mock_date):
        mock_date.today.return_value = date(2024, 9, 16)

        task = get_version_task(genomic_unit, dataset_name)
        actual_version_json = task.annotate()
        assert actual_version_json == expected


@pytest.mark.parametrize(
    "genomic_unit,dataset_name,version_to_extract,expected", [
        ('VMA21', 'Entrez Gene Id', {"rosalution": "rosalution-manifest-00"}, "rosalution-manifest-00"),
        ('VMA21', 'Ensembl Gene Id', {"releases": [112]}, 112),
        ('LMNA', 'OMIM', {"date": "rosalution-manifest-00"}, "rosalution-manifest-00"),
    ]
)
def test_version_extraction(genomic_unit, dataset_name, expected, version_to_extract, get_version_task):
    """ Verifies extraction for datasets for all 3 versioning types - rest, date, rosalution"""
    task = get_version_task(genomic_unit, dataset_name)
    actual_version_extraction = task.extract_version(version_to_extract)
    assert actual_version_extraction == expected


## Fixtures ##


@pytest.fixture(name="get_version_task")
def get_version_annotation_task(get_annotation_unit):
    """creating version task"""

    def _create_version_task(genomic_unit, dataset_name):

        annotation_unit = get_annotation_unit(genomic_unit, dataset_name)

        return VersionAnnotationTask(annotation_unit)

    return _create_version_task

