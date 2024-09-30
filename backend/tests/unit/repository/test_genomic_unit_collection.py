""" Manages the genomic unit collection. Including reading, writing, fetching various genomic units. """
from unittest.mock import Mock
import copy
import pytest

from bson import ObjectId

from src.enums import GenomicUnitType


def test_find_genomic_units(genomic_unit_collection):
    """ Gets all the genomic units from the genomic unit collection """
    all_genomic_units = genomic_unit_collection.all()
    assert len(all_genomic_units) == 2


@pytest.mark.parametrize(
    "transcript_annotation_unit", [
        ('Polyphen Prediction', 'Ensembl', '112', '120', False),
        ('Polyphen Prediction', 'Ensembl', '112', '112', True),
        ('transcript_id', 'Ensembl', '', '120', False),
        ('Polyphen Prediction', 'Ensembl', '', '120', False),
    ],
    indirect=True,
    ids=["polyphen_exists_different_version", "polyphen_exists", "no_transcripts_yet", "polyphen_not_exists"]
)
def test_transcripts_annotations_exists(transcript_annotation_unit, genomic_unit_collection):
    """ Tests if a transcript annotation does not exist """
    annotation_unit, variant_in_database_json, expected = transcript_annotation_unit
    genomic_unit_collection.collection.find_one.return_value = variant_in_database_json
    actual = genomic_unit_collection.annotation_exist(annotation_unit)
    assert actual is expected


@pytest.mark.parametrize(
    "genomic_unit,dataset_name,expected", [('VMA21', 'Entrez Gene Id', True), ('VMA21', 'Entrez Gene Id', False),
                                           ('NM_001017980.3:c.164G>T', 'ClinVar_Variantion_Id', True)]
)
def test_genomic_units_annotations_exists(
    genomic_unit, dataset_name, expected, genomic_unit_collection, get_annotation_unit
):
    """ Tests if an annotation exists for a gene. This test does not utilize the JSON fixtures to verify if exists"""
    annotation_unit = get_annotation_unit(genomic_unit, dataset_name)

    genomic_unit_collection.collection.count_documents.return_value = int(expected)

    actual = genomic_unit_collection.annotation_exist(annotation_unit)

    dataset_attribute = f"annotations.{dataset_name}"
    datasource_attribute = f"{dataset_attribute}.data_source"
    version_attribute = f"{dataset_attribute}.version"

    expected_find_query = {
        annotation_unit.get_genomic_unit_type_string(): genomic_unit, dataset_attribute: {'$exists': True},
        datasource_attribute: annotation_unit.get_dataset_source(), version_attribute: annotation_unit.get_version()
    }

    genomic_unit_collection.collection.count_documents.assert_called_with(
        expected_find_query,
        limit=1,
    )
    assert actual is expected


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


@pytest.mark.parametrize(
    "genomic_unit,dataset_name,expected", [('VMA21', 'Entrez Gene Id', 'wup'), ('VMA21', 'Entrez Gene Id', None),
                                           ('NM_001017980.3:c.164G>T', 'ClinVar_Variantion_Id', 'wup2')]
)
def test_find_genomic_unit_annotation_values(
    genomic_unit, dataset_name, expected, genomic_unit_collection, get_annotation_unit
):
    """
    Finds the Genomic Unit's Annotation when the value exists within the mongo collection
    """
    annotation_unit = get_annotation_unit(genomic_unit, dataset_name)
    genomic_unit_collection.collection.find_one.return_value = {
        'annotations': [{dataset_name: [{'value': expected}]}]
    } if expected else None

    actual_value = genomic_unit_collection.find_genomic_unit_annotation_value(annotation_unit)

    genomic_unit_collection.collection.find_one.assert_called_with(
        genomic_unit_collection.__find_annotation_query__(annotation_unit),
        {f"annotations.{dataset_name}.value.$": 1, "_id": 0}
    )

    assert actual_value == expected


