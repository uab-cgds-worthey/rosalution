"""
Manages the genomic units and their subsequent annotations within MongoDB.
"""
import logging

from bson import ObjectId
from pymongo import ReturnDocument

from src.enums import GenomicUnitType
from src.core.annotation_unit import AnnotationUnit

from .genomic_unit_collection_for_transcripts import GenomicUnitCollectionForTranscripts

logger = logging.getLogger(__name__)


class GenomicUnitQuery():
    """
    Represents the MongoDB query's filter and update arguments of an AnnotationUnit.
    """

    def __init__(self, genomic_unit, genomic_annotation):
        """Initializes this query builder with the genomic unit and the gathered annotation."""
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation

    @property
    def dataset_name(self):
        """Returns the name of the dataset for the genomic unit's annotation"""
        return self.genomic_annotation['data_set']

    def provision_dataset_query_and_update(self):
        """Constructs a query's filter and update MongoDB arguments to provision a dataset for a genomic unit."""

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            f"annotations.{self.dataset_name}": {'$exists': False}
        }

        update_operation = {'$addToSet': {"annotations": {self.dataset_name: []}}}

        return query_filter, update_operation

    def annotate_dataset_query_and_update(self):
        """
        Constructs a query's filter, update, and arraysFilter MongoDB arguments to annotate a dataset
        for a genomic unit.
        """

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            f"annotations.{self.dataset_name}": {'$exists': True}
        }

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        update_operation = {'$addToSet': {f"annotations.$[dataset].{self.dataset_name}": annotation_entry}}

        arrays_filter = [{f"dataset.{self.dataset_name}": {'$exists': True}}]

        return query_filter, update_operation, arrays_filter


class AnnotationUnitQuery():
    """
    Represents the MongoDB query's filter and update arguments for an AnnotationUnit.
    """

    def __init__(self, annotation_unit: AnnotationUnit):
        """Initializes this query builder with an AnnotationUnit"""
        self.annotation_unit = annotation_unit

    def find_annotation_query(self):
        """
        Constructs the find filter to query MongoDB for the annotation unit for by its genomic unit name,
        dataset, data source, and calculated version.

        find_query = {
            'gene': 'VMA21',
            'annotations.CADD': {'$exists': True },
            'annotations.CADD.data_source': 'Ensembl',
            'annotations.CADD.version': '112'
        }
        """
        genomic_unit_type_string = self.annotation_unit.get_genomic_unit_type_string()
        genomic_unit_name = self.annotation_unit.get_genomic_unit()
        data_set_name = self.annotation_unit.get_dataset_name()

        find_query = {
            genomic_unit_type_string: genomic_unit_name, f"annotations.{data_set_name}": {'$exists': True},
            f"annotations.{data_set_name}.data_source": self.annotation_unit.get_dataset_source(),
            f"annotations.{data_set_name}.version": self.annotation_unit.version
        }

        return find_query

    def find_annotation_value_projection(self):
        """
        Constructs the find projection MongoDB argument for an annotation unit's value by its genomic unit name,
        dataset, data source, and calculated version.

        find_query = {
            'gene': 'VMA21',
            'annotations.CADD': {'$exists': True },
            'annotations.CADD.data_source': 'Ensembl',
            'annotations.CADD.version': '112'
        }
        """
        return {f"annotations.{self.annotation_unit.get_dataset_name()}.$": 1, "_id": 0}


