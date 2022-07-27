"""Tests to verify Analysis operations"""
import pytest

from src.enums import GenomicUnitType


def test_get_units_to_annotate(units_to_annotate):
    """tests the number of units to annotate"""
    assert len(units_to_annotate) == 4


def test_get_genes_in_units_to_annotate(units_to_annotate):
    """Tests the list of genes returned"""
    genes = list(filter(lambda x: GenomicUnitType.GENE == x["type"], units_to_annotate))
    gene_names = list(map(lambda x: x["unit"], genes))
    assert len(gene_names) == 2
    assert "VMA21" in gene_names
    assert "DMD" in gene_names


def test_get_variants_in_units_to_annotate(units_to_annotate):
    """Tests the list of variants returned"""
    variants = list(filter(lambda x: GenomicUnitType.HGVS_VARIANT == x["type"], units_to_annotate))
    variant_names = list(map(lambda x: x["unit"], variants))
    assert len(variant_names) == 1
    assert "NM_001017980.3:c.164G>T" in variant_names


def test_get_transcripts_in_units_to_annotate(units_to_annotate):
    """Tests the list of transcripts returned"""
    transcripts = list(filter(lambda x: GenomicUnitType.TRANSCRIPT == x["type"], units_to_annotate))
    transcript_names = list(map(lambda x: x["unit"], transcripts))
    assert len(transcript_names) == 1
    assert "NM_001017980.3" in transcript_names


@pytest.fixture(name="units_to_annotate")
def fixture_units_to_annotate(cpam0002_analysis):
    """Fixture for the units to annotate for the CPAM0002 Analysis"""
    return cpam0002_analysis.units_to_annotate()
