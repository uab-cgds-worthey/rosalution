"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import queue

from .core.data_set_source import DataSetSource

from .core.analysis import Analysis

from .repository.annotation_collection import AnnotationCollection

# Creating a callable wrapper for an instance for FastAPI dependency injection
# pylint: disable=too-few-public-methods


def log_to_file(string):
    """
    Temprorary utility function for development purposes abstracted for testing.
    Will remove once feature is completed.
    """
    with open("divergen-annotation-log.txt", mode="a", encoding="utf-8") as log_file:
        log_file.write(string)
    print(string)


class AnnotationQueue():
    """Wrapper for the queue to processes annotation tasks"""

    def __init__(self):
        """Instantiates an annotation queue that is thread-safe"""
        self.annotation_queue = queue.Queue()

    def __call__(self):
        """Returns the Thread Safe Blocking Queue"""
        return self.annotation_queue

    def get(self):
        return self.annotation_queue.get()
    
    def put(self, value):
        self.annotation_queue.put(value)
    
    def empty(self):
        return self.annotation_queue.empty()


class AnnotationService():
    """
    Creates and user09es annotating genomic units for cases.
    """

    def __init__(self, annotation_collection: AnnotationCollection):
        self.annotation_collection = annotation_collection

    def queue_annotation_tasks(self, analysis: Analysis, annotation_task_queue: AnnotationQueue):
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
        log_to_file('running annotations for ...\n')

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            annotation_task_futures = {}
            while not annotation_queue.empty():
                genomic_unit, dataset = annotation_queue.get()
                annotation = DataSetSource(**dataset)
                log_to_file(f"Que: {genomic_unit} for datasets {dataset}\n")
                annotation_task_futures[executor.submit(
                    annotation.annotate, genomic_unit)] = (genomic_unit, dataset)

            for future in concurrent.futures.as_completed(annotation_task_futures):
                genomic_unit, dataset = annotation_task_futures[future]
                try:
                    log_to_file(f"{future.result()} \n")
                except FileNotFoundError as error:
                    log_to_file(f"exception happened {error}")
                except Exception as error:
                    log_to_file(f"exception happened {error}")

                del annotation_task_futures[future]
