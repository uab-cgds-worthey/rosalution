"""
Manges the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added
from itertools import groupby
from ..utils import read_fixture, write_fixture

import json

class AnnotationCollection:
    """Repository for querying configurations for annotation"""

    # def __init__(self, annotation_collection):
    # self.collection = annotation_collection

    def find_genomic_units(self):
        """ Returns all genomic units that are currently stored """
        return read_fixture("genomic-units-collection.json")

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

    def write_genomic_unit(self, genomic_unit):
        annotations = read_fixture("annotations.json")
        print(annotations)
        return

    def write_genomic_annotation(self, genomic_annotation):
        genomic_units_to_annotate = self.find_genomic_units()

        annotation_genomic_unit = genomic_annotation['genomic_unit']
        symbol_value = genomic_annotation['symbol_value']

        # print("")
        # print(annotation_genomic_unit)
        # print(symbol_value)
        
        for unit in genomic_units_to_annotate:
            if annotation_genomic_unit in unit.keys() and unit[annotation_genomic_unit] == symbol_value:
                unit['annotations'].append(genomic_annotation)
                
        
        write_fixture("genomic-units-collection.json", genomic_units_to_annotate)
        
        return
