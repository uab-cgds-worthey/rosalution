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


def test_add_file(analysis_collection):
    """Tests the update_analysis function"""
    actual = analysis_collection.add_file(
        "CPAM0002", "test.txt", "This is a test comment for file test.txt")
    assert actual["files"][0]["filename"] == "test.txt"
    assert actual["files"][0]["comments"] == "This is a test comment for file test.txt"
