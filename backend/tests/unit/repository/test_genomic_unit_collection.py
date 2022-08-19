""" Manages the genomic unit collection. Including reading, writing, fetching various genomic units. """
from unittest.mock import Mock
import pytest

from bson import ObjectId

from src.enums import GenomicUnitType
from src.repository.genomic_unit_collection import GenomicUnitCollection

from ...test_utils import mock_mongo_collection, read_database_fixture

def test_find_genomic_units(genomic_unit_collection):
    """ Gets all the genomic units from the genomic unit collection """
    all_genomic_units = genomic_unit_collection.all()
    assert len(all_genomic_units) == 3

def test_find_genomic_unit_with_transcript_id(genomic_unit_collection):
    """
    Verifies that the find_genomic_unit_with_transcript_id function gets called with the correct parameters
    """
    genomic_unit = { 'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT }
    transcript_id = "NM_001363810.1"

    genomic_unit_collection.find_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

    genomic_unit_collection.collection.find_one.assert_called_with(
        {
            "hgvs_variant": "NM_001017980.3:c.164G>T",
            "transcripts.transcript_id": "NM_001363810.1"
        }
    )

def test_update_genomic_unit_with_transcript_id(genomic_unit_collection):
    """
    Verifies that the update_genomic_unit_with_transcript_id function makes the pymongo call with the correct params
    """
    genomic_unit = { 'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT }
    transcript_id = "NM_001363810.1"

    genomic_unit_collection.update_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        { 'hgvs_variant': 'NM_001017980.3:c.164G>T' },
        { '$addToSet': { 'transcripts': { 'transcript_id': 'NM_001363810.1', 'annotations': [] } } }
    )

def test_update_genomic_unit_with_mongo_id(genomic_unit_collection):
    """
    Verifies that the update genomic unit with mongo id function makes the pymongo call with the correct params
    """
    genomic_unit_document = {
        "_id": ObjectId('62fbfa5f616a9799131174c8'),
        "hgvs_variant": "NM_001017980.3:c.164G>T",
        "transcripts": [],
        "annotations": {}
    }

    genomic_unit_collection.update_genomic_unit_with_mongo_id(genomic_unit_document)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        { '_id': ObjectId('62fbfa5f616a9799131174c8') },
        { '$set': genomic_unit_document }
    )

def test_annotate_transcript_genomic_unit(genomic_unit_collection):
    """ Verifies that a transcript annotates a genomic unit properly """
    genomic_unit = { 'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT }
    transcript_annotation_unit = {
        "data_set": "SIFT Prediction",
        "data_source": "Ensembl",
        "version": "",
        "value": "deleterious",
        "transcript_id": "NM_001017980.4"
    }

    genomic_unit_collection.find_genomic_unit_with_transcript_id = Mock(return_value={
        "_id": ObjectId("62fbfa5f616a9799131174ca"),
        "hgvs_variant": "NM_001017980.3:c.164G>T",
        "transcripts": [
            {
                'transcript_id': 'NM_001363810.1',
                'annotations': []
            }
        ],
        "annotations": {}
    })

    genomic_unit_collection.annotate_genomic_unit(genomic_unit, transcript_annotation_unit)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        {'_id': ObjectId("62fbfa5f616a9799131174ca")},
        {
            '$set': {
                "_id": ObjectId("62fbfa5f616a9799131174ca"),
                "hgvs_variant": "NM_001017980.3:c.164G>T",
                "transcripts": [
                    {
                        'transcript_id': 'NM_001363810.1',
                        'annotations': []
                    }
                ],
                "annotations": {}
            }
        }
    )

@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection(genomic_units_json):
    """ Returns a genomic unit collection """

    mock_collection = mock_mongo_collection()
    mock_collection.find.return_value = genomic_units_json

    return GenomicUnitCollection(mock_collection)

@pytest.fixture(name="genomic_units_json")
def fixture_genomic_units_json():
    """ Returns the JSON for the genomic units used to seed the MongoDB database """
    return read_database_fixture("genomic-units.json")
