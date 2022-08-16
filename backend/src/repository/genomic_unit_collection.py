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

    def find_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Returns the genomic unit with the corresponding transcript if it exists """
        return self.collection.find_one({
            genomic_unit['type'].value: genomic_unit['unit'],
            'transcripts.transcript_id': transcript_id
        })

    def update_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        return self.collection.update_one(
            { genomic_unit['type'].value: genomic_unit['unit'] },
            {
                '$addToSet':
                { 'transcripts':
                    {
                        'transcript_id': transcript_id,
                        'annotations': []
                    }
                }
            }
        )

    def update_genomic_unit_with_mongo_id(self, genomic_unit):
        """ Takes a genomic unit and overwrites the existing object based on the object's id """
        genomic_unit_id = genomic_unit['_id']
        self.collection.update_one({'_id': ObjectId(str(genomic_unit_id))}, { '$set': genomic_unit } )

    def annotate_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Takes a genomic_unit from an annotation task as well as a genomic_annotation and arranges them in a pattern
        that can be sent to mongo to update the genomic unit's document in the collection
        """

        if genomic_unit['type'].value == 'hgvs_variant':
            if 'transcript_id' in genomic_annotation:
                transcript_genomic_unit = self.find_genomic_unit_with_transcript_id(
                    genomic_unit, genomic_annotation['transcript_id']
                )

                if not transcript_genomic_unit:
                    self.update_genomic_unit_with_transcript_id(genomic_unit, genomic_annotation['transcript_id'])

                transcript_genomic_unit = self.find_genomic_unit_with_transcript_id(
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

                temp_data_set[genomic_annotation['data_set']].append(temp_data_set)

                for transcript in transcript_genomic_unit['transcripts']:
                    if transcript['transcript_id'] == genomic_annotation['transcript_id']:
                        transcript['annotations'].append(temp_data_set)

                self.update_genomic_unit_with_mongo_id(transcript_genomic_unit)

        return
