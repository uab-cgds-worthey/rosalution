"""Tests Annotation Tasks and the creation of them"""
import copy
import pytest

from src.core.annotation_task import AnnotationTaskFactory, HttpAnnotationTask
from src.enums import GenomicUnitType
from src.core.annotation_unit import AnnotationUnit


def test_http_annotation_task_build_url(http_annotation_transcript_id):
    """Verifies that the HTTP annotation task creates the base url using the 'url' and the genomic unit"""
    actual = http_annotation_transcript_id.build_url()

    assert (
        actual ==
        "http://grch37.rest.ensembl.org/vep/human/hgvs/NM_170707.3:c.745C>T?content-type=application/json;refseq=1;"
    )
    # This link cannot be shortened, will just disable for this one due to the nature of the long URL dependency


def test_http_annotation_task_build_url_with_dependency(http_annotation_task_gene):
    """Verifies that the HTTP annotation task builds the URL that includes depdencies"""
    actual = http_annotation_task_gene.build_url()
    assert actual == "https://hpo.jax.org/api/hpo/gene/45614"


def test_annotation_task_create_http_task(hgvs_variant_annotation_unit):
    """Verifies that the annotation task factory creates the correct annotation task according to the dataset type"""
    actual_task = AnnotationTaskFactory.create_annotation_task(hgvs_variant_annotation_unit)
    assert isinstance(actual_task, HttpAnnotationTask)


def test_annotation_extraction_for_transcript_id_dataset(http_annotation_transcript_id, transcript_annotation_response):
    """Verifying genomic unit extraction for a transcript using the the transcript ID dataset"""
    actual_extractions = http_annotation_transcript_id.extract(transcript_annotation_response)
    assert len(actual_extractions) == 2
    assert {
        'data_set': 'transcript_id', 'data_source': 'Ensembl', 'version': '', 'value': 'NM_001017980.4',
        'transcript_id': 'NM_001017980.4'
    } in actual_extractions

    assert {
        'data_set': 'transcript_id', 'data_source': 'Ensembl', 'version': '', 'value': 'NM_001363810.1',
        'transcript_id': 'NM_001363810.1'
    } in actual_extractions


def test_annotation_extraction_for_polyphen_prediction_transcript_dataset(
    http_annotation_polyphen_prediction, transcript_annotation_response
):
    """Verifying genomic unit extraction for a transcript using the the transcript ID dataset"""
    actual_extractions = http_annotation_polyphen_prediction.extract(transcript_annotation_response)
    assert len(actual_extractions) == 2

    actual_nm_001017980_extraction = next(
        (annotation for annotation in actual_extractions if annotation['transcript_id'] == 'NM_001017980.4'), None
    )

    actual_nm_001363810_extraction = next(
        (annotation for annotation in actual_extractions if annotation['transcript_id'] == 'NM_001363810.1'), None
    )

    assert actual_nm_001017980_extraction['value'] == 'possibly_damaging'
    assert actual_nm_001363810_extraction['value'] == 'probably_damaging'


def test_annotation_extraction_for_genomic_unit(http_annotation_task_gene, hpo_annotation_response):
    """Verifying genomic unit extraction for a gene using the HPO dataset"""
    actual_extractions = http_annotation_task_gene.extract(hpo_annotation_response)
    assert len(actual_extractions) == 1
    assert {
        'data_set': 'HPO', 'data_source': 'HPO', 'version': '',
        'value': ['Myopathy, X-linked, With Excessive Autophagy']
    } in actual_extractions


def test_annotation_extraction_value_error_exception(http_annotation_task_gene, hpo_annotation_response):
    """
    Verifying annotation failure does not cause crash in application during extraction. Removes the expected value
    in the json to force jq parse error to more closelyemulate the failure instead of mocking the jq response to fail.
    """

    del hpo_annotation_response['diseaseAssoc']

    actual_extractions = http_annotation_task_gene.extract(hpo_annotation_response)
    assert len(actual_extractions) == 0


## Fixtures ##

