"""
Manages the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""

# pylint: disable=no-self-use
# This linting disable will be removed once database is added
import json, os

from ..utils import read_fixture

class GenomicUnitCollection:
    def all(self):
        """ Returns all genomic units that are currently stored """
        return read_fixture("genomic-units-collection.json")

    def update_genomic_unit(self, genomic_unit, genomic_annotation):
        """ Update record for genomic unit """
        # This will be replaced by a Mongo update function and the proper query parameters
        # For right now, we'll get all genomic units, find the right now, update, and re-write the file
        genomic_units_to_annotate = self.all()

        selected_unit = None

        for unit in genomic_units_to_annotate:
            if genomic_unit['unit'] in unit.values():
                selected_unit = unit

        if selected_unit is None:
            print("Genomic Unit doesn't exist in collection")
            return

        # If the genomic unit is a transcript, we check to see if the transcript exists before we append it
        # to the existing genomic unit and then proceed to annotate.
        if genomic_annotation['symbol_notation'] == 'transcript_id':
            selected_transcript = None
            for transcript in selected_unit['transcripts']:
                if genomic_annotation['symbol_value']['transcript_id'] in transcript['transcript_id']:
                    selected_transcript = transcript

            if selected_transcript is None:
                selected_transcript = {
                    'transcript_id': genomic_annotation['symbol_value']['transcript_id'],
                    'gene_symbol': genomic_annotation['symbol_value']['gene_symbol'],
                    'annotations': {}
                }
                selected_unit['transcripts'].append(selected_transcript)

            annotation_key = genomic_annotation['key']
            annotation_value = genomic_annotation['value']

            selected_transcript['annotations'][annotation_key] = [annotation_value]

        # Temporary as mongo will be used to update the collection properly
        self.write_fixture('genomic-units-collection.json', genomic_units_to_annotate)

    def write_fixture(self, fixture_filename, data_to_write):
        """reads the JSON from the filepath relative to the src directory"""

        RELATIVE_FIXUTRE_DIRECTORY_PATH = "../fixtures/"

        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.split(path_to_current_file)[0]
        path_to_file = os.path.join(current_directory, RELATIVE_FIXUTRE_DIRECTORY_PATH + fixture_filename)
        with open(path_to_file, mode="w", encoding="utf-8") as file_to_write:
            json.dump(data_to_write, file_to_write, ensure_ascii=False, indent=4)

            file_to_write.close()

        return