def test_add_transcript_to_genomic_unit(genomic_unit_collection):
    """
    Verifies adding the transcript to an HGVS variant in the collection.
    """
    genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    transcript_id = "NM_001363810.1"

    genomic_unit_collection.add_transcript_to_genomic_unit(genomic_unit, transcript_id)

    genomic_unit_collection.collection.update_one.assert_called_once_with(
        {'hgvs_variant': 'NM_001017980.3:c.164G>T'},
        {'$addToSet': {'transcripts': {'transcript_id': 'NM_001363810.1', 'annotations': []}}},
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

    expected_genomic_unit = {
        "_id": ObjectId("62fbfa5f616a9799131174ca"),
        "hgvs_variant": "NM_001017980.3:c.164G>T",
        "transcripts": [{'transcript_id': 'NM_001363810.1', 'annotations': []}],
        "annotations": {},
    }

    genomic_unit_collection.annotate_genomic_unit(genomic_unit, transcript_annotation_unit)

    genomic_unit_collection.collection.find_one_and_update.assert_called_once()
    actual_updated_genomic_unit = genomic_unit_collection.collection.find_one_and_update.call_args_list[0][0][1]['$set']
    assert actual_updated_genomic_unit == expected_genomic_unit


@pytest.mark.parametrize(
    "prepare_test_annotate", [('VMA21', 'Entrez Gene Id', "rosalution-manifest-01", 203547, False),
                              ('VMA21', 'Entrez Gene Id', "rosalution-manifest-00", 203550, True),
                              ('NM_001017980.3:c.164G>T', 'ClinVar_Variantion_Id', "2024-09-06", "581270", False)],
    indirect=True,
    ids=["new_VMA21_annotation_for_dataset", "new_VMA21_dataset", "new_variant_annotation"]
)
def test_annotate_genomic_unit(prepare_test_annotate, genomic_unit_collection):
    """
    Tests if a genomic unit's new annotation either adds a new dataset or adds the annotation to an exists dataset.
    """

    genomic_unit_json, dataset_name, genomic_annotation, annotation_unit, expected_amount = prepare_test_annotate

    genomic_unit_collection.collection.find_one.return_value = genomic_unit_json

    genomic_unit_collection.annotate_genomic_unit(annotation_unit.genomic_unit, genomic_annotation)

    updated_genomic_unit = genomic_unit_collection.collection.find_one_and_update.call_args_list[0][0][1]['$set']
    annotations = updated_genomic_unit['annotations']
    actual_updated_dataset = next((dataset for dataset in annotations if dataset_name in dataset), None)

    assert actual_updated_dataset is not None

    assert len(actual_updated_dataset[dataset_name]) == expected_amount

    def is_entry(entry):
        return entry['data_source'] == genomic_annotation['data_source'] and entry['version'] == genomic_annotation[
            'version']

    actual_updated_annotation = next((entry for entry in actual_updated_dataset[dataset_name] if is_entry(entry)), None)

    assert actual_updated_annotation is not None
    assert actual_updated_annotation['value'] == genomic_annotation['value']


def test_annotation_genomic_unit_with_file(genomic_unit_collection, get_annotation_json):
    """ Accepts a file and adds it as an annotation to the given genomic unit """
    genomic_unit = get_annotation_json('NM_001017980.3:c.164G>T', GenomicUnitType.HGVS_VARIANT)
    incoming_genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    annotation_unit = {
        "data_set": 'GeneHomology_Multi-SequenceAlignment', "data_source": "rosalution_manual", "version": "1979-01-01",
        "value": {"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}
    }

    expected_annotation_update = {
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    }

    expected_genomic_unit = genomic_unit
    expected_genomic_unit['annotations'].append(expected_annotation_update)

    genomic_unit_collection.collection.find_one.return_value = genomic_unit

    genomic_unit_collection.annotate_genomic_unit_with_file(incoming_genomic_unit, annotation_unit)

    genomic_unit_collection.collection.find_one_and_update.assert_called_once()
    actual_updated_genomic_unit = genomic_unit_collection.collection.find_one_and_update.call_args_list[0][0][1]['$set']
    assert actual_updated_genomic_unit == expected_genomic_unit


def test_update_existing_genomic_unit_file_annotation(genomic_unit_collection, get_annotation_json):
    """ Updates an existing file annotation with a new file annotation in place"""
    genomic_unit = get_annotation_json('NM_001017980.3:c.164G>T', GenomicUnitType.HGVS_VARIANT)
    incoming_genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    annotation_unit_value = {"file_id": "fake-image-id-2", "created_date": "1979-01-01 00:00:00"}
    data_set = 'GeneHomology_Multi-SequenceAlignment'
    file_id_old = "fake-image-id-1"

    expected_genomic_unit = copy.copy(genomic_unit)

    genomic_unit['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    })

    genomic_unit_collection.collection.find_one.return_value = genomic_unit

    expected_annotation_update = {
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-2", "created_date": "1979-01-01 00:00:00"}]
        }]
    }

    expected_genomic_unit['annotations'].append(expected_annotation_update)

    genomic_unit_collection.update_genomic_unit_file_annotation(
        incoming_genomic_unit, data_set, annotation_unit_value, file_id_old
    )

    genomic_unit_collection.collection.find_one_and_update.assert_called_once()
    actual_updated_genomic_unit = genomic_unit_collection.collection.find_one_and_update.call_args_list[0][0][1]['$set']
    assert actual_updated_genomic_unit == expected_genomic_unit


def test_remove_existing_genomic_unit_file_annotation(genomic_unit_collection, get_annotation_json):
    """ Accepts a request to remove an existing file annotation """
    genomic_unit_json = get_annotation_json('NM_001017980.3:c.164G>T', GenomicUnitType.HGVS_VARIANT)
    incoming_genomic_unit = {'unit': 'NM_001017980.3:c.164G>T', 'type': GenomicUnitType.HGVS_VARIANT}
    data_set = 'GeneHomology_Multi-SequenceAlignment'
    file_id = "fake-image-id-1"

    expected_genomic_unit = copy.deepcopy(genomic_unit_json)

    genomic_unit_json['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01",
            "value": [{"file_id": "fake-image-id-1", "created_date": "1979-01-01 00:00:00"}]
        }]
    })

    genomic_unit_collection.collection.find_one.return_value = genomic_unit_json

    expected_genomic_unit['annotations'].append({
        "GeneHomology_Multi-SequenceAlignment": [{
            "data_source": "rosalution_maual", "version": "1979-01-01", "value": []
        }]
    })

    genomic_unit_collection.remove_genomic_unit_file_annotation(incoming_genomic_unit, data_set, file_id)

    genomic_unit_collection.collection.find_one_and_update.assert_called_once()
    actual_updated_genomic_unit = genomic_unit_collection.collection.find_one_and_update.call_args_list[0][0][1]['$set']
    assert actual_updated_genomic_unit == expected_genomic_unit


