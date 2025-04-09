"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
import json
import logging
from types import NoneType

from bson import ObjectId
from pymongo import ReturnDocument

from src.enums import GenomicUnitType
from src.core.annotation_unit import AnnotationUnit

from .genomic_unit_collection_transcripts_adapter import GenomicUnitCollectionForTranscripts
from .genomic_unit_collection_files_adapter import GenomicUnitCollectionForFiles


logger = logging.getLogger(__name__)


class GenomicUnitQuery():
    def __init__(self, genomic_unit, genomic_annotation):
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation
        self.dataset_name = self.genomic_annotation['data_set']
    
    def create_annotation_entry(self):
        """ Helper method that restructures a dataset and the queried annotation into an entry for MongoDBc"""

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        new_dataset_entry = {
            self.dataset_name: [annotation_entry]
        }

        return new_dataset_entry, annotation_entry
    
    def find_dataset_in_genomic_unit(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """

        dataset_exists = f"annotations.{self.dataset_name}"

        return {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            dataset_exists: {'$exists': True }
        }
        
class AnnotationUnitQuery():
    def __init__(self, annotation_unit):
        self.annotation_unit = annotation_unit
    
    def find_genomic_unit_query(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        genomic_unit_type_string = self.annotation_unit.get_genomic_unit_type_string()
        genomic_unit_name = self.annotation_unit.get_genomic_unit()
        return {genomic_unit_type_string: genomic_unit_name}

    def find_dataset_query(self):
        genomic_unit_query = self.find_genomic_unit_query()

        data_set_name = self.annotation_unit.get_dataset_name()
        dataset_property = f"annotations.{data_set_name}"
        genomic_unit_query[dataset_property] = {'$exists': True}

    def find_annotation_query(self):
        """
            find_query = {
              'gene': 'VMA21',
              'annotations.CADD': {'$exists': True },
              'annotations.CADD.data_source': 'Ensembl',
              'annotations.CADD.version': '112'
            }
        """
        find_query = self.find_genomic_unit_query()
        data_set_name = self.annotation_unit.get_dataset_name()
        dataset_attribute_base = f"annotations.{data_set_name}"
        datasource_attribute = f"{dataset_attribute_base}.data_source"
        version_attribute = f"{dataset_attribute_base}.version"

        find_query[dataset_attribute_base] = {'$exists': True}
        find_query[datasource_attribute] = self.annotation_unit.get_dataset_source()
        find_query[version_attribute] = self.annotation_unit.get_version()
        return find_query

    def find_annotation_value_projection(self):
        return {f"annotations.{self.annotation_unit.get_dataset_name()}.value.$": 1, "_id": 0}
    
class GenomicUnitCollection:
    """ Repository for managing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection
        self.transcript_adapter = GenomicUnitCollectionForTranscripts(self)
        self.file_adapter = GenomicUnitCollectionForFiles(self)

    def all(self):
        """ Returns all genomic units that are currently stored """
        return self.collection.find()

    def annotation_exist(self, annotation_unit: AnnotationUnit):
        """ Returns true if the genomic_unit already has that dataset annotated """
        if annotation_unit.is_transcript_dataset():
            return self.transcript_adapter.annotation_exist(annotation_unit)

        data_set_name = annotation_unit.get_dataset_name()

        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)
        find_query = annotation_query_adapter.find_annotation_query(annotation_unit)
        
        if( data_set_name == 'pos'):
            logger.warning(find_query)
            logger.warning('why did it fail to find the annotation for this')

        return bool(self.collection.count_documents(find_query, limit=1))

    def find_genomic_unit_annotation_value(self, annotation_unit: AnnotationUnit):
        """ Returns the annotation value for a genomic unit according the the dataset"""

        dataset_name = annotation_unit.get_dataset_name()
        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)

        find_query = annotation_query_adapter.find_annotation_query()
        projection = annotation_query_adapter.find_annotation_value_projection()
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
        return self.transcript_adapter.find_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

    def update_genomic_unit_by_mongo_id(self, genomic_unit_document):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit_document['_id']

        return self.collection.find_one_and_update({'_id': ObjectId(str(genomic_unit_id))},
                                                   {'$set': genomic_unit_document},
                                                   return_document=ReturnDocument.AFTER)

    # def query_if_genomic_unit_has_dataset(self,):

    def annotate_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Takes a genomic_unit from an annotation task as well as a genomic_annotation and arranges them in a pattern
        that can be sent to mongo to update the genomic unit's document in the collection.  Saves annotation as the
        following example

        example:
        {
            'Entrez Gene Id': [{
                'data_source': 'Rosalution',
                'version': 'rosalution-manifest-00',
                'value': 203547   
            }]
        }
        """

        if 'transcript_id' in genomic_annotation:
            return self.transcript_adapter.annotate_transcript_dataset(genomic_unit, genomic_annotation)

        dataset_name = genomic_annotation['data_set']

        genomic_unit_query = GenomicUnitQuery(genomic_unit, genomic_annotation)
        genomic_unit_query.find_genomic_unity_query()

        # genomic_unit_json = self.find_genomic_unit(genomic_unit)
        # self.__add_to_annotations_from_document(genomic_unit_json['annotations'], dataset_name, genomic_annotation)

        # updated_document = self.update_genomic_unit_by_mongo_id(genomic_unit_json)

        return updated_document


    def __add_to_annotations_from_document(self, list_of_annotations, dataset_name, genomic_annotation):
        new_dataset_entry, annotation_entry = create_annotation_entry(dataset_name, genomic_annotation)

        existing_dataset = next((dataset for dataset in list_of_annotations if dataset_name in dataset), None)
        if existing_dataset:
            existing_dataset[dataset_name].append(annotation_entry)
        else:
            list_of_annotations.append(new_dataset_entry)

        return list_of_annotations

    def annotate_genomic_unit_with_file(self, genomic_unit, genomic_annotation):
        """ Ensures that an annotation is created for the annotation image upload and only one image is allowed """

        return self.file_adapter.annotate_genomic_unit_with_file(genomic_unit, genomic_annotation)


    def update_genomic_unit_file_annotation(self, genomic_unit, data_set, annotation_value, file_id_old):
        """ Replaces existing annotation image with new image """
        self.file_adapter.update_genomic_unit_file_annotation(genomic_unit, data_set, annotation_value, file_id_old)
        return

    def remove_genomic_unit_file_annotation(self, genomic_unit, data_set, file_id):
        """ Removes a file that has been added as an annotation to a genomic unit """

        return self.file_adapter.remove_genomic_unit_file_annotation(genomic_unit, data_set, file_id)


    def create_genomic_unit(self, genomic_unit):
        """
        Takes a genomic_unit and adds it to the collection if it doesn't already exist (exact match).
        """
        type_to_save = GenomicUnitType.string_types() & genomic_unit.keys()

        if len(type_to_save) != 1:
            logger.error(
                'Failed to create new Genomic Unit "%s", contains more then one genomic_unit type', genomic_unit
            )
            return

        genomic_unit_type = type_to_save.pop()
        find_query = {genomic_unit_type: genomic_unit[genomic_unit_type]}

        if self.collection.find_one(find_query):
            logger.info("Genomic unit already exists, skipping creation")
            return

        self.collection.insert_one(genomic_unit)
        return
