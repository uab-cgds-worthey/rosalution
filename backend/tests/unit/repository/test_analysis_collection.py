"""Tests analysis collection"""


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
