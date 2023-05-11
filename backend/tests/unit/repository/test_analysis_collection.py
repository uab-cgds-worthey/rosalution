"""Tests analysis collection"""
from unittest.mock import patch
import datetime
import pytest

from pymongo import ReturnDocument
from src.enums import EventType
from src.models.event import Event
from ...test_utils import read_test_fixture


def test_all(analysis_collection):
    """Tests the all function"""
    actual = analysis_collection.all()
    assert len(actual) == 6
    assert actual[0]["name"] == "CPAM0002"


def test_summary_by_name(analysis_collection):
    """Tests the summary_by_name function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    actual = analysis_collection.summary_by_name("CPAM0002")
    assert actual["name"] == "CPAM0002"


def test_find_by_name(analysis_collection):
    """Tests the find_by_name function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    actual = analysis_collection.find_by_name("CPAM0002")
    assert actual["name"] == "CPAM0002"


def test_update_analysis_section(analysis_collection):
    """Tests the update_analysis_section function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0112.json")
    analysis_collection.collection.find_one_and_update.return_value = read_test_fixture("update_analysis_section.json")
    actual = analysis_collection.update_analysis_section(
        "CPAM0112", "Brief", "Reason", {"value": ["the quick brown fox jumps over the lazy dog."]}
    )
    assert actual["sections"][0]["content"][1]["value"] == ["the quick brown fox jumps over the lazy dog."]


def test_find_file_by_name(analysis_collection):
    """Tests the find_file_by_name function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    actual = analysis_collection.find_file_by_name("CPAM0002", "test.txt")
    assert actual == {'attachment_id': '633afb87fb250a6ea1569555', 'comments': 'hello world', 'name': 'test.txt'}


def test_find_file_by_name_analysis_none(analysis_collection):
    """Tests the find_file_by_name function"""
    analysis_collection.collection.find_one.return_value = None
    actual = analysis_collection.find_file_by_name("CPAM1234", "notfound.txt")
    assert actual is None


def test_find_file_by_name_no_supporting_evidence(analysis_collection):
    """Tests the find_file_by_name function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json"
                                                                            ).pop('supporting_evidence_files')
    actual = analysis_collection.find_file_by_name("CPAM0002", "notfound.txt")
    assert actual is None


def test_create_analysis(analysis_collection):
    """Tests the create_analysis function"""
    analysis_collection.collection.find_one.return_value = None
    new_analysis = read_test_fixture("analysis-CPAM0002.json")
    new_analysis["name"] = "CPAM1234"
    analysis_collection.create_analysis(new_analysis)
    analysis_collection.collection.insert_one.assert_called_once_with(new_analysis)


def test_create_analysis_already_exists(analysis_collection):
    """Tests the create_analysis function"""
    try:
        analysis_collection.create_analysis(read_test_fixture("analysis-CPAM0002.json"))
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis with name CPAM0002 already exists"


def test_attach_link_supporting_evidence(analysis_collection, cpam0002_analysis_json):
    """Tests adding supporting evidence link to an analysis and return an updated analysis"""

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        updated_analysis = cpam0002_analysis_json
        updated_analysis['supporting_evidence_files'].append(query['$push']['supporting_evidence_files'])
        updated_analysis['_id'] = 'fake-mongo-object-id'
        return updated_analysis

    analysis_collection.collection.find_one_and_update.side_effect = valid_query_side_effect

    actual_analysis = analysis_collection.attach_supporting_evidence_link(
        "CPAM0002", "Interesting Article", "http://sites.uab.edu/cgds/", "Serious Things in here"
    )

    assert '_id' not in actual_analysis

    new_evidence = next((
        evidence for evidence in actual_analysis['supporting_evidence_files']
        if evidence['name'] == "Interesting Article"
    ), None)
    assert new_evidence['type'] == 'link'
    assert 'attachment_id' in new_evidence
    assert new_evidence['data'] == 'http://sites.uab.edu/cgds/'


def test_attach_file_supporting_evidence(analysis_collection, cpam0002_analysis_json):
    """Tests adding supporting evidence link to an analysis and return an updated analysis"""

    def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        updated_analysis = cpam0002_analysis_json
        updated_analysis['supporting_evidence_files'].append(query['$push']['supporting_evidence_files'])
        updated_analysis['_id'] = 'fake-mongo-object-id'
        return updated_analysis

    analysis_collection.collection.find_one_and_update.side_effect = valid_query_side_effect

    actual_analysis = analysis_collection.attach_supporting_evidence_file(
        "CPAM0002", "Fake-Mongo-Object-ID-2", "SeriousFileName.pdf", "Serious Things said in here"
    )

    assert '_id' not in actual_analysis

    new_evidence = next((
        evidence for evidence in actual_analysis['supporting_evidence_files']
        if evidence['name'] == "SeriousFileName.pdf"
    ), None)
    assert new_evidence['type'] == 'file'
    assert 'attachment_id' in new_evidence
    assert new_evidence['attachment_id'] == 'Fake-Mongo-Object-ID-2'


def test_file_exists_in_analysis(analysis_collection):
    """Tests the file_exists_in_analysis function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    actual = analysis_collection.file_exists_in_analysis("CPAM0002", "test.txt")
    assert actual is True


