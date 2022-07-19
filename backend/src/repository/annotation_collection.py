"""
Manges the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added
from itertools import groupby
from ..utils import read_fixture, write_fixture

class AnnotationCollection:
    """Repository for querying configurations for annotation"""

    # def __init__(self, annotation_collection):
    # self.collection = annotation_collection

    def find_genomic_units(self):
        """ Returns all genomic units that are currently stored """
        return read_fixture("genomic-units-collection.json")

    def update_genomic_unit(self, genomic_unit, genomic_annotation):
        """ Update record for genomic unit """
        # This will be replaced by a Mongo update function and the proper query parameters
        # For right now, we'll get all genomic units, find the right now, update, and re-write the file
        genomic_units_to_annotate = self.find_genomic_units()

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
        write_fixture('genomic-units-collection.json', genomic_units_to_annotate)

        return

    def get_annotation_configurations(self):
        """Returns all annotation configurations"""
        # return self.collection.find() - eventually
        return read_fixture("dataset-sources.json")

    def find_by_data_set(self, dataset_name):
        """Returns a data set source that matches by name"""
        for dataset in self.get_annotation_configurations():
            if dataset_name == dataset.get("data_set"):
                return dataset

        return None

    def datasets_to_annotate_by_type(self, types):
        """gets dataset configurations according to the types"""
        configuration = self.get_annotation_configurations()
        return [dataset for dataset in configuration if dataset["genomic_unit_type"] in types]

    def datasets_to_annotate_for_units(self, genomic_units_to_annotate):
        """
        Returns an dict which uses GenomicUnitType enumeration as a key with
        a value being the list of datasets configured to annotate for that type
        """
        types_to_annotate = set(map(lambda x: x["type"], genomic_units_to_annotate))
        datasets_to_annotate = self.datasets_to_annotate_by_type(types_to_annotate)

        configuration = {}
        for genomic_unit_type in types_to_annotate:
            configuration[genomic_unit_type] = []

        for key, group in groupby(datasets_to_annotate, lambda x: x["genomic_unit_type"]):
            configuration[key] = list(group)

        return configuration
