"""Supports the queueing and processing of genomic unit annotation"""
import queue

from .core.analysis import Analysis

from .repository.annotation_collection import AnnotationCollection

# Creating a callable wrapper for an instance for FastAPI dependency injection
# pylint: disable=too-few-public-methods


class AnnotationQueue():
    """Wrapper for the queue to processes annotation tasks"""

    def __init__(self):
        """Instantiates an annotation queue that is thread-safe"""
        self.annotation_queue = queue.Queue()

    def __call__(self):
        """Returns the Thread Safe Blocking Queue"""
        return self.annotation_queue


class AnnotationService():
    """
    Creates and user09es annotating genomic units for cases.
    """

    def __init__(self, annotation_collection: AnnotationCollection):
        self.annotation_collection = annotation_collection

    def queue_annotation_tasks(self, analysis: Analysis, annotation_task_queue):
        """
        Uses the list of genomic units and the list of types to queue annotation operations.
        """
        units_to_annotate = analysis.units_to_annotate()

        annotation_configuration = self.annotation_collection.datasets_to_annotate_for_units(
            units_to_annotate)

        for genomic_unit in units_to_annotate:
            genomic_unit_type = genomic_unit['type'].value
            for dataset in annotation_configuration[genomic_unit_type]:
                annotation_task_queue.put((genomic_unit, dataset))

    @staticmethod
    def process_tasks(annotation_queue):
        """Processes items that have been added to the queue"""
        log = 'running annotations for ...\n'
        while not annotation_queue.empty():
            genomic_unit, dataset = annotation_queue.get()
            log += f"Unit '{genomic_unit['unit']}', Queue '{dataset['data_set']}' from '{dataset['data_source']}'\n"
        log += 'queue empty'
        
        with open("divergen-annotation-log.txt", mode="w", encoding="utf-8") as email_file:
            email_file.write(log)
