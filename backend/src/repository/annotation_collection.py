"""
Manges the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added
from itertools import groupby
from ..utils import read_fixture


class AnnotationCollection:
    """Repository for querying configurations for annotation"""

    # def __init__(self, annotation_collection):
    # self.collection = annotation_collection

    def all(self):
        """Returns all annotation configurations"""
        # return self.collection.find() - eventually
        return read_fixture("dataset-sources.json")

    def find_by_data_set(self, dataset_name):
        """Returns a data set source that matches by name"""
        for dataset in self.all():
            if dataset_name == dataset.get("data_set"):
                return dataset

        return None

    def datasets_to_annotate_by_type(self, types):
        """gets dataset configurations according to the types"""
        configuration = self.all()
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
