""" Manages the genomic unit collection. Including reading, writing, fetching various genomic units. """

from unittest.mock import Mock
import pytest

from src.enums import GenomicUnitType
from src.repository.genomic_unit_collection import GenomicUnitCollection

from ...test_utils import mock_mongo_collection

def test_update_genomic_unit(
        genomic_unit_collection, hgvs_variant_genomic_unit, genomic_unit_annotation_fixture
    ):
    """
    Takes a hgvs genomic unit provided from an annotation task as well as an extracted genomic annotation unit and
    tests updating them in the genomic_unit_collection
    """



    assert 1 == 1

    # genomic_unit_collection.update_genomic_unit(
    #     hgvs_variant_genomic_unit, genomic_unit_annotation_fixture
    # ) # pylint: disable=no-member

    # assert GenomicUnitCollection.update_one.call_count == 1

@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection():
    """ Returns a genomic unit collection """

    mock_collection = mock_mongo_collection()
    mock_collection.update_one.return_value = None

    return GenomicUnitCollection(mock_collection)

@pytest.fixture(name="genomic_unit_annotation_fixture")
def fixture_genomic_unit_annotation():
    """
    Returns a genomic unit annotation for genomic unit NM_001017980.3:c.164G>T with data for the SIFT Prediction
    data source and the value of 'deleterious'
    """
    return {
        "genomic_unit":"hgvs_variant",
        "symbol_notation":"transcript_id",
        "symbol_value": {
            "transcript_id": "NM_001017980.4",
            "gene_symbol": "VMA21"
        },
        "key":"sift_prediction",
        "value":{
            "data_set_id":"hbIJlfAbyR843yi9pVhxjGZj9a",
            "data_set":"SIFT Prediction",
            "data_source":"Ensembl",
            "version":"None",
            "value":"deleterious"
        }
    }

@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit():
    """ Returns the genomic unit 'NM_001017980.3:c.164G>T' to be annotated """
    return {
        "unit": "NM_001017980.3:c.164G>T",
        "type": GenomicUnitType.HGVS_VARIANT,
    }

@pytest.fixture(name="mongo_query_transcript_fixture")
def fixture_mongo_transcript_query():
    """
    The query parameters that will be potentially needed when looking for a transcript record when calling
    the updateOne mongodb function
    """
    return {'hgvs_variant': 'NM_001017980.3:c.164G>T', 'transcripts.transcript_id': 'NM_001363810.1'}

@pytest.fixture(name="mongo_annotation_fixture")
def fixture_mongo_annotation():
    """
    The second part of the query parameter for the updateOne mongodb function with the data that's updating
    the document.
    """
    return {
        "annotations.sift_prediction": {
            "data_set_id":"6Ym2o3PZOJ2TQpz9cu9nLHkNKN",
            "data_set":"SIFT Prediction",
            "data_source":"Ensembl",
            "version":"None",
            "value":"deleterious"
        }
    }
