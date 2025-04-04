"""Tests Annotation Tasks and the creation of them"""
import pytest

from src.core.annotation_task import ForgeAnnotationTask
from src.enums import GenomicUnitType
from src.core.annotation_unit import AnnotationUnit


def test_annotate_forge_gene_linkout_dataset(forge_annotation_task_gene):
    """Verifies that the NCBI linkout dataset is structured as expected"""
    actual_annotation = forge_annotation_task_gene.annotate()
    assert "NCBI_linkout" in actual_annotation
    assert actual_annotation['NCBI_linkout'] == 'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=45614'


def test_extraction_forge_gene_linkout_dataset(forge_annotation_task_gene):
    """Verifies that the NCBI linkout dataset is extracted as expected"""
    annotation = forge_annotation_task_gene.annotate()
    extracted_annotations = forge_annotation_task_gene.extract(annotation)
    assert extracted_annotations[0]['value'] == 'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=45614'


def test_extraction_forge_hgvs_variant_without_transcript_version(hgvs_without_transcript_version_annotation_task):
    """Verifies the jq query used to forge create the transcript without a version dataset for a variant"""
    forge_annotation = hgvs_without_transcript_version_annotation_task.annotate()
    actual_extractions = hgvs_without_transcript_version_annotation_task.extract(forge_annotation)
    assert actual_extractions[0]['value'] == "NM_001017980:c.745C>T"


def test_annotation_forge_from_cache_dataset_dependeny_cadd(forge_annotation_task_hgvs_variant_cadd):
    """Verifies the forge task annotates a dataset using a cached dataset dependency like the mocked one included"""
    forge_annotation = forge_annotation_task_hgvs_variant_cadd.annotate()

    assert 'CADD' in forge_annotation
    assert isinstance(forge_annotation['CADD'], list)
    assert len(forge_annotation['CADD']) == 1
    assert forge_annotation['CADD'][0]['input'] == "NM_001017980:c.164G>T"


def test_extraction_forge_from_cache_dataset_dependeny_cadd(forge_annotation_task_hgvs_variant_cadd):
    """Verifies the forge task extracts a dataset annotation from a cached dataset dependency like the one included"""
    forge_annotation = forge_annotation_task_hgvs_variant_cadd.annotate()
    actual_extractions = forge_annotation_task_hgvs_variant_cadd.extract(forge_annotation)
    assert actual_extractions[0]['value'] == 24


def test_annotation_forge_from_cache_dataset_dependeny_polyphen(forge_annotation_task_hgvs_variant_polyphen):
    """Verifies the forge task annotates a dataset using a cached dataset dependency like the mocked one included"""
    forge_annotation = forge_annotation_task_hgvs_variant_polyphen.annotate()

    assert 'Polyphen Prediction' in forge_annotation
    assert isinstance(forge_annotation['Polyphen Prediction'], list)
    assert len(forge_annotation['Polyphen Prediction']) == 1
    assert forge_annotation['Polyphen Prediction'][0]['input'] == "NM_001017980:c.164G>T"


def test_extraction_forge_from_cache_dataset_dependeny_polyphen(forge_annotation_task_hgvs_variant_polyphen):
    """Verifies the forge task annotates a dataset using a cached dataset dependency like the mocked one included"""
    forge_annotation = forge_annotation_task_hgvs_variant_polyphen.annotate()

    actual_extractions = forge_annotation_task_hgvs_variant_polyphen.extract(forge_annotation)
    assert actual_extractions[0]['value'] == 'possibly_damaging'


## Fixtures ##


@pytest.fixture(name="forge_annotation_task_gene")
def fixture_forge_annotation_task_gene_ncbi_linkout(gene_genomic_unit, gene_ncbi_linkout_dataset):
    """Returns a Forge annotation task for the NCBI linkout for the VMA21 Gene genomic unit"""
    annotation_unit = AnnotationUnit(gene_genomic_unit, gene_ncbi_linkout_dataset)
    task = ForgeAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="gene_ncbi_linkout_dataset")
