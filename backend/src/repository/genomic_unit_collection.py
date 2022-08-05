"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""

# pylint: disable=no-self-use
# This linting disable will be removed once database is added
import json
import os

from ..utils import read_fixture

class GenomicUnitCollection:
    """ Repository for user09ing genomic units and their annotations """

    def __init__(self, genomic_units_collection):
        """Initializes with the 'PyMongo' Collection object for the Genomic Units collection"""
        self.collection = genomic_units_collection

    def all(self):
        """ Returns all genomic units that are currently stored """
        return read_fixture("genomic-units-collection.json")

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
            
            self.update_one(mongo_query, annotation_document)

            # self.collection.updateOne(mongo_query, annotation_document, { 'upsert': True })

        return

    # This will not be used in the future
    def update_one(self, genomic_unit, genomic_annotation):
        """ Takes a file name and data then formats the data needed for the file """

        # This will be replaced by a Mongo update function and the proper query parameters
        # For right now, we'll get all genomic units, find the right now, update, and re-write the file
        genomic_units_to_annotate = self.all()

        selected_unit = None

        genomic_unit_key = list(genomic_unit.keys())[0]
        transcript_id = genomic_unit['transcripts.transcript_id']

        for unit in genomic_units_to_annotate:
            if genomic_unit[genomic_unit_key] in unit.values():
                selected_unit = unit

        if selected_unit is None:
            print("Genomic Unit doesn't exist in collection")
            return

        ## If the genomic unit is a transcript, we check to see if the transcript exists before we append it
        ## to the existing genomic unit and then proceed to annotate.

        selected_transcript = None
        for transcript in selected_unit['transcripts']:
            if transcript_id in transcript['transcript_id']:
                selected_transcript = transcript

        if selected_transcript is None:
            selected_transcript = {
                'transcript_id': transcript_id,
                'gene_symbol': '',
                'annotations': {}
            }
            selected_unit['transcripts'].append(selected_transcript)


        genomic_annotation_key = list(genomic_annotation.keys())[0]

        selected_transcript['annotations'].update({
                genomic_annotation_key.split('.')[1]: genomic_annotation[genomic_annotation_key]
            }
        )

        self.write_fixture(genomic_units_to_annotate)


    def write_fixture(self, genomic_units_to_annotate):
        """ Temporary write fixture function """
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.split(path_to_current_file)[0]
        path_to_file = os.path.join(
                current_directory, "../../fixtures/genomic-units-collection.json"
            )
        with open(path_to_file, mode="w", encoding="utf-8") as file_to_write:
            json.dump(genomic_units_to_annotate, file_to_write, ensure_ascii=False, indent=4)

            file_to_write.close()

        return
