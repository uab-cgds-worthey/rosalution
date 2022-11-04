"""Tests importing the phenotips data"""
import pytest

from src.core.phenotips_importer import PhenotipsImporter

from ...test_utils import read_test_fixture


def test_import_genomic_unit_data_hgvs(phenotips_importer):
    """Tests the format_genomic_unit_data function"""
    data = {"transcript": "NM_001005484.1", "cdna": "c.1036C>T", "reference_genome": "GRCh37"}
    actual = phenotips_importer.import_genomic_unit_collection_data(data, "hgvs")
    assert actual['hgvs_variant'] == "NM_001005484.1:c.1036C>T"
    assert len(actual['transcripts']) == 0
    assert len(actual['annotations']) == 0


def test_import_genomic_unit_data_gene(phenotips_importer):
    """Tests the format_genomic_unit_data function"""
    data = {"gene": "BRCA1"}
    actual = phenotips_importer.import_genomic_unit_collection_data(data, "gene")
    assert actual == {"gene": "BRCA1", "gene_symbol": "BRCA1", "annotations": []}


def test_import_analysis_data(phenotips_importer, exported_phenotips_to_import_json):
    """Tests the import_analyses_data function"""

    variant_data = [{
        "inheritance": "maternal",
        "zygosity": "hemizygous",
        "interpretation": "variant_u_s",
        "transcript": "NM_001017111.3",
        "protein": "p.Gly55Val",
        "cdna": "c.164G>T",
        "reference_genome": "GRCh38",
        "gene": "VMA21",
    }]

    actual = phenotips_importer.import_analysis_data(
        exported_phenotips_to_import_json, variant_data, exported_phenotips_to_import_json["genes"]
    )
    assert actual["name"] == "CPAM0112"
    assert actual["genomic_units"] == [{
        "gene": "VMA21",
        "transcripts": [{"transcript": "NM_001017111.3"}],
        "variants": [{
            "hgvs_variant": "NM_001017111.3:c.164G>T",
            "c_dot": "c.164G>T",
            "p_dot": "p.Gly55Val",
            "build": "GRCh38",
            "case": [
                {"field": "Interpretation", "value": ["variant_u_s"]},
                {"field": "Zygosity", "value": ["hemizygous"]},
                {"field": "Inheritance", "value": ["maternal"]},
            ],
        }],
    }]


def test_format_case_data(phenotips_importer):
    """Tests the format_case_data function"""
    variants = {
        "inheritance": "maternal",
        "zygosity": "hemizygous",
        "interpretation": "variant_u_s",
        "transcript": "NM_001017111.3",
        "cdna": "c.164G>T",
        "reference_genome": "GRCh38",
        "gene": "VMA21",
    }
    actual = phenotips_importer.format_case_data(variants)
    assert actual == [
        {"field": "Interpretation", "value": ["variant_u_s"]},
        {"field": "Zygosity", "value": ["hemizygous"]},
        {"field": "Inheritance", "value": ["maternal"]},
    ]


def test_extracting_hpo_terms(exported_phenotips_to_import_json):
    """Tests if the importer extracts the Phenotips HPO terms into the expected string format"""
    actual_extraction_string = PhenotipsImporter.extract_hpo_terms(exported_phenotips_to_import_json["features"])
    expected_extraction_string = (
        "HP:0000175: Cleft palate; HP:0000252: Microcephaly; "
        "HP:0000708: Behavioral abnormality; HP:0000750: Delayed speech and language development; "
        "HP:0001263: Global developmental delay; HP:0002719: Recurrent infections; HP:0004322: Short stature; "
        "HP:0008872: Feeding difficulties in infancy; HP:0410030: Cleft lip"
    )

    assert actual_extraction_string == expected_extraction_string


def test_import_phenotips_json(phenotips_importer, analysis_collection, exported_phenotips_to_import_json):
    """Tests the import_phenotips_json function"""
    analysis_collection.collection.find_one.return_value = None
    incoming_phenotips_json = exported_phenotips_to_import_json
    incoming_phenotips_json["external_id"] = "C-PAM12345"
    actual = phenotips_importer.import_phenotips_json(incoming_phenotips_json)
    assert actual["name"] == "CPAM12345"


@pytest.fixture(name="phenotips_importer")
def fixture_phenotips_importer(analysis_collection, genomic_unit_collection):
    """Returns a PhenotipsImporter object"""
    return PhenotipsImporter(analysis_collection, genomic_unit_collection)


@pytest.fixture(name="exported_phenotips_to_import_json")
def fixture_phenotips_import():
    """Returns a phenotips json fixture"""
    return read_test_fixture("phenotips-import.json")
