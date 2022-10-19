"""Tests analysis collection"""
import pytest

from ...test_utils import read_test_fixture


def test_all(analysis_collection):
    """Tests the all function"""
    actual = analysis_collection.all()
    assert len(actual) == 5
    assert actual[0]["name"] == "CPAM0002"


def test_update_analysis(analysis_collection):
    """Tests the update_analysis function"""
    actual = analysis_collection.update_analysis(
        "CPAM0002", {"name": "CPAM0112", "nominated_by": "Dr. Person One"})
    assert actual["name"] == "CPAM0112"
    assert actual["nominated_by"] == "Dr. Person One"


def test_update_analysis_section(analysis_collection):
    """Tests the update_analysis_section function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0112.json")
    analysis_collection.collection.find_one_and_update.return_value = read_test_fixture(
        "update_analysis_section.json")
    actual = analysis_collection.update_analysis_section(
        "CPAM0112", "Brief", "Reason", {"value": ["the quick brown fox jumps over the lazy dog."]})
    assert actual["sections"][0]["content"][1]["value"] == [
        "the quick brown fox jumps over the lazy dog."]


def test_add_file(analysis_collection):
    """Tests the update_analysis function"""
    actual = analysis_collection.add_file(
        "CPAM0002", "633afb87fb250a6ea1569555", "test.txt", "This is a test comment for file test.txt")
    assert actual["supporting_evidence_files"][0]["filename"] == "test.txt"
    assert actual["supporting_evidence_files"][0]["file_id"] == "633afb87fb250a6ea1569555"
    assert actual["supporting_evidence_files"][0]["comments"] == "This is a test comment for file test.txt"


def test_attach_link_supporting_evidence(analysis_collection, cpam0002_analysis_json):
    """Tests adding supporting evidence link to an analysis and return an updated analysis"""
    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        updated_analysis = cpam0002_analysis_json
        updated_analysis['supporting_evidence_files'].append(
            query['$push']['supporting_evidence_files'])
        updated_analysis['_id'] = 'fake-mongo-object-id'
        return updated_analysis

    analysis_collection.collection.find_one_and_update.side_effect = valid_query_side_effect

    actual_analysis = analysis_collection.attach_supporting_evidence_link(
        "CPAM0002", "Interesting Article", "http://sites.uab.edu/cgds/", "Serious Things in here")

    assert '_id' not in actual_analysis

    new_evidence = next(
        (evidence for evidence in actual_analysis['supporting_evidence_files']
            if evidence['name'] == "Interesting Article"), None)
    assert new_evidence['type'] == 'link'
    assert 'attachment_id' in new_evidence
    assert new_evidence['data'] == 'http://sites.uab.edu/cgds/'


def test_attach_file_supporting_evidence(analysis_collection, cpam0002_analysis_json):
    """Tests adding supporting evidence link to an analysis and return an updated analysis"""
    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        updated_analysis = cpam0002_analysis_json
        updated_analysis['supporting_evidence_files'].append(
            query['$push']['supporting_evidence_files'])
        updated_analysis['_id'] = 'fake-mongo-object-id'
        return updated_analysis

    analysis_collection.collection.find_one_and_update.side_effect = valid_query_side_effect

    actual_analysis = analysis_collection.attach_supporting_evidence_file(
        "CPAM0002", "Fake-Mongo-Object-ID-2", "SeriousFileName.pdf", "Serious Things said in here")

    assert '_id' not in actual_analysis

    new_evidence = next(
        (evidence for evidence in actual_analysis['supporting_evidence_files']
            if evidence['name'] == "SeriousFileName.pdf"), None)
    assert new_evidence['type'] == 'file'
    assert 'attachment_id' in new_evidence
    assert new_evidence['attachment_id'] == 'Fake-Mongo-Object-ID-2'


def test_get_genomic_units(analysis_collection):
    """Tests the get_genomic_units function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0002.json")
    actual = analysis_collection.get_genomic_units("CPAM0002")
    assert len(actual) == 2


def test_get_genomic_units_analysis_does_not_exist(analysis_collection):
    """Tests the get_genomic_units function"""
    analysis_collection.collection.find_one.return_value = None
    try:
        analysis_collection.get_genomic_units("CPAM2222")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis with name CPAM2222 does not exist"


def test_get_genomic_units_analysis_has_no_genomic_units(analysis_collection):
    """Tests the get_genomic_units function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0002.json").pop("genomic_units")

    try:
        analysis_collection.get_genomic_units("CPAM0002")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis CPAM0002 does not have genomic units"


def test_get_genomic_units_with_no_p_dot(analysis_collection, analysis_with_no_p_dot):
    """Tests the get_genomic_units function"""
    analysis_collection.collection.find_one.return_value = analysis_with_no_p_dot
    actual = analysis_collection.get_genomic_units("CPAM1111")
    assert len(actual) == 2
    assert actual == {'genes': {'VMA21': ['NM_001017980.3:c.164G>T']}, 'variants': [
        'NM_001017980.3:c.164G>T']}


def test_remove_supporting_evidence(analysis_collection):
    """Tests the remove_supporting_evidence function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture(
        "analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    analysis_collection.collection.find_one_and_update.return_value = expected
    actual = analysis_collection.remove_supporting_evidence(
        "CPAM0002", "633afb87fb250a6ea1569555")
    assert actual == expected


@pytest.fixture(name="analysis_with_no_p_dot")
def fixture_analysis_with_no_p_dot():
    """Returns an analysis with no p. in the genomic unit"""
    return {
        "name": "CPAM1111",
        "genomic_units": [
            {
                "gene": "VMA21",
                "transcripts": [
                    {
                        "transcript": "NM_001017980.3"
                    }
                ],
                "variants": [
                    {
                        "hgvs_variant": "NM_001017980.3:c.164G>T",
                        "c_dot": "c.164G>T",
                        "p_dot": "",
                        "build": "GRCh38"
                    }
                ]
            }
        ]
    }
