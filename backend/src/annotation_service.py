"""
Collection with retrieves, creates, and modify analyses.
"""
from itertools import groupby

from .repository.annotation_collection import AnnotationCollection


class AnnotationService:
    """
    Creates and user09es annotating genomic units for cases.
    """
    def __init__(self, annotation_collection: AnnotationCollection):
        self.annotation_collection = annotation_collection

    def annotate(self, units, types):
        """
        Uses the list of genomic units and the list of types to queue annotation operations.
        """
        datasets_to_annotate = self.annotation_collection.datasets_configuration(
            types)

        configuration = {}
        for genomic_unit_type in types:
            configuration[genomic_unit_type] = []

        for key, group in groupby(datasets_to_annotate, lambda x: x['type']):
            configuration[key] = list(group)

        for unit in units:
            for dataset in configuration[unit['type'].value]:
                queue_annotation(dataset, unit)

        return

def queue_annotation(dataset, unit):
    """Placeholder method to queue a dataset to annotate for a specific unit"""
    print(f"Quesing '{dataset['data_set']}' from '{dataset['data_source']}' for unit {unit['unit']}")

    return
