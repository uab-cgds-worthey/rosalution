"""Tests to verify Analysis operations"""
import pytest

from src.core.analysis import Analysis
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


@pytest.fixture(name="analysis")
def fixture_analysis(analysis_collection):
    """Fixture for the CPAM0002 Analysis"""
    analysis_json = analysis_collection.find_by_name("CPAM0002")
    return Analysis(**analysis_json)


@pytest.fixture(name="units_to_annotate")
def fixture_units_to_annotate(analysis):
    """Fixture for the units to annotate for the CPAM0002 Analysis"""
    return analysis.units_to_annotate()
