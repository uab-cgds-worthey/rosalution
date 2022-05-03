import pytest

from src.core.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.enums import GenomicUnitType

def test_get_units_to_annotate(analysis):
    unitsToAnnotate = analysis.unitsToAnnotate()
    print(unitsToAnnotate)
    print('called annotate')
    assert len(unitsToAnnotate) == 4

def test_get_genes_in_units_to_annotate(analysis):
    unitsToAnnotate = analysis.unitsToAnnotate()
    genes = list(filter(lambda x: GenomicUnitType.GENE == x['type'], unitsToAnnotate))
    gene_names = list(map(lambda x: x['unit'], genes))
    assert len(gene_names) == 2
    assert 'VMA21' in gene_names
    assert 'DMD' in gene_names

def test_get_variants_in_units_to_annotate(analysis):
    unitsToAnnotate = analysis.unitsToAnnotate()
    variants = list(filter(lambda x: GenomicUnitType.HGVS_VARIANT == x['type'], unitsToAnnotate))
    variant_names = list(map(lambda x: x['unit'], variants))
    assert len(variant_names) == 1
    assert 'NM_001017980.3:c.164G>T' in variant_names

def test_get_transcripts_in_units_to_annotate(analysis):
    unitsToAnnotate = analysis.unitsToAnnotate()
    transcripts = list(filter(lambda x: GenomicUnitType.TRANSCRIPT == x['type'], unitsToAnnotate))
    transcript_names = list(map(lambda x: x['unit'], transcripts))
    assert len(transcript_names) == 1
    assert 'NM_001017980.3' in transcript_names

@pytest.fixture
def analysis_collection():
  return AnalysisCollection()

@pytest.fixture
def analysis(analysis_collection):
  analysisJson = analysis_collection.find_by_name('CPAM0002')
  return Analysis(**analysisJson)