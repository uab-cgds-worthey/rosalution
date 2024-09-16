"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
import logging

# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
from bson import ObjectId
from pymongo import ReturnDocument

from src.core.annotation_unit import AnnotationUnit

# create logger
logger = logging.getLogger(__name__)


def transcript_unit_exist(dataset, data_source, version, annotation):
    """Helper method to evaluate if transcript annotations have existing annotation"""
    if dataset not in annotation:
        return False

    annotation_unit_match = next(
        (unit for unit in annotation[dataset] if unit['data_source'] == data_source and unit['version'] == version),
        None
    )

    return annotation_unit_match is not None


class GenomicUnitCollection:
    """ Repository for managing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection

    def __find_genomic_unit_query__(self, annotation_unit: AnnotationUnit):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        genomic_unit_type_string = annotation_unit.get_genomic_unit_type_string()
        genomic_unit_name = annotation_unit.get_genomic_unit()
        return {genomic_unit_type_string: genomic_unit_name}

    def __find_annotation_query__(self, annotation_unit: AnnotationUnit):
        """
            find_query = {
              'gene': 'VMA21',
              'annotations.CADD': {'$exists': True },
              'annotations.CADD.data_source': 'Ensembl',
              'annotations.CADD.version': '112'
            }
        """
        find_query = self.__find_genomic_unit_query__(annotation_unit)
        data_set_name = annotation_unit.get_dataset_name()
        dataset_attribute_base = f"annotations.{data_set_name}"
        datasource_attribute = f"{dataset_attribute_base}.data_source"
        version_attribute = f"{dataset_attribute_base}.version"

        return {
            **find_query, **{
                dataset_attribute_base: {'$exists': True}, datasource_attribute: annotation_unit.get_dataset_source(),
                version_attribute: annotation_unit.get_version()
            }
        }

    def all(self):
        """ Returns all genomic units that are currently stored """
        return self.collection.find()

    def annotation_exist(self, annotation_unit: AnnotationUnit):
        """ Returns true if the genomic_unit already has that dataset annotated """
        data_set_name = annotation_unit.get_dataset_name()
        dataset_version = annotation_unit.get_version()
        dataset_source = annotation_unit.get_dataset_source()

        find_query = self.__find_genomic_unit_query__(annotation_unit)

        if annotation_unit.is_transcript_dataset():
            hgvs_genomic_unit = self.collection.find_one(find_query)

            for transcript in hgvs_genomic_unit['transcripts']:
                dataset_in_transcript_annotation = next((
                    annotation for annotation in transcript['annotations']
                    if transcript_unit_exist(data_set_name, dataset_source, dataset_version, annotation)
                ), None)
                if not dataset_in_transcript_annotation:
                    return False

            return True

        find_query = self.__find_annotation_query__(annotation_unit)

        return bool(self.collection.count_documents(find_query, limit=1))

    def find_genomic_unit_annotation_value(self, annotation_unit: AnnotationUnit):
        """ Returns the annotation value for a genomic unit according the the dataset"""

        dataset_name = annotation_unit.get_dataset_name()
        find_query = self.__find_annotation_query__(annotation_unit)

        projection = {f"annotations.{dataset_name}.value.$": 1, "_id": 0}
        result = self.collection.find_one(find_query, projection)

        if result is None:
            return None

        return next((
            annotation[dataset_name][0].get('value')
            for annotation in result['annotations']
            if dataset_name in annotation
        ), None)

    def find_genomic_unit(self, genomic_unit):
        """ Returns the given genomic unit from the genomic unit collection """
        return self.collection.find_one({
            genomic_unit['type'].value: genomic_unit['unit'],
        })

    def find_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Returns the genomic unit with the corresponding transcript if it exists """
        return self.collection.find_one({
            genomic_unit['type'].value: genomic_unit['unit'],
            'transcripts.transcript_id': transcript_id,
        })

    def add_transcript_to_genomic_unit(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        return self.collection.update_one(
            {genomic_unit['type'].value: genomic_unit['unit']},
            {'$addToSet': {'transcripts': {'transcript_id': transcript_id, 'annotations': []}}},
        )

    def update_genomic_unit_annotation_by_mongo_id(self, genomic_unit_document):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit_document['_id']

        return self.collection.find_one_and_update({'_id': ObjectId(str(genomic_unit_id))},
                                                   {'$set': genomic_unit_document},
                                                   return_document=ReturnDocument.AFTER)

    def annotate_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Takes a genomic_unit from an annotation task as well as a genomic_annotation and arranges them in a pattern
        that can be sent to mongo to update the genomic unit's document in the collection
        """

        annotation_data_set = {
            genomic_annotation['data_set']: [{
                'data_source': genomic_annotation['data_source'],
                'version': genomic_annotation['version'],
                'value': genomic_annotation['value'],
            }]
        }

        updated_document = None

        if 'transcript_id' in genomic_annotation:
            genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                genomic_unit, genomic_annotation['transcript_id']
            )

            if not genomic_unit_document:
                self.add_transcript_to_genomic_unit(genomic_unit, genomic_annotation['transcript_id'])
                genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                    genomic_unit, genomic_annotation['transcript_id']
                )

            for transcript in genomic_unit_document['transcripts']:
                if transcript['transcript_id'] == genomic_annotation['transcript_id']:
                    transcript['annotations'].append(annotation_data_set)

            updated_document = self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

        else:
            genomic_unit_document = self.find_genomic_unit(genomic_unit)
            genomic_unit_document['annotations'].append(annotation_data_set)
            updated_document = self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

        return updated_document

    def annotate_genomic_unit_with_file(self, genomic_unit, genomic_annotation):
        """ Ensures that an annotation is created for the annotation image upload and only one image is allowed """

        genomic_unit_document = self.find_genomic_unit(genomic_unit)
        data_set = genomic_annotation['data_set']

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                annotation[data_set][0]['value'].append(genomic_annotation['value'])
                return self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

        annotation_data_set = {
            genomic_annotation['data_set']: [{
                'data_source': genomic_annotation['data_source'],
                'version': genomic_annotation['version'],
                'value': [genomic_annotation['value']],
            }]
        }

        genomic_unit_document['annotations'].append(annotation_data_set)
        return self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

    def update_genomic_unit_file_annotation(self, genomic_unit, data_set, annotation_value, file_id_old):
        """ Replaces existing annotation image with new image """

        genomic_unit_document = self.find_genomic_unit(genomic_unit)

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                for i in range(len(annotation[data_set][0]['value'])):
                    if annotation[data_set][0]['value'][i]['file_id'] == file_id_old:
                        annotation[data_set][0]['value'].pop(i)
                        annotation[data_set][0]['value'].append(annotation_value)
                        break

        self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

        return

    def remove_genomic_unit_file_annotation(self, genomic_unit, data_set, file_id):
        """ Removes a file that has been added as an annotation to a genomic unit """

        genomic_unit_document = self.find_genomic_unit(genomic_unit)

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                for i in range(len(annotation[data_set][0]['value'])):
                    if annotation[data_set][0]['value'][i]['file_id'] == file_id:
                        annotation[data_set][0]['value'].pop(i)
                        break

        return self.update_genomic_unit_annotation_by_mongo_id(genomic_unit_document)

    def create_genomic_unit(self, genomic_unit):
        """
        Takes a genomic_unit and adds it to the collection if it doesn't already exist (exact match).
        """

        # Make sure the genomic unit doesn't already exist
        if self.collection.find_one(genomic_unit):
            logging.info("Genomic unit already exists, skipping creation")
            return

        self.collection.insert_one(genomic_unit)
        return
