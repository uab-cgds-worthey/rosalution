"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
import logging

# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
from bson import ObjectId

# create logger
logger = logging.getLogger(__name__)


class GenomicUnitCollection:
    """ Repository for managing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection

    def all(self):
        """ Returns all genomic units that are currently stored """
        return self.collection.find()

    def annotation_exist(self, genomic_unit, dataset):
        """ Returns true if the genomic_unit already has that dataset annotated """
        data_set_name = dataset['data_set']
        find_query = {
            genomic_unit['type'].value: genomic_unit['unit'],
        }

        if 'transcript' in dataset:
            hgvs_genomic_unit = self.collection.find_one(find_query)

            if not hgvs_genomic_unit['transcripts']:
                return False

            for transcript in hgvs_genomic_unit['transcripts']:
                dataset_in_transcript_annotation = next(
                    (annotation for annotation in transcript['annotations'] if data_set_name in annotation), None
                )
                if not dataset_in_transcript_annotation:
                    return False
            return True

        annotation_field_key = f"annotations.{data_set_name}"
        find_query[annotation_field_key] = {'$exists': True}
        return bool(self.collection.count_documents(find_query, limit=1))

    def find_genomic_unit_annotation_value(self, genomic_unit, dataset):
        """ Returns the annotation value for a genomic unit according the the dataset"""
        data_set_name = dataset
        find_query = {
            genomic_unit['type'].value: genomic_unit['unit'],
            f"annotations.{data_set_name}": {'$exists': True},
        }
        result = self.collection.find_one(find_query)

        if result is None:
            return None

        for annotation in result['annotations']:
            if dataset in annotation:
                for data in annotation[dataset]:
                    return data['value']

        return None

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

    def update_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        return self.collection.update_one(
            {genomic_unit['type'].value: genomic_unit['unit']},
            {'$addToSet': {'transcripts': {'transcript_id': transcript_id, 'annotations': []}}},
        )

    def update_genomic_unit_with_mongo_id(self, genomic_unit_document):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit_document['_id']
        self.collection.update_one(
            {'_id': ObjectId(str(genomic_unit_id))},
            {'$set': genomic_unit_document},
        )

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

        if 'transcript_id' in genomic_annotation:
            genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                genomic_unit, genomic_annotation['transcript_id']
            )

            if not genomic_unit_document:
                self.update_genomic_unit_with_transcript_id(genomic_unit, genomic_annotation['transcript_id'])
                genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                    genomic_unit, genomic_annotation['transcript_id']
                )

            for transcript in genomic_unit_document['transcripts']:
                if transcript['transcript_id'] == genomic_annotation['transcript_id']:
                    transcript['annotations'].append(annotation_data_set)

            self.update_genomic_unit_with_mongo_id(genomic_unit_document)

        else:
            genomic_unit_document = self.find_genomic_unit(genomic_unit)
            genomic_unit_document['annotations'].append(annotation_data_set)
            self.update_genomic_unit_with_mongo_id(genomic_unit_document)

        return

    def annotate_genomic_unit_with_file(self, genomic_unit, genomic_annotation):
        """ Ensures that an annotation is created for the annotation image upload and only one image is allowed """

        genomic_unit_document = self.find_genomic_unit(genomic_unit)
        data_set = genomic_annotation['data_set']

        for annotation in genomic_unit_document['annotations']:
            if data_set in annotation:
                annotation[data_set][0]['value'].append(genomic_annotation['value'])
                self.update_genomic_unit_with_mongo_id(genomic_unit_document)
                return

        annotation_data_set = {
            genomic_annotation['data_set']: [{
                'data_source': genomic_annotation['data_source'],
                'version': genomic_annotation['version'],
                'value': [genomic_annotation['value']],
            }]
        }

        genomic_unit_document['annotations'].append(annotation_data_set)
        self.update_genomic_unit_with_mongo_id(genomic_unit_document)

        return

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

        self.update_genomic_unit_with_mongo_id(genomic_unit_document)

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

        self.update_genomic_unit_with_mongo_id(genomic_unit_document)

        return

    def create_genomic_unit(self, genomic_unit):
        """
        Takes a genomic_unit and adds it to the collection if it doesn't already exist (exact match).
        """

        # Make sure the genomic unit doesn't already exist
        if self.collection.find_one(genomic_unit):
            logging.info("Genomic unit already exists, skipping creation")

        self.collection.insert_one(genomic_unit)
        return
