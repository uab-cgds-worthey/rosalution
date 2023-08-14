"""Tests to verify dataset configuration is returned"""
import pytest

from src.enums import GenomicUnitType


def test_get_datasets_configuration_by_type(annotation_collection):
    """Tests getting the datasets for the provided types of genomic units"""
    types = set({GenomicUnitType.GENE, GenomicUnitType.HGVS_VARIANT})
    datasets = annotation_collection.datasets_to_annotate_by_type(types)
    assert len(datasets) == 50


def test_get_datasets_to_annotate_for_units(annotation_collection, genomic_units_for_annotation):
    """Tests if the configuration for datasets is return as expected"""
    actual_configuration = annotation_collection.datasets_to_annotate_for_units(genomic_units_for_annotation)
    assert len(actual_configuration["gene"]) == 40
    assert len(actual_configuration["hgvs_variant"]) == 10


@pytest.fixture(name="genomic_units_for_annotation")
def fixture_genomic_units():
    """Fixture for list of genomic units"""
    return [
        {"type": GenomicUnitType.GENE, "unit": "DMD"},
        {"type": GenomicUnitType.GENE, "unit": "VMA21"},
        {"type": GenomicUnitType.HGVS_VARIANT, "unit": "NM_170707.3:c.745C>T"},
    ]


@pytest.fixture(name="hgvs_genomic_unit_for_annotation")
def fixture_hgvs_genomic_unit():
    """ Single HGVS genomic unit fixture """
    return {"type": GenomicUnitType.HGVS_VARIANT, "unit": "NM_001017980.3:c.164G>T"}
