"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""

# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
from bson import ObjectId


class GenomicUnitCollection:
    """ Repository for user09ing genomic units and their annotations """

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
                if not next(
                    (annotation for annotation in transcript['annotations'] if data_set_name in annotation), None
                ):
                    return False
            return True

        annotation_field_key = f"annotations.{data_set_name}"
        find_query[annotation_field_key] = {'$exists': True}
        return True if self.collection.count_documents(find_query, limit=1) else False

    def find_genomic_unit_annotation_value(self, genomic_unit, dataset):
        """ Returns the annotation value for a genomic unit according the the dataset"""
        data_set_name = dataset
        find_query = {
            genomic_unit['type'].value: genomic_unit['unit'],
            f"annotations.{data_set_name}": {'$exists': True}
        }
        result = self.collection.find_one(find_query)

        if result is None:
            return None

        return next(
            (annotation[data_set_name]['value']
             for annotation in result['annotations'] if data_set_name in annotation),
            None
        )

    def find_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Returns the genomic unit with the corresponding transcript if it exists """
        return self.collection.find_one({
            genomic_unit['type'].value: genomic_unit['unit'],
            'transcripts.transcript_id': transcript_id
        })

    def update_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        return self.collection.update_one(
            {genomic_unit['type'].value: genomic_unit['unit']},
            {'$addToSet': {'transcripts': {
                'transcript_id': transcript_id, 'annotations': []}}}
        )

    def update_genomic_unit_with_mongo_id(self, genomic_unit_document):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit_document['_id']
        self.collection.update_one({'_id': ObjectId(str(genomic_unit_id))}, {
                                   '$set': genomic_unit_document})

    def annotate_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Takes a genomic_unit from an annotation task as well as a genomic_annotation and arranges them in a pattern
        that can be sent to mongo to update the genomic unit's document in the collection
        """

        if genomic_unit['type'].value == 'hgvs_variant':
            if 'transcript_id' in genomic_annotation:
                genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                    genomic_unit,
                    genomic_annotation['transcript_id']
                )

                if not genomic_unit_document:
                    self.update_genomic_unit_with_transcript_id(
                        genomic_unit, genomic_annotation['transcript_id'])
                    genomic_unit_document = self.find_genomic_unit_with_transcript_id(
                        genomic_unit,
                        genomic_annotation['transcript_id']
                    )

                # We'll need to find if the genomic annotation exists before updating the record, but here, we know
                # it doesn't exist, so we insert it directly. This needs to be a check.
                temp_data_set = {
                    genomic_annotation['data_set']: [{
                        'data_source': genomic_annotation['data_source'],
                        'version': genomic_annotation['version'],
                        'value': genomic_annotation['value'],
                    }]
                }

                for transcript in genomic_unit_document['transcripts']:
                    if transcript['transcript_id'] == genomic_annotation['transcript_id']:
                        transcript['annotations'].append(temp_data_set)

                self.update_genomic_unit_with_mongo_id(genomic_unit_document)

        return


    def create_genomic_unit(self, genomic_unit):
        """
        Takes a genomic_unit and adds it to the collection if it doesn't already exist (exact match).
        """

        # Make sure the genomic unit doesn't already exist
        if self.collection.find_one(genomic_unit):
            print("Genomic unit already exists, skipping creation")
        self.collection.insert_one(genomic_unit)
        return