@pytest.fixture(name="gene_ncbi_linkout_dataset")
def fixture_ncbi_linkout_dataset():
    """
    Retrusn the the 'forged' dataset configuration that builds the dataset from a genomic unit and its dependencies
    """
    return {
        "data_set": "NCBI_linkout",
        "data_source": "Rosalution",
        "genomic_unit_type": "gene",
        "annotation_source_type": "forge",
        "base_string": "https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term={Entrez Gene Id}",
        "attribute": "{ \"NCBI_linkout\": .NCBI_linkout }",
        "dependencies": ["Entrez Gene Id"],
    }


@pytest.fixture(name="gene_hpo_dataset")
def fixture_gene_hpo_dataset():
    """
    Returns the dict of the HPO dataset that has a dependency
    """
    return {
        "data_set": "HPO",
        "data_source": "HPO",
        "genomic_unit_type": "gene",
        "annotation_source_type": "http",
        "url": "https://hpo.jax.org/api/hpo/gene/{Entrez Gene Id}",
        "dependencies": ["Entrez Gene Id"],
        "attribute": "{ \"diseaseAssoc\": [.diseaseAssoc[].diseaseName]}",
    }


@pytest.fixture(name="gene_genomic_unit")
def fixture_gene_genomic_unit():
    """Returns the genomic unit 'VMA21' to be annotated"""
    return {
        "unit": "VMA21",
        "Entrez Gene Id": "45614",
        "genomic_unit_type": GenomicUnitType.GENE,
    }


@pytest.fixture(name="http_annotation_task_gene")
def fixture_http_annotation_empty(gene_genomic_unit, gene_hpo_dataset):
    """Returns an HTTP annotation taskd"""
    annotation_unit = AnnotationUnit(gene_genomic_unit, gene_hpo_dataset)
    task = HttpAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit():
    """Returns the genomic unit 'NM_170707.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_170707.3:c.745C>T",
        "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
        "transcript": "NM_170707",
    }


@pytest.fixture(name="transcript_id_dataset")
def fixture_transcript_id_dataset():
    """
    Returns the dict of the transcript_id dataset
    """
    return {
        "data_set": "transcript_id",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "transcript": True,
        "annotation_source_type": "http",
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;refseq=1;",
        "attribute": ".[].transcript_consequences[] | { transcript_id: .transcript_id }",
    }


@pytest.fixture(name="hgvs_variant_annotation_unit")
def fixture_hgvs_variant_annotation_unit(hgvs_variant_genomic_unit, transcript_id_dataset):
    """
    Returns the annotation unit with hgvs_variant genomic unit and transcript_id dataset
    """
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit, transcript_id_dataset)
    return annotation_unit


@pytest.fixture(name="http_annotation_transcript_id")
def fixture_http_annotation_transcript_id(hgvs_variant_genomic_unit, transcript_id_dataset):
    """An HTTP annotation task with a single dataset"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit, transcript_id_dataset)
    task = HttpAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="polyphen_prediction_dataset")
def fixture_polyphen_prediction_dataset():
    """
    Returns the dict of the polyphen_prediction dataset
    """
    return {
        "data_set": "Polyphen Prediction",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "transcript": True,
        "annotation_source_type": "http",
        "url": "http://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;refseq=1;",
        "attribute":
            ".[].transcript_consequences[] | \
            { polyphen_prediction: .polyphen_prediction,transcript_id: .transcript_id }",
    }


@pytest.fixture(name="ditto_score_dataset")
def fixture_ditto_score_dataset():
    """ Returns a subprocess dataset specifically for ditto """

    return {
        "data_set": "DITTO",
        "data_source": "cgds",
        "genomic_unit_type": "hgvs_variant",
        "annotation_source_type": "subprocess",
        "subprocess":
            "tabix https://s3.lts.rc.uab.edu/cgds-public/dittodb/DITTO_chr{chrom}.tsv.gz chr{chrom}:{pos}-{pos}",
        "fieldnames": ["chrom", "pos", "ref", "alt", "transcript", "gene", "classification", "ditto"],
        "delimiter": "\t",
        "attribute": ".[] += (\"{ensembl_vep_vcf_string}\" | split(\"-\") | {\"vcf_string\": .}) | .[] | " \
            "select( .chrom == (\"chr\" + .vcf_string[0]) and .vcf_string[1] == .pos and .vcf_string[2] == " \
            ".ref and .vcf_string[3] == .alt and .transcript ==\"{Ensembl_Transcript_Id}\") | { \"ditto\": .ditto }",
        "dependencies": [
            "chrom",
            "pos",
            "Ensembl_Transcript_Id",
            "ensembl_vep_vcf_string"
        ],
        "versioning_type": "rosalution"
    }