class GenomicUnitCollection:
    """ Repository for managing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the 'genomic_units' collection"""
        self.collection = genomic_units_collection

    def all(self):
        """ Returns all genomic units that are stored """
        return self.collection.find()

    def annotation_exist(self, annotation_unit: AnnotationUnit):
        """ 
        Returns True if the the genomic unit is annotated by a genomic unit's name, dataset, data source, and
        calculated version, otherwise returns False.
        """
        if annotation_unit.is_transcript_dataset():
            collection_for_transcripts = GenomicUnitCollectionForTranscripts(self)
            return collection_for_transcripts.annotation_exist(annotation_unit)

        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)
        find_query = annotation_query_adapter.find_annotation_query()

        return bool(self.collection.count_documents(find_query, limit=1))

    def find_genomic_unit_annotation_value(self, annotation_unit: AnnotationUnit):
        """
        Returns the annotation value for a genomic unit according the the dataset, datasource, and calculated version.
        Returns None if the annotation does not exist for the genomic unit.
        """

        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)

        find_query = annotation_query_adapter.find_annotation_query()
        projection = annotation_query_adapter.find_annotation_value_projection()
        result = self.collection.find_one(find_query, projection)

        if result is None:
            return None

        dataset_name = annotation_unit.get_dataset_name()
        dataset_annotations = next((dataset for dataset in result['annotations'] if dataset_name in dataset), None)

        if not dataset_annotations:
            return None

        return next((
            annotation['value']
            for annotation in dataset_annotations[dataset_name]
            if annotation_unit.does_source_and_version_match(annotation['data_source'], annotation['version'])
        ), None)

    def find_genomic_unit(self, genomic_unit):
        """ Returns the given genomic unit from the genomic unit collection """
        return self.collection.find_one({
            genomic_unit['type'].value: genomic_unit['unit'],
        })

    def update_genomic_unit_by_mongo_id(self, genomic_unit_document):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit_document['_id']

        return self.collection.find_one_and_update({'_id': ObjectId(str(genomic_unit_id))},
                                                   {'$set': genomic_unit_document},
                                                   return_document=ReturnDocument.AFTER)

    def annotate_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Annotates a genomic unit with the dataset value from an annotation task. Saves annotation as the
        following example.

        Example:
        {
            'Entrez Gene Id': [{
                'data_source': 'Rosalution',
                'version': 'rosalution-manifest-00',
                'value': 203547   
            }]
        }
        """

        if 'transcript_id' in genomic_annotation:
            collection_for_transcripts = GenomicUnitCollectionForTranscripts(self)
            return collection_for_transcripts.annotate_transcript_dataset(genomic_unit, genomic_annotation)

        genomic_unit_query = GenomicUnitQuery(genomic_unit, genomic_annotation)

        provision_dataset, update_operation = genomic_unit_query.provision_dataset_query_and_update()
        genomic_unit = self.collection.update_one(provision_dataset, update_operation)

        add_annotation_query, add_annotation_update_operation, add_annotation_array_filters = \
            genomic_unit_query.annotate_dataset_query_and_update()

        try:
            self.collection.update_one(
                add_annotation_query, add_annotation_update_operation, array_filters=add_annotation_array_filters
            )
        except ValueError as error:
            raise error

        return True

    def annotate_genomic_unit_with_file(self, genomic_unit, genomic_annotation):
        """ Ensures that an annotation is created for the annotation image upload and only one image is allowed """
        genomic_unit_document = self.find_genomic_unit(genomic_unit)
        data_set = genomic_annotation['data_set']

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                annotation[data_set][0]['value'].append(genomic_annotation['value'])
                return self.update_genomic_unit_by_mongo_id(genomic_unit_document)

        annotation_data_set = {
            genomic_annotation['data_set']: [{
                'data_source': genomic_annotation['data_source'],
                'version': genomic_annotation['version'],
                'value': [genomic_annotation['value']],
            }]
        }

        genomic_unit_document['annotations'].append(annotation_data_set)
        return self.update_genomic_unit_by_mongo_id(genomic_unit_document)

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

        self.update_genomic_unit_by_mongo_id(genomic_unit_document)

    def remove_genomic_unit_file_annotation(self, genomic_unit, data_set, file_id):
        """ Removes a file that has been added as an annotation to a genomic unit """

        genomic_unit_document = self.find_genomic_unit(genomic_unit)

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                for i in range(len(annotation[data_set][0]['value'])):
                    if annotation[data_set][0]['value'][i]['file_id'] == file_id:
                        annotation[data_set][0]['value'].pop(i)
                        break

        return self.update_genomic_unit_by_mongo_id(genomic_unit_document)

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
