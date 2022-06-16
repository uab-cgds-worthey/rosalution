"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import queue

from .annotation_task import AnnotationTaskFactory
from .core.analysis import Analysis
from .repository.annotation_collection import AnnotationCollection

# Creating a callable wrapper for an instance for FastAPI dependency injection
# pylint: disable=too-few-public-methods


def log_to_file(string):
    """
    Temprorary utility function for development purposes abstracted for testing.
    Will remove once feature is completed.
    """
    with open("rosalution-annotation-log.txt", mode="a", encoding="utf-8") as log_file:
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
        """Gets the thread safe item from the queue"""
        return self.annotation_queue.get()

    def put(self, value):
        """Puts the value in the thread safe queue"""
        self.annotation_queue.put(value)

    def empty(self):
        """Verifies if the thread safe queue is empty"""
        return self.annotation_queue.empty()


class AnnotationService():
    """
    Creates and user09es annotating genomic units for cases.
    """
    def __init__(self, annotation_collection: AnnotationCollection):
        """Initializes the annotation service and injects the collection that has the annotation configuration"""
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
            batched_annotation_tasks = {}
            while not annotation_queue.empty():
                genomic_unit, dataset_json = annotation_queue.get()

                task_identifier, task = AnnotationTaskFactory.create(
                    genomic_unit, dataset_json)

                if task_identifier not in batched_annotation_tasks:
                    batched_annotation_tasks[task_identifier] = task
                    log_to_file(
                        f"Batched: {genomic_unit} for datasets {dataset_json}\n")
                else:
                    batched_annotation_tasks[task_identifier].append(
                        dataset_json)

            for batch_task in batched_annotation_tasks.values():
                annotation_task_futures[executor.submit(
                    batch_task.annotate)] = (genomic_unit, batch_task)

            log_to_file('------done submitting tasks\n')

            for future in concurrent.futures.as_completed(annotation_task_futures):
                genomic_unit, annotation_task = annotation_task_futures[future]
                try:
                    log_to_file(f"{future.result()}\n")
                    log_to_file(f'{annotation_task.datasets}\n')
                    log_to_file(f'{genomic_unit}\n')
                except FileNotFoundError as error:
                    log_to_file(f"exception happened {error} with {genomic_unit} and {annotation_task}\n")

                log_to_file('\n')
                del annotation_task_futures[future]

            log_to_file(
                'after for loop for waiting for all of the futures to finis\n\n')
