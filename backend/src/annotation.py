"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import queue

from .annotation_task import AnnotationTaskFactory
from .core.analysis import Analysis
from .repository.annotation_config_collection import AnnotationConfigCollection

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

class AnnotationQueue:
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

class AnnotationService:
    """
    Creates and user09es annotating genomic units for cases.
    """

    def __init__(self, annotation_config_collection: AnnotationConfigCollection):
        """Initializes the annotation service and injects the collection that has the annotation configuration"""
        self.annotation_config_collection = annotation_config_collection

    def queue_annotation_tasks(self, analysis: Analysis, annotation_task_queue: AnnotationQueue):
        """
        Uses the list of genomic units and the list of types to queue annotation operations.
        """
        units_to_annotate = analysis.units_to_annotate()

        annotation_configuration = self.annotation_config_collection.datasets_to_annotate_for_units(
            units_to_annotate)

        for genomic_unit in units_to_annotate:
            genomic_unit_type = genomic_unit["type"].value
            for dataset in annotation_configuration[genomic_unit_type]:
                annotation_task_queue.put((genomic_unit, dataset))

    @staticmethod
    def process_tasks(annotation_queue, genomic_unit_collection): # pylint: disable=too-many-locals
        """Processes items that have been added to the queue"""
        log_to_file("Running annotations for ...\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            annotation_task_futures = {}
            while not annotation_queue.empty():
                genomic_unit, dataset_json = annotation_queue.get()
                if genomic_unit_collection.annotation_exist(genomic_unit, dataset_json):
                    log_to_file(f"{genomic_unit['unit']} for {dataset_json['data_set']} - Annotation Exists...\n")
                    continue

                ready = True
                if 'dependencies' in dataset_json:
                    missing_dependencies = [
                        dependency for dependency in dataset_json['dependencies'] if dependency not in genomic_unit]

                    for missing in missing_dependencies:
                        annotation_value = genomic_unit_collection.find_genomic_unit_annotation_value(
                            genomic_unit, missing)
                        if annotation_value:
                            genomic_unit[missing] = annotation_value
                        else:
                            ready = False

                # print('----------------------\n')
                if not ready:
                    log_to_file(f"{genomic_unit['unit']} for {dataset_json['data_set']} + \
                        - Delaying Annotation, Missing Dependency...\n")
                    annotation_queue.put((genomic_unit, dataset_json))
                    continue

                task = AnnotationTaskFactory.create(genomic_unit, dataset_json)
                log_to_file(f"{genomic_unit['unit']} for {dataset_json['data_set']} - Creating Task To Annotate...\n")

                annotation_task_futures[executor.submit(task.annotate)] = (
                    genomic_unit,
                    task,
                )

                for future in concurrent.futures.as_completed(annotation_task_futures):
                    genomic_unit, annotation_task = annotation_task_futures[future]
                    log_to_file(f"{genomic_unit['unit']} for {dataset_json['data_set']} - futureQuery completed...\n")
                    try:
                        result_temp = future.result()

                        for annotation in annotation_task.extract(result_temp):
                            log_to_file(
                                f"{genomic_unit['unit']} for {annotation_task.dataset['data_set']} - + \
                                Saving {annotation['value']}...\n")
                            genomic_unit_collection.annotate_genomic_unit(
                                annotation_task.genomic_unit, annotation)

                    except FileNotFoundError as error:
                        log_to_file(
                            f"exception happened {error} with {genomic_unit} and {annotation_task}\n")

                    log_to_file("\n")
                    del annotation_task_futures[future]

            log_to_file(
                "after for loop for waiting for all of the futures to finish\n\n")
