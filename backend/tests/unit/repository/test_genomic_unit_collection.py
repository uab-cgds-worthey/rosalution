""" Manages the genomic unit collection. Including reading, writing, fetching various genomic units. """
from unittest.mock import Mock
import copy
import pytest

from bson import ObjectId

from src.enums import GenomicUnitType
from src.repository.genomic_unit_collection import GenomicUnitCollection

from ...test_utils import mock_mongo_collection, read_database_fixture


def test_find_genomic_units(genomic_unit_collection):
    """ Gets all the genomic units from the genomic unit collection """
    all_genomic_units = genomic_unit_collection.all()
    assert len(all_genomic_units) == 14


def test_transcript_annotation_not_exist_with_no_annotations(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Tests if a transcript that has no annotations will return false on a test"""
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    dataset = {'data_set': 'fake_annotation_not_exist', 'transcript': True}

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json

    actual = genomic_unit_collection.annotation_exist(genomic_unit, dataset)

    assert actual is False


def test_transcript_annotation_not_exist(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Tests if a transcript annotation does not exist """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    dataset = {'data_set': 'Polyphen Prediction', 'transcript': True}

    hgvs_variant_genomic_unit_json['transcripts'] = [{
        'transcript_id': 'NM_001017980.3',
        'annotations': [{'transcript_id': {
            'data_source': 'Ensembl',
            'version': '0.0',
            'value': 'NM_001017980.3',
        }}]
    }]

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json

    actual = genomic_unit_collection.annotation_exist(genomic_unit, dataset)

    assert actual is False


def test_transcript_annotation_exist(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Tests if there is an annotation for a transcript """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    dataset = {'data_set': 'transcript_id', 'transcript': True}

    hgvs_variant_genomic_unit_json['transcripts'] = [{
        'transcript_id': 'NM_001017980.3',
        'annotations': [{'transcript_id': {
            'data_source': 'Ensembl',
            'version': '0.0',
            'value': 'NM_001017980.3',
        }}]
    }]

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json

    actual = genomic_unit_collection.annotation_exist(genomic_unit, dataset)

    assert actual is True


def test_annotation_exists_for_gene(genomic_unit_collection):
    """ Tests if an annotation exists for a gene. This test does not utilize the JSON fixtures to verify if exists"""
    genomic_unit = {'unit': 'VMA21', 'type': GenomicUnitType.GENE}
    dataset = {'data_set': "Entrez Gene Id"}

    genomic_unit_collection.collection.count_documents.return_value = 1

    actual = genomic_unit_collection.annotation_exist(genomic_unit, dataset)

    genomic_unit_collection.collection.count_documents.assert_called_with(
        {"gene": "VMA21", "annotations.Entrez Gene Id": {'$exists': True}},
        limit=1,
    )
    assert actual is True


def test_annotation_does_not_exist_for_gene(genomic_unit_collection):
    """
    Tests if an annotation does not exist for a gene.  This test does not utilize the JSON fixtures to verify if exists
    """
    genomic_unit = {'unit': 'VMA21', 'type': GenomicUnitType.GENE}
    dataset = {'data_set': "HPO"}

    genomic_unit_collection.collection.count_documents.return_value = 0

    actual = genomic_unit_collection.annotation_exist(genomic_unit, dataset)
    genomic_unit_collection.collection.count_documents.assert_called_with(
        {"gene": "VMA21", "annotations.HPO": {'$exists': True}},
        limit=1,
    )
    assert actual is False


def test_find_genomic_unit_with_transcript_id(genomic_unit_collection):
    """
    Verifies that the find_genomic_unit_with_transcript_id function gets called with the correct parameters
    """
    genomic_unit = {
        'unit': 'NM_001017980.3:c.164G>T',
        'type': GenomicUnitType.HGVS_VARIANT,
    }
    transcript_id = "NM_001363810.1"

    genomic_unit_collection.find_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

    genomic_unit_collection.collection.find_one.assert_called_with({
        "hgvs_variant": "NM_001017980.3:c.164G>T",
        "transcripts.transcript_id": "NM_001363810.1",
    })


def test_find_genomic_unit_annotation_value_when_exists(genomic_unit_collection, vma21_genomic_unit):
    """
    Finds the Genomic Unit's Annotation when the value exists within the mongo collection
    """
    genomic_unit = {'unit': 'VMA21', 'type': GenomicUnitType.GENE}
    dataset = "Eat-Tacos"

    genomic_unit_collection.collection.find_one.return_value = vma21_genomic_unit

    actual_value = genomic_unit_collection.find_genomic_unit_annotation_value(genomic_unit, dataset)

    genomic_unit_collection.collection.find_one.assert_called_with({
        "gene": "VMA21",
        'annotations.Eat-Tacos': {'$exists': True},
    })

    expected_vma21_entrez_gene_id = None
    assert actual_value == expected_vma21_entrez_gene_id


def test_find_genomic_unit_annotation_value_when_unit_not_exist(genomic_unit_collection):
    """
    Fails to find the Genomic Unit's Annotation when the value does not exist within the mongo collection
    """
    genomic_unit = {'unit': 'PEX10', 'type': GenomicUnitType.GENE}
    dataset = "Entrez Gene Id"

    genomic_unit_collection.collection.find_one.return_value = None

    actual_value = genomic_unit_collection.find_genomic_unit_annotation_value(genomic_unit, dataset)

    genomic_unit_collection.collection.find_one.assert_called_with({
        "gene": "PEX10",
        'annotations.Entrez Gene Id': {'$exists': True},
    })

    assert actual_value is None


def test_update_genomic_unit_with_transcript_id(genomic_unit_collection):
    """
    Verifies that the update_genomic_unit_with_transcript_id function makes the pymongo call with the correct params
    """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    transcript_id = "NM_001363810.1"

    genomic_unit_collection.update_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        {'hgvs_variant': 'NM_001017980.3:c.164G>T'},
        {'$addToSet': {'transcripts': {'transcript_id': 'NM_001363810.1', 'annotations': []}}},
    )


def test_update_genomic_unit_with_mongo_id(genomic_unit_collection):
    """
    Verifies that the update genomic unit with mongo id function makes the pymongo call with the correct params
    """
    genomic_unit_document = {
        "_id": ObjectId('62fbfa5f616a9799131174c8'),
        "hgvs_variant": "NM_001017980.3:c.164G>T",
        "transcripts": [],
        "annotations": {},
    }

    genomic_unit_collection.update_genomic_unit_with_mongo_id(genomic_unit_document)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        {'_id': ObjectId('62fbfa5f616a9799131174c8')},
        {'$set': genomic_unit_document},
    )


def test_annotate_transcript_genomic_unit(genomic_unit_collection):
    """ Verifies that a transcript annotates a genomic unit properly """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    transcript_annotation_unit = {
        "data_set": "SIFT Prediction",
        "data_source": "Ensembl",
        "version": "",
        "value": "deleterious",
        "transcript_id": "NM_001017980.4",
    }

    genomic_unit_collection.find_genomic_unit_with_transcript_id = Mock(
        return_value={
            "_id": ObjectId("62fbfa5f616a9799131174ca"),
            "hgvs_variant": "NM_001017980.3:c.164G>T",
            "transcripts": [{'transcript_id': 'NM_001363810.1', 'annotations': []}],
            "annotations": {},
        }
    )

    genomic_unit_collection.annotate_genomic_unit(genomic_unit, transcript_annotation_unit)

    genomic_unit_collection.collection.update_one.assert_called_once_with({'_id':
        ObjectId("62fbfa5f616a9799131174ca")}, {
            '$set': {
                "_id": ObjectId("62fbfa5f616a9799131174ca"),
                "hgvs_variant": "NM_001017980.3:c.164G>T",
                "transcripts": [{'transcript_id': 'NM_001363810.1', 'annotations': []}],
                "annotations": {},
            }
        })


def test_annotation_genomic_unit_with_file(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Accepts a file and adds it as an annotation to the given genomic unit """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    annotation_unit = {
        "data_set": 'GeneHomology_Multi-SequenceAlignment', "data_source": "rosalution_manual",
        "version": "1979-01-01", "value": {"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}
    }

    expected_annotation_update = {
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    }

    expected_genomic_unit = hgvs_variant_genomic_unit_json
    expected_genomic_unit['annotations'].append(expected_annotation_update)

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json
    genomic_unit_collection.update_genomic_unit_with_mongo_id = Mock()

    genomic_unit_collection.annotate_genomic_unit_with_file(genomic_unit, annotation_unit)

    genomic_unit_collection.update_genomic_unit_with_mongo_id.assert_called_once_with(expected_genomic_unit)


def test_update_existing_genomic_unit_file_annotation(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Updates an existing file annotation with a new file annotation in place"""
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    annotation_unit_value = {"file_id": "fake-image-id-2", "created_date": "1979-01-01 00:00:00"}
    data_set = 'GeneHomology_Multi-SequenceAlignment'
    file_id_old = "fake-image-id-1"

    expected_genomic_unit = copy.copy(hgvs_variant_genomic_unit_json)

    hgvs_variant_genomic_unit_json['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    })

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json

    expected_annotation_update = {
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-2", "created_date": "1979-01-01 00:00:00"}]
        }]
    }

    expected_genomic_unit['annotations'].append(expected_annotation_update)

    genomic_unit_collection.update_genomic_unit_with_mongo_id = Mock()

    genomic_unit_collection.update_genomic_unit_file_annotation(
        genomic_unit, data_set, annotation_unit_value, file_id_old
    )

    genomic_unit_collection.update_genomic_unit_with_mongo_id.assert_called_once_with(expected_genomic_unit)


def test_remove_existing_genomic_unit_file_annotation(genomic_unit_collection, hgvs_variant_genomic_unit_json):
    """ Accepts a request to remove an existing file annotation """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    data_set = 'GeneHomology_Multi-SequenceAlignment'
    file_id = "fake-image-id-1"

    expected_genomic_unit = copy.deepcopy(hgvs_variant_genomic_unit_json)

    hgvs_variant_genomic_unit_json['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    })

    genomic_unit_collection.collection.find_one.return_value = hgvs_variant_genomic_unit_json

    expected_genomic_unit['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01", "value": []
        }]
    })

    genomic_unit_collection.update_genomic_unit_with_mongo_id = Mock()

    genomic_unit_collection.remove_genomic_unit_file_annotation(genomic_unit, data_set, file_id)

    genomic_unit_collection.update_genomic_unit_with_mongo_id.assert_called_once_with(expected_genomic_unit)


@pytest.fixture(name="hgvs_variant_genomic_unit_json")
def fixture_hgvs_genomic_unit_json(genomic_units_json):
    """ Returns the genomic unit for VMA21 Gene"""
    return next((
        unit for unit in genomic_units_json
        if 'hgvs_variant' in unit and unit['hgvs_variant'] == "NM_001017980.3:c.164G>T"
    ), None)


@pytest.fixture(name="vma21_genomic_unit")
def fixture_vma21_genomic_unit_json(genomic_units_json):
    """ Returns the genomic unit for VMA21 Gene"""
    return next((unit for unit in genomic_units_json if 'gene' in unit and unit['gene'] == "VMA21"), None)


@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection(genomic_units_json):
    """ Returns a genomic unit collection """

    mock_collection = mock_mongo_collection()
    mock_collection.find.return_value = genomic_units_json

    return GenomicUnitCollection(mock_collection)


@pytest.fixture(name="genomic_units_json")
def fixture_genomic_units_json():
    """ Returns the JSON for the genomic units used to seed the MongoDB database """
    return read_database_fixture("genomic-units.json")