def fixture_ncbi_linkout_dataset():
    """Returns 'forged' dataset configuration that builds the dataset from a genomic unit and its dependencies"""
    return {
        "data_set": "NCBI_linkout",
        "data_source": "Rosalution",
        "genomic_unit_type": "gene",
        "annotation_source_type": "forge",
        "base_string": "https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term={Entrez Gene Id}",
        "attribute": "{ \"NCBI_linkout\": .NCBI_linkout }",
        "dependencies": ["Entrez Gene Id"],
    }


@pytest.fixture(name="cadd_dataset_config")
def fixture_cadd_from_cached_dataset_as_dependency():
    """An annotation configuration for a dataset that uses a cached dataset like the Ensembl HGVS variant call result"""
    return {
        "data_set": "CADD",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "annotation_source_type": "forge",
        "base_string_cache": True,
        "base_string": "{ENSEMBL_VARIANT_CALL_CACHE}",
        "attribute":
            ".CADD | .[].transcript_consequences[] | select( .transcript_id | contains(\"{transcript}\") ) | { CADD: .cadd_phred }",  # pylint: disable=line-too-long 
        "dependencies": ["transcript", "ENSEMBL_VARIANT_CALL_CACHE"],
        "versioning_type": "rest",
        "version_url": "https://rest.ensembl.org/info/data/?content-type=application/json",
        "version_attribute": ".releases[]"
    }


@pytest.fixture(name="polyphen_dataset_config")
def fixture_polyphen_from_cached_dataset_as_dependency():
    """r.i.p. sanity"""
    return {
        "data_set": "Polyphen Prediction",
        "data_source": "Ensembl",
        "genomic_unit_type": "hgvs_variant",
        "transcript": True,
        "annotation_source_type": "forge",
        "base_string_cache": True,
        "base_string": "{ENSEMBL_VARIANT_CALL_CACHE}",
        "attribute":
            ".\"Polyphen Prediction\" | .[].transcript_consequences[] | { polyphen_prediction: .polyphen_prediction, transcript_id: .transcript_id }",  # pylint: disable=line-too-long
        "versioning_type": "rest",
        "dependencies": ["ENSEMBL_VARIANT_CALL_CACHE"],
        "version_url": "https://rest.ensembl.org/info/data/?content-type=application/json",
        "version_attribute": ".releases[]"
    }


