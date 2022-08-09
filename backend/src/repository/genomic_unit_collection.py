"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""

class GenomicUnitCollection:
    """ Repository for user09ing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection

    def all(self):
        """ Returns all genomic units that are currently stored """
        return self.collection.find()

    def update_genomic_unit(self, genomic_unit, genomic_annotation):
        """
        Takes a genomic_unit from an annotation task as well as a genomic_annotation and arranges them in a pattern
        that can be sent to mongo to update the genomic unit's document in the collection
        """

        if genomic_unit['type'].value == 'hgvs_variant':
            mongo_query = {
                genomic_unit['type'].value: genomic_unit['unit'],
                'transcripts.transcript_id': genomic_annotation['symbol_value']['transcript_id']
            }

            annotation_path = 'annotations.' + genomic_annotation['key']
            annotation_document = { annotation_path: genomic_annotation['value'] }

            self.collection.update_one(mongo_query, {'$set': annotation_document}, upsert=True)

        return