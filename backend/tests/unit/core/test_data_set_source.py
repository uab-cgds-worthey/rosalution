import pytest
from src.core.data_set_source import DataSetSource
from src.enums import GenomicUnitType

from src.core.analysis import Analysis

def test_data_set_base_url(transcript_id_dataset, cpam0046_hgvs_genomic_unit):
    dataset = DataSetSource(**transcript_id_dataset)
    actual = dataset.base_url(cpam0046_hgvs_genomic_unit)
    print(actual)
    assert actual == "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;"

@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset(annotation_collection):
    """
    Returns the dict of the transcript_id dataset
    """
    return annotation_collection.find_by_data_set('transcript_id')

@pytest.fixture(name="cpam0046_hgvs_genomic_unit")
def fixture_cpam0046_hgvs_genomic_unit(cpam0046_analysis):
    """
    Returns the HGVS variant within the CPAM0046 analysis.
    """
    genomic_units = cpam0046_analysis.units_to_annotate()
    unit = {}
    for genomic_unit in genomic_units:
        if genomic_unit['type'] == GenomicUnitType.HGVS_VARIANT:
          unit = genomic_unit
    
    return unit  


@pytest.fixture(name='cpam0046_analysis')
def fixture_cpam0046_analysis(analysis_collection):
    """Returns the Analysis for CPAM0046 to verify creating annotation tasks"""
    analysis_json = analysis_collection.find_by_name('CPAM0046')
    return Analysis(**analysis_json)