@pytest.fixture(name="http_annotation_polyphen_prediction")
def fixture_http_annotation_polyphen_prediction(hgvs_variant_genomic_unit, polyphen_prediction_dataset):
    """An HTTP annotation task with a single dataset"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit, polyphen_prediction_dataset)
    task = HttpAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="hpo_annotation_response")
def fixture_hpo_annotation_response():
    """
    Returns an object that contains the actual return aoutput for GENE VMA21 for HPO terms
    """
    return {
        "gene": {"entrezGeneId": 203547, "entrezGeneSymbol": "VMA21"},
        "termAssoc": [
            {"ontologyId": "HP:0001270", "name": "Motor delay", "definition": "A type of Developmental delay crized"},
            {"ontologyId": "HP:0001419", "name": "X-linked recessive inheritance", "definition": "A mode of inheriee."},
            {"ontologyId": "HP:0001371", "name": "Flexion contracture", "definition": "A flexion contracnt of joints."},
            {"ontologyId": "HP:0003391", "name": "Gowers sign", "definition": "A phenomenon whereby patie"},
            {"ontologyId": "HP:0008994", "name": "Proximal muscle weakness in lower limbs", "definition": "lack legs."},
            {"ontologyId": "HP:0002650", "name": "Scoliosis", "definition": "The presence of an abnormal lateral curv"},
            {"ontologyId": "HP:0003551", "name": "Difficulty climbing stairs", "definition": "Reduced abilit climb."},
            {"ontologyId": "HP:0002093", "name": "Respiratory insufficiency", "definition": ""},
            {"ontologyId": "HP:0003198", "name": "Myopathy", "definition": "A disorder of to impairment"},
            {"ontologyId": "HP:0009046", "name": "Difficulty running", "definition": "Reduced ability to run."},
            {"ontologyId": "HP:0003202", "name": "Skeletal muscle atrophy", "definition": "The presence of skeletal "},
            {"ontologyId": "HP:0001319", "name": "Neonatal hypotonia", "definition": "Muscular hypotonia (abnormally "},
            {
                "ontologyId": "HP:0003236", "name": "Elevated circulating creatine kinase concentration",
                "definition": "A"
            },
            {"ontologyId": "HP:0002486", "name": "Myotonia", "definition": "An involuntartrical stimulation."},
            {"ontologyId": "HP:0007941", "name": "Limited extraocular movements", "definition": "Limitehe"},
        ],
        "diseaseAssoc": [{
            "diseaseId": "OMIM:310440", "diseaseName": "Myopathy, X-linked, With Excessive Autophagy", "dbId": "310440",
            "db": "OMIM"
        }],
    }


@pytest.fixture(name="hgvs_variant_ditto_annotation_unit")
def fixture_hgvs_variant_ditto_annotation_unit(hgvs_variant_genomic_unit, ditto_score_dataset):
    """ Creates and returns a ditto annotation unit with the required dependencies to run """

    # Creating a copy of the variant fixture
    ditto_hgvs_variant_genomic_unit = copy.deepcopy(hgvs_variant_genomic_unit)

    # Adding dependencies to the genomic unit for ditto
    ditto_hgvs_variant_genomic_unit["chrom"] = "X"
    ditto_hgvs_variant_genomic_unit["pos"] = "156134910"
    ditto_hgvs_variant_genomic_unit["Ensembl_Transcript_Id"] = "ENST00000368297"
    ditto_hgvs_variant_genomic_unit["ensembl_vep_vcf_string"] = "1-156134910-C-T"

    annotation_unit = AnnotationUnit(ditto_hgvs_variant_genomic_unit, ditto_score_dataset)

    return annotation_unit
