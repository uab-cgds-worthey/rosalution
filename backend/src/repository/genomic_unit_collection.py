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

logger = logging.getLogger(__name__)


class GenomicUnitQuery():
    def __init__(self, genomic_unit, genomic_annotation):
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation
        self.dataset_name = self.genomic_annotation['data_set']

    @property
    def annotations_dataset_field_name(self):
        return f"annotations.{self.dataset_name}"
    
    @property
    def annotations_add_dataset_field_name(self):
        return f"annotations.$[dataset].{self.dataset_name}"
    
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
    
    def dataset_in_genomic_unit(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """

        genomic_unit_find = self._genomic_unit_find()

        dataset_in_annotations = f"annotations.{self.dataset_name}"
        genomic_unit_find[dataset_in_annotations] =  {'$exists': False }

        return dataset_in_annotations
    
    def provision_dataset_query_and_update(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            self.annotations_dataset_field_name: {'$exists': False}
        }

        update_operation = { 
            '$addToSet': {
                "annotations": { 
                    self.dataset_name: []
                }
            }
        }

        return query_filter, update_operation

    def _annotations_dataset_field_name(self):
        return f"annotations.{self.dataset_name}"
    
    def _annotations_add_dataset_field_name(self):
        return f"annotations.$[dataset].{self.dataset_name}"
        

    def annotation_exist_in_dataset(self, dataset_json):
        return next((
            annotation for annotation in dataset_json[self.dataset_name]
            if self.genomic_annotation['version'] == annotation['version']
            and self.genomic_annotation['data_source'] == annotation['data_source']), None
        )

    def annotate_dataset_query_and_update(self):

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            self._annotations_dataset_field_name(): { '$exists': True } 
        }

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        update_operation = { 
            self._annotations_add_dataset_field_name(): annotation_entry
        }

        arrays_filter = [
            {f"dataset.{self.dataset_name}": {'$exists': True}}
        ]

        return query_filter, update_operation, arrays_filter

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
        return {f"annotations.{self.annotation_unit.get_dataset_name()}.$": 1, "_id": 0}
    
class GenomicUnitCollection:
    """ Repository for managing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection

    def all(self):
        """ Returns all genomic units that are currently stored """
        return self.collection.find()

    def annotation_exist(self, annotation_unit: AnnotationUnit):
        """ Returns true if the genomic_unit already has that dataset annotated """
        if annotation_unit.is_transcript_dataset():
            collection_for_transcripts = GenomicUnitCollectionForTranscripts(self)
            return collection_for_transcripts.annotation_exist(annotation_unit)

        data_set_name = annotation_unit.get_dataset_name()

        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)
        find_query = annotation_query_adapter.find_annotation_query()
        
        if( data_set_name == 'pos'):
            logger.warning(find_query)
            logger.warning('why did it fail to find the annotation for this')

        return bool(self.collection.count_documents(find_query, limit=1))

    def find_genomic_unit_annotation_value(self, annotation_unit: AnnotationUnit):
        """ Returns the annotation value for a genomic unit according the the dataset"""

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
        
        print(dataset_annotations)
        
        return next((
            annotation['value'] 
            for annotation in dataset_annotations[dataset_name]
            if annotation_unit.does_source_and_version_match(annotation['data_source'], annotation['version'])
        ),None)

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
            collection_for_transcripts = GenomicUnitCollectionForTranscripts(self)
            return collection_for_transcripts.annotate_transcript_dataset(genomic_unit, genomic_annotation)


        genomic_unit_query = GenomicUnitQuery(genomic_unit, genomic_annotation)

        provision_dataset, update_operation = genomic_unit_query.provision_dataset_query_and_update()
        genomic_unit = self.collection.update_one(provision_dataset, update_operation)

        add_annotation_query, add_annotation_update_operation, add_annotation_array_filters = genomic_unit_query.annotate_dataset_query_and_update()
        self.collection.update_one(add_annotation_query, add_annotation_update_operation, array_filters=add_annotation_array_filters)


    def annotate_genomic_unit_with_file(self, genomic_unit, genomic_annotation):
        """ Ensures that an annotation is created for the annotation image upload and only one image is allowed """
        collection_file_adapter = GenomicUnitCollectionForFiles(self)
        return collection_file_adapter.annotate_genomic_unit_with_file(genomic_unit, genomic_annotation)


    def update_genomic_unit_file_annotation(self, genomic_unit, data_set, annotation_value, file_id_old):
        """ Replaces existing annotation image with new image """
        collection_file_adapter = GenomicUnitCollectionForFiles(self)
        collection_file_adapter.update_genomic_unit_file_annotation(genomic_unit, data_set, annotation_value, file_id_old)
        return

    def remove_genomic_unit_file_annotation(self, genomic_unit, data_set, file_id):
        """ Removes a file that has been added as an annotation to a genomic unit """

        collection_file_adapter = GenomicUnitCollectionForFiles(self)
        return collection_file_adapter.remove_genomic_unit_file_annotation(genomic_unit, data_set, file_id)


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



class GenomicUnitCollectionForFiles():
    def __init__(self, genomic_unit_collection: GenomicUnitCollection):
        self.collection = genomic_unit_collection.collection


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

        return self.update_genomic_unit_by_mongo_id(genomic_unit_document)