def test_add_pedigree_file(analysis_collection, empty_pedigree):
    """Tests adding pedigree file to an analysis and return an updated analysis"""
    analysis_collection.collection.find_one.return_value = empty_pedigree
    expected = read_test_fixture("analysis-CPAM0002.json")

    analysis_collection.add_pedigree_file("CPAM0002", "63505be22888347cf1c275db")
    analysis_collection.collection.find_one_and_update.assert_called_with({"name": "CPAM0002"}, {"$set": expected})


def test_get_genomic_units(analysis_collection):
    """Tests the get_genomic_units function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
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
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json"
                                                                            ).pop("genomic_units")

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
    assert actual == {'genes': {'VMA21': ['NM_001017980.3:c.164G>T']}, 'variants': ['NM_001017980.3:c.164G>T']}


def test_remove_supporting_evidence(analysis_collection):
    """Tests the remove_supporting_evidence function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["supporting_evidence_files"] = []
    analysis_collection.collection.find_one_and_update.return_value = expected
    actual = analysis_collection.remove_supporting_evidence("CPAM0002", "633afb87fb250a6ea1569555")
    assert actual == expected


def test_get_pedigree_file_id(analysis_collection):
    """Tests the get_pedigree_file_id function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    actual = analysis_collection.get_pedigree_file_id("CPAM0002")
    assert actual == "63505be22888347cf1c275db"


def test_get_pedigree_file_id_pedigree_empty(analysis_collection, empty_pedigree):
    """Tests the get_pedigree_file_id function"""
    analysis_collection.collection.find_one.return_value = empty_pedigree
    try:
        analysis_collection.get_pedigree_file_id("CPAM0002")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis CPAM0002 does not have a pedigree file"


def test_get_pedigree_file_id_analysis_does_not_exist(analysis_collection):
    """Tests the get_pedigree_file_id function"""
    analysis_collection.collection.find_one.return_value = None
    try:
        analysis_collection.get_pedigree_file_id("CPAM2222")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis with name CPAM2222 does not exist"


def test_get_pedigree_file_id_pedigree_section_does_not_exist(analysis_collection):
    """Tests the get_pedigree_file_id function"""
    missing_pedigree_section = read_test_fixture("analysis-CPAM0002.json")
    del missing_pedigree_section["sections"][2]
    analysis_collection.collection.find_one.return_value = missing_pedigree_section
    try:
        analysis_collection.get_pedigree_file_id("CPAM0002")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis CPAM0002 does not have a pedigree section"


def test_remove_pedigree_file_id(analysis_collection):
    """Tests the remove_pedigree_file_id function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    expected = read_test_fixture("analysis-CPAM0002.json")
    expected["sections"][2]["content"] = []
    analysis_collection.collection.find_one_and_update.return_value = expected
    actual = analysis_collection.remove_pedigree_file("CPAM0002")
    assert actual == expected


def test_attach_third_party_link_monday(analysis_collection):
    """Tests the attach_third_party_link function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    analysis_collection.attach_third_party_link("CPAM0002", "monday_com", "https://monday.com")
    analysis_collection.collection.find_one_and_update.assert_called_with({'name': 'CPAM0002'}, {
        '$push': {'third_party_links': {'type': "monday_com", 'link': "https://monday.com"}}
    },
                                                                          return_document=True)


def test_attach_third_party_link_phenotips(analysis_collection):
    """Tests the attach_third_party_link function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    analysis_collection.attach_third_party_link("CPAM0002", "phenotips_com", "https://phenotips.com")
    analysis_collection.collection.find_one_and_update.assert_called_with({'name': 'CPAM0002'}, {
        '$push': {'third_party_links': {'type': "phenotips_com", 'link': 'https://phenotips.com'}}
    },
                                                                          return_document=True)


