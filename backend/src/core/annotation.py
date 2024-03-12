"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import logging
import queue

from .annotation_logging import annotation_log_label, annotation_unit_string
from .annotation_task import AnnotationTaskFactory
from ..models.analysis import Analysis
from ..repository.annotation_config_collection import AnnotationConfigCollection
from ..core.annotation_unit import AnnotationUnit

# create logger
logger = logging.getLogger(__name__)


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
    Creates and manages annotating genomic units for cases.
    """

    def __init__(self, annotation_config_collection: AnnotationConfigCollection):
        """Initializes the annotation service and injects the collection that has the annotation configuration"""
        self.annotation_config_collection = annotation_config_collection

    def queue_annotation_tasks(self, analysis: Analysis, annotation_task_queue: AnnotationQueue):
        """
        Uses the list of genomic units and the list of types to queue annotation operations.
        """
        units_to_annotate = analysis.units_to_annotate()

        annotation_configuration = self.annotation_config_collection.datasets_to_annotate_for_units(units_to_annotate)

        for genomic_unit in units_to_annotate:
            genomic_unit_type = genomic_unit["type"].value
            for dataset in annotation_configuration[genomic_unit_type]:
                annotation_unit_queued = AnnotationUnit(genomic_unit, dataset)
                annotation_task_queue.put(annotation_unit_queued)

    @staticmethod
    def process_tasks(annotation_queue, genomic_unit_collection):  # pylint: disable=too-many-locals
        """Processes items that have been added to the queue"""
        logger.info("%s Processing annotation tasks queue ...", annotation_log_label())

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            annotation_task_futures = {}
            while not annotation_queue.empty():
                annotation_unit = annotation_queue.get()
                if genomic_unit_collection.annotation_exist(annotation_unit.genomic_unit, annotation_unit.dataset):
                    logger.info(
                        '%s Annotation Exists...',
                        annotation_unit_string(annotation_unit.get_genomic_unit(), annotation_unit.get_dataset())
                    )
                    continue

                ready = True

                if 'dependencies' in annotation_unit.dataset:
                    missing_dependencies = annotation_unit.get_missing_dependencies()
                    for missing in missing_dependencies:
                        annotation_value = genomic_unit_collection.find_genomic_unit_annotation_value(
                            annotation_unit.genomic_unit, missing
                        )
                        if annotation_value:
                            annotation_unit.genomic_unit[missing] = annotation_value
                        else:
                            ready = False

                if not ready:
                    annotation_unit.set_delay_count()

                    if annotation_unit.check_delay_count():
                        logger.info(
                            '%s Delaying Annotation, Missing Dependency...',
                            annotation_unit_string(annotation_unit.get_genomic_unit(), annotation_unit.get_dataset())
                        )
                        annotation_queue.put(annotation_unit)
                    else:
                        missing_dependencies = annotation_unit.get_missing_dependencies()
                        logger.info(
                            '%s Canceling Annotation, Missing %s ...',
                            annotation_unit_string(annotation_unit.get_genomic_unit(), annotation_unit.get_dataset()),
                            missing_dependencies
                        )

                    continue

                task = AnnotationTaskFactory.create(annotation_unit.genomic_unit, annotation_unit.dataset)
                logger.info(
                    '%s Creating Task To Annotate...',
                    annotation_unit_string(annotation_unit.get_genomic_unit(), annotation_unit.get_dataset())
                )

                annotation_task_futures[executor.submit(task.annotate)] = (annotation_unit.genomic_unit, task)

                for future in concurrent.futures.as_completed(annotation_task_futures):
                    annotation_unit.genomic_unit, annotation_task = annotation_task_futures[future]
                    logger.info(
                        '%s Query completed...',
                        annotation_unit_string(annotation_unit.get_genomic_unit(), annotation_unit.get_dataset())
                    )

                    try:
                        result_temp = future.result()

                        for annotation in annotation_task.extract(result_temp):
                            logger.info(
                                '%s Saving %s...',
                                annotation_unit_string(
                                    annotation_unit.get_genomic_unit(), annotation_task.dataset['data_set']
                                ), annotation['value']
                            )
                            genomic_unit_collection.annotate_genomic_unit(annotation_task.genomic_unit, annotation)

                    except FileNotFoundError as error:
                        logger.info(
                            '%s exception happened %s with %s and %s', annotation_log_label(), error,
                            annotation_unit.genomic_unit, annotation_task
                        )

                    del annotation_task_futures[future]

            logger.info("%s Processing annotation tasks queue complete", annotation_log_label())