class AnnotationUnitTranscriptQuery():
    def __init__(self, annotation_unit):
        self.annotation_unit = annotation_unit
    
    @property
    def genomic_unit_type_string(self):
        return self.annotation_unit.get_genomic_unit_type_string()

    @property
    def genomic_unit_name(self):
        return self.self.annotation_unit.get_genomic_unit()

    @property
    def annotation_dataset_field_name(self):
        return f"transcripts.annotations.{self.dataset_name}"
    
    @property
    def annotations_add_dataset_field_name(self):
        return f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}"

    # def find_genomic_unit_query(self):
    #     """
    #         # find_query = {
    #         #   'gene': 'VMA21',
    #         #}
    #     """
    #     return {genomic_unit_type_string: genomic_unit_name}

    def find_dataset_query(self):
        genomic_unit_query = self.find_genomic_unit_query()

        data_set_name = self.annotation_unit.get_dataset_name()
        dataset_property = f"annotations.{data_set_name}"
        genomic_unit_query[dataset_property] = {'$exists': True}

    def find_annotation_query(self, transcript_id):
        """
            find_query = {
              "hgvs_variant": "NM_001017980.3:c.164G>T"
                "transcripts.transcript_id": "NM_001017980.4",
                "transcripts.annotations.SIFT Score": {$exists: true},
                "transcripts.annotations.SIFT Score.data_source": "Ensembl",
                "transcripts.annotations.SIFT Score.version": 113,
            }
        """

        data_source_field = f"{self.annotation_dataset_field_name}.data_source"
        version_field = f"{self.annotation_dataset_field_name}.version"

        find_query = {
            self.genomic_unit_type_string: self.genomic_unit_name,
            "transcripts.transcript_id": transcript_id,
            self.annotation_dataset_field_name: {'$exists': True},
            data_source_field: self.annotation_unit.get_dataset_source(),
            version_field: self.annotation_unit.get_version()
        }
        
        return find_query

    def find_annotation_value_projection(self):
        return {f"annotations.{self.annotation_unit.get_dataset_name()}.$": 1, "_id": 0}

class GenomicUnitTranscriptQuery():
    def __init__(self, genomic_unit, genomic_annotation):
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation
        self.dataset_name = self.genomic_annotation['data_set']

    @property
    def annotations_dataset_field_name(self):
        return f"annotations.{self.dataset_name}"
    
    @property
    def annotations_add_dataset_field_name(self):
        return f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}"

    def provision_dataset_query_and_update(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            "transcripts.transcript_id": {'$exists': True },
            self.annotations_add_dataset_field_name: {'$exists': False}
        }

        update_operation = { 
            '$addToSet': {
                "transcripts.$[transcript].annotations": { 
                    self.dataset_name: []
                }
            }
        }

        arrays_filter = [
            {"transcript.transcript_id": self.genomic_annotation['transcript_id']},
        ]

        return query_filter, update_operation, arrays_filter

    def annotate_dataset_query_and_update(self):

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            "transcripts.transcript_id": self.genomic_annotation['transcript_id']
        }

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        update_operation = {
            '$addToSet': {
                self.annotations_add_dataset_field_name: annotation_entry
            }
        }

        arrays_filter = [
            {"transcript.transcript_id": self.genomic_annotation['transcript_id']},
            {f"dataset.{self.dataset_name}": {'$exists': True}}
        ]

        return query_filter, update_operation, arrays_filter

class GenomicUnitCollectionForTranscripts():
    def __init__(self, genomic_unit_collection: GenomicUnitCollection):
        self.collection = genomic_unit_collection.collection

    def annotation_exist(self, annotation_unit):
        annotation_query_adapter = AnnotationUnitTranscriptQuery(annotation_unit)

        find_query = annotation_query_adapter.find_genomic_unit_query()
        hgvs_genomic_unit_json = self.collection.find_one(find_query)

        if 'transcripts' not in hgvs_genomic_unit_json or len(hgvs_genomic_unit_json['transcripts']) == 0:
            return False


        for transcript in hgvs_genomic_unit_json['transcripts']:
            # if( "NM_001365.4:c.1039del" in annotation_unit.to_name_string() ):
            #     logger.warning("LOOKING AT THE FOLLOWING TRANSCRIPT TO FIND: %s", transcript)
            #     logger.warning(transcript['annotations'])
            #     logger.warning(annotation_unit.to_name_string())
            #     logger.warning(data_set_name)
            find_transcript_query = annotation_query_adapter.find_annotation_query(transcript)
            if  not bool(self.collection.count_documents(find_transcript_query, limit=1)):
                return False

        return True

    def find_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Returns the genomic unit with the corresponding transcript if it exists """

        query = {
            genomic_unit['type'].value: genomic_unit['unit'],
            'transcripts.transcript_id': transcript_id,
        }
        result = self.collection.find_one(query)
        return result
    
    def add_transcript_to_genomic_unit(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        query = {
            genomic_unit['type'].value: genomic_unit['unit']
        }

        operation = {
            '$addToSet': {
                'transcripts': {'transcript_id': transcript_id, 'annotations': []}
            }
        }

        result = self.collection.find_one_and_update(
            query,
            operation,
            return_document=ReturnDocument.AFTER
        )

        return result
    
    def annotate_transcript_dataset(self, genomic_unit, genomic_annotation):
        transcript_query = GenomicUnitTranscriptQuery(genomic_unit, genomic_annotation)

        provision_dataset, update_operation = transcript_query.provision_dataset_query_and_update()
        genomic_unit = self.collection.update_one(provision_dataset, update_operation)

        add_annotation_query, add_annotation_update_operation, add_annotation_array_filters = transcript_query.annotate_dataset_query_and_update()
        result = self.collection.update_one(add_annotation_query, add_annotation_update_operation, array_filters=add_annotation_array_filters)

        return result