def test_attach_third_party_link_analysis_does_not_exist(analysis_collection):
    """Tests the attach_third_party_link function"""
    analysis_collection.collection.find_one.return_value = None
    try:
        analysis_collection.attach_third_party_link("CPAM02222", "MONDAY_COM", "https://monday.com")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis with name CPAM02222 does not exist"


def test_attach_third_party_link_unsupported_enum(analysis_collection):
    """Tests the attach_third_party_link function"""
    analysis_collection.collection.find_one.return_value = read_test_fixture("analysis-CPAM0002.json")
    try:
        analysis_collection.attach_third_party_link("CPAM02222", "BAD_ENUM", "https://monday.com")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Third party link type BAD_ENUM is not supported"


def test_mark_ready(analysis_collection, create_timestamp, ready_timestamp):
    """Tests the mark_ready function"""
    staging_analysis_timeline = read_test_fixture("analysis-CPAM0002.json")
    staging_analysis_timeline["timeline"] = [{
        'event': 'create',
        'timestamp': create_timestamp,
        'username': 'user01',
    }]
    analysis_collection.collection.find_one.return_value = staging_analysis_timeline
    with patch(
        "src.models.event.Event.timestamp_ready_event",
        return_value=Event(
            **{
                'event': EventType.READY,
                'timestamp': datetime.datetime(2022, 11, 10, 16, 52, 52, 301003),
                'username': 'user01',
            }
        )
    ):

        analysis_collection.mark_ready("CPAM0002", "user01")

        analysis_collection.collection.find_one_and_update.assert_called_with(
            {"name": "CPAM0002"},
            {
                "$set": {
                    "timeline": [
                        {'event': 'create', 'timestamp': create_timestamp, 'username': 'user01'},
                        {'event': EventType.READY, 'timestamp': ready_timestamp, 'username': 'user01'},
                    ]
                }
            },
            return_document=ReturnDocument.AFTER,
        )


def test_mark_ready_analysis_does_not_exist(analysis_collection):
    """Tests the mark_ready function returns an error if the analysis does not exist"""
    analysis_collection.collection.find_one.return_value = None
    try:
        analysis_collection.mark_ready("CPAM2222", "user01")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis with name CPAM2222 does not exist."


def test_mark_ready_already_marked_ready(analysis_collection, create_timestamp, ready_timestamp):
    """"tests the mark_ready function returns an error if the analysis is already marked ready"""
    staging_analysis_timeline = read_test_fixture("analysis-CPAM0002.json")
    staging_analysis_timeline["timeline"] = [
        {'event': 'create', 'timestamp': create_timestamp, 'username': 'user01'},
        {'event': 'ready', 'timestamp': ready_timestamp, 'username': 'user01'},
    ]
    analysis_collection.collection.find_one.return_value = staging_analysis_timeline
    try:
        analysis_collection.mark_ready("CPAM0002", "user01")
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == "Analysis CPAM0002 is already marked as ready!"


@pytest.fixture(name="analysis_with_no_p_dot")
def fixture_analysis_with_no_p_dot():
    """Returns an analysis with no p. in the genomic unit"""
    return {
        "name": "CPAM1111",
        "genomic_units": [{
            "gene": "VMA21",
            "transcripts": [{"transcript": "NM_001017980.3"}],
            "variants": [{
                "hgvs_variant": "NM_001017980.3:c.164G>T",
                "c_dot": "c.164G>T",
                "p_dot": "",
                "build": "GRCh38",
            }],
        }],
    }


@pytest.fixture(name="create_timestamp")
def fixture_create_timestamp():
    """Returns a create timestamp"""
    return datetime.datetime(2022, 11, 10, 16, 52, 43, 910000)


@pytest.fixture(name="ready_timestamp")
def fixture_ready_timestamp():
    """Returns a ready timestamp"""
    return datetime.datetime(2022, 11, 10, 16, 52, 52, 301003)