@pytest.fixture(name="forge_annotation_task_hgvs_variant_cadd")
def fixture_forge_annotation_task_ensembl_cache(hgvs_variant_genomic_unit, cadd_dataset_config):
    """Returns a Forge annotation task for the NCBI linkout for the VMA21 Gene genomic unit"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit, cadd_dataset_config)
    task = ForgeAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="forge_annotation_task_hgvs_variant_polyphen")
def fixture_forge_annotation_task_ensembl_cache_polyphen(hgvs_variant_genomic_unit, polyphen_dataset_config):
    """Returns a Forge annotation task for the NCBI linkout for the VMA21 Gene genomic unit"""
    annotation_unit = AnnotationUnit(hgvs_variant_genomic_unit, polyphen_dataset_config)
    task = ForgeAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="gene_genomic_unit")
def fixture_gene_genomic_unit():
    """Returns the genomic unit 'VMA21' to be annotated"""
    return {
        "unit": "VMA21",
        "Entrez Gene Id": "45614",
        "genomic_unit_type": GenomicUnitType.GENE,
    }


@pytest.fixture(name="hgvs_variant_genomic_unit")
def fixture_genomic_unit(ensembl_hgvs_variant_call_cache_dataset_value):
    """Returns the genomic unit 'NM_001017980.3:c.745C>T' to be annotated"""
    return {
        "unit": "NM_001017980.3:c.745C>T", "genomic_unit_type": GenomicUnitType.HGVS_VARIANT,
        "transcript": "NM_001017980", "ENSEMBL_VARIANT_CALL_CACHE": ensembl_hgvs_variant_call_cache_dataset_value
    }


@pytest.fixture(name="hgvs_without_transcript_version_annotation_task")
def fixture_hgvs_without_transcript_version(hgvs_variant_genomic_unit):
    """An Annotation Unit to experiment with jq parsing and rebuilding a string in a result."""
    annotation_unit = AnnotationUnit(
        hgvs_variant_genomic_unit,
        {
            "data_set": "hgvs_variant_without_transcript_version",
            "data_source": "Rosalution",
            "annotation_source_type": "forge",
            "genomic_unit_type": "hgvs_variant",
            "base_string": "{hgvs_variant}",
            "attribute":
                ".hgvs_variant_without_transcript_version | split(\":\") as $transcript_split | $transcript_split[0] | split(\".\")[0] | . + \":\" + $transcript_split[1] | {\"hgvs_variant_without_transcript_version\": .}",  # pylint: disable=line-too-long 
            "versioning_type": "rosalution"
        }
    )
    task = ForgeAnnotationTask(annotation_unit)
    return task


@pytest.fixture(name="ensembl_hgvs_variant_call_cache_dataset_value")
def fixture_ensembl_hgvs_variant_call_cache_dataset_value():
    """Mocks the dataset value that is returned from the mongodb database for the cached hgvs variant call dataset."""
    return [{
        "input": "NM_001017980:c.164G>T", "id": "NM_001017980:c.164G>T", "vcf_string": "X-151404916-G-T",
        "most_severe_consequence": "missense_variant", "start": 151404916, "assembly_name": "GRCh38",
        "seq_region_name": "X", "colocated_variants": [{
            "clin_sig": ["uncertain_significance"], "start": 151404916, "allele_string": "G/A/T", "id": "rs1306425454",
            "strand": 1, "seq_region_name": "X", "phenotype_or_disease": 1,
            "var_synonyms": {"ClinVar": ["RCV003741639", "VCV002805126", "RCV000705011", "VCV000581244"]},
            "end": 151404916, "clin_sig_allele": "A:uncertain_significance;T:uncertain_significance"
        }], "allele_string": "G/T", "transcript_consequences": [{
            "codons": "gGc/gTc", "cadd_raw": 3.96743, "amino_acids": "G/V", "gene_id": "203547",
            "polyphen_score": 0.607, "cdna_end": 267, "gene_symbol": "VMA21", "sift_score": 0, "variant_allele": "T",
            "cds_start": 164, "transcript_id": "NM_001017980.4", "cds_end": 164, "protein_start": 55, "strand": 1,
            "protein_end": 55, "used_ref": "G", "polyphen_prediction": "possibly_damaging", "impact": "MODERATE",
            "cdna_start": 267, "cadd_phred": 24, "biotype": "protein_coding",
            "consequence_terms": ["missense_variant", "splice_region_variant"], "given_ref": "G",
            "gene_symbol_source": "EntrezGene", "sift_prediction": "deleterious"
        }, {
            "biotype": "protein_coding", "cadd_phred": 24, "given_ref": "G",
            "consequence_terms": ["missense_variant", "splice_region_variant"], "impact": "MODERATE", "cdna_start": 574,
            "sift_prediction": "deleterious", "gene_symbol_source": "EntrezGene", "variant_allele": "T",
            "sift_score": 0.01, "gene_symbol": "VMA21", "cds_start": 329, "cadd_raw": 3.96743, "codons": "gGc/gTc",
            "gene_id": "203547", "amino_acids": "G/V", "polyphen_score": 0.998, "cdna_end": 574, "strand": 1,
            "protein_end": 110, "used_ref": "G", "polyphen_prediction": "probably_damaging",
            "transcript_id": "NM_001363810.1", "protein_start": 110, "cds_end": 329
        }], "strand": 1, "end": 151404916
    }]
