"""Tests Annotation Tasks and the creation of them"""
from unittest.mock import Mock, patch

import copy
import subprocess
import pytest

from src.core.annotation_task import AnnotationTaskFactory, SubprocessAnnotationTask
from src.core.annotation_unit import AnnotationUnit


def test_subprocess_annotation_build_command_with_dependency(subprocess_annotation_ditto_score_task):
    """ Verifies the subprocess command is built properly to be executed programmatically """
    expected = ['tabix', 'https://s3.lts.rc.uab.edu/cgds-public/dittodb/DITTO_chrX.tsv.gz', 'chrX:156134910-156134910']

    actual = subprocess_annotation_ditto_score_task.build_command()

    assert expected == actual


def test_annotation_task_create_subprocess_task(hgvs_variant_ditto_annotation_unit):
    """ Verifies the ditto dataset creates a subprocess task """
    actual_task = AnnotationTaskFactory.create_annotation_task(hgvs_variant_ditto_annotation_unit)

    assert isinstance(actual_task, SubprocessAnnotationTask)


def test_ditto_subprocess_annotate(subprocess_annotation_ditto_score_task):
    """ Tests the completion of a subprocess and extracting the correct result """
    expected = [{
        'chrom': 'chr1', 'pos': '156134910', 'ref': 'C', 'alt': 'A', 'transcript': 'ENST00000347559', 'gene': 'LMNA',
        'classification': 'synonymous_variant', 'ditto': '0.00011253357'
    }]

    mock_response = Mock(spec=subprocess.CompletedProcess)
    attrs = {
        'args': [
            'tabix', 'https://s3.lts.rc.uab.edu/cgds-public/dittodb/DITTO_chr1.tsv.gz', 'chr1:156134910-156134910'
        ], 'returncode': 0,
        'stdout': b'chr1\t156134910\tC\tA\tENST00000347559\tLMNA\tsynonymous_variant\t0.00011253357\n'
    }
    mock_response.configure_mock(**attrs)

    with patch('subprocess.run', return_value=mock_response):
        task = subprocess_annotation_ditto_score_task

        actual_subprocess_result = task.annotate()

        assert expected == actual_subprocess_result


def test_ditto_subprocess_annotate_failure(subprocess_annotation_ditto_score_task):
    """ Assures that the subprocess run function faily gracefully and returns an empty object """

    attrs = {
        'cmd': ['tabix', 'https://s3.lts.rc.uab.edu/cgds-public/fake-data.gz', 'chr1:156134910-156134910'],
        'returncode': 1, 'stderr': b''
    }

    mock_error = subprocess.CalledProcessError(**attrs)

    with patch('subprocess.run', side_effect=mock_error):
        result = subprocess_annotation_ditto_score_task.annotate()

        assert result == {}


## Fixtures ##


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


@pytest.fixture(name="hgvs_variant_ditto_annotation_unit")
def fixture_hgvs_variant_ditto_annotation_unit(hgvs_variant_genomic_unit_for_annotation_tasks, ditto_score_dataset):
    """ Creates and returns a ditto annotation unit with the required dependencies to run """

    # Creating a copy of the variant fixture
    ditto_hgvs_variant_genomic_unit = copy.deepcopy(hgvs_variant_genomic_unit_for_annotation_tasks)

    # Adding dependencies to the genomic unit for ditto
    ditto_hgvs_variant_genomic_unit["chrom"] = "X"
    ditto_hgvs_variant_genomic_unit["pos"] = "156134910"
    ditto_hgvs_variant_genomic_unit["Ensembl_Transcript_Id"] = "ENST00000368297"
    ditto_hgvs_variant_genomic_unit["ensembl_vep_vcf_string"] = "1-156134910-C-T"

    annotation_unit = AnnotationUnit(ditto_hgvs_variant_genomic_unit, ditto_score_dataset)

    return annotation_unit


@pytest.fixture(name="subprocess_annotation_ditto_score_task")
def fixture_subprocess_annotation_ditto_score(hgvs_variant_ditto_annotation_unit):
    """ Creates a subprocess task with the ditto annotation unit fixture """

    task = SubprocessAnnotationTask(hgvs_variant_ditto_annotation_unit)

    return task
