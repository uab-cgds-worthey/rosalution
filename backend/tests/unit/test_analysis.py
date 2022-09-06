"""Tests analysis collection"""
import pytest


def test_all(analysis_collection):
    """Tests the all function"""
    actual = analysis_collection.all()
    assert len(actual) == 5
    assert actual[0]["name"] == "CPAM0002"


def test_update_analysis(analysis_collection):
    """Tests the update_analysis function"""
    analysis_collection.update_analysis(
        "CPAM0002", {"name": "CPAM0002", "description": "test"})
    actual = analysis_collection.find_by_name("CPAM0002")
    assert actual["description"] == "test"