@pytest.fixture(name="prepare_test_annotate", scope="function")
def prepare_test_annotate_genomic_units(request, get_annotation_unit, get_annotation_json):
    """ Provides a genomic unit from the genomic unit collection, otherwise returns false"""

    genomic_unit, dataset_name, version, value, remove_dataset = request.param

    annotation_unit = get_annotation_unit(genomic_unit, dataset_name)
    annotation_unit.set_latest_version(version)

    genomic_unit_json = get_annotation_json(genomic_unit, annotation_unit.genomic_unit['type'])
    if remove_dataset:
        genomic_unit_json['annotations'] = [
            dataset for dataset in genomic_unit_json['annotations'] if dataset_name not in dataset
        ]

    genomic_annotation = {
        "data_set": annotation_unit.get_dataset_name(),
        "data_source": annotation_unit.get_dataset_source(),
        "version": annotation_unit.get_version(),
        "value": value,
    }

    expected_annotation_amount = 1 if remove_dataset else 2

    return (genomic_unit_json, dataset_name, genomic_annotation, annotation_unit, expected_annotation_amount)


@pytest.fixture(name="transcript_annotation_unit", scope="function")
def variant_with_datasets_annotation_unit(request, get_annotation_unit, get_annotation_json):
    """ Fixture that creates generates the test data for verifying transcript annotation operations"""
    dataset, data_source, existing_version, calculated_version, expected = request.param

    annotation_unit = get_annotation_unit('NM_001017980.3:c.164G>T', dataset)
    annotation_unit.version = calculated_version

    variant_in_database_json = get_annotation_json("NM_001017980.3:c.164G>T", GenomicUnitType.HGVS_VARIANT)

    if existing_version:
        for transcript_annotation in variant_in_database_json['transcripts']:
            if dataset in transcript_annotation:
                transcript_annotation[dataset].data_source = data_source
                transcript_annotation[dataset].version = existing_version
    elif dataset == 'transcript_id':
        variant_in_database_json['transcripts'] = []
    else:
        for transcript in variant_in_database_json['transcripts']:
            transcript['annotations'] = [
                annotation for annotation in transcript['annotations'] if dataset not in annotation
            ]

    return (annotation_unit, variant_in_database_json, expected)
