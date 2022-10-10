"""Tests analysis collection"""

from ...test_utils import read_test_fixture  # pylint: disable=unused-import


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


# this test is disabled for now, it will be re-enabled after we add in this functionality to the main branch
# def test_update_analysis_section(analysis_collection):
#     """Tests the update_analysis_section function"""
#     analysis_collection.collection.find_one.return_value = read_test_fixture(
#         "analysis-CPAM0112.json")
#     actual = analysis_collection.update_analysis_section(
#         "CPAM0112", "Brief", "Reason", {"value": ["the quick brown fox jumps over the lazy dog."]})
#     assert actual["sections"][0]["content"][1]["value"] == [
#         "the quick brown fox jumps over the lazy dog."]


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
