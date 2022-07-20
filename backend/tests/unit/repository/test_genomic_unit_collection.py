""" Manages the genomic unit collection. Including reading, writing, fetching various genomic units. """

import pytest

from unittest.mock import Mock

from src.enums import GenomicUnitType
from src.repository.genomic_unit_collection import GenomicUnitCollection

def test_write_genomic_units_to_file(
        genomic_unit_collection, hgvs_variant_genomic_unit, genomic_unit_annotation_fixture
    ):
    
    GenomicUnitCollection.write_fixture = Mock()

    genomic_unit_collection.update_genomic_unit(hgvs_variant_genomic_unit, genomic_unit_annotation_fixture)

    assert GenomicUnitCollection.write_fixture.call_count == 1

@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection():
    return GenomicUnitCollection()

@pytest.fixture(name="genomic_unit_annotation_fixture")
def fixture_genomic_unit_annotation():
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
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
    }