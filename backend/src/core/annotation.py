"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import logging
import queue

from .annotation_task import AnnotationTaskFactory
from ..models.analysis import Analysis
from ..repository.annotation_config_collection import AnnotationConfigCollection
from ..core.annotation_unit import AnnotationUnit

# create logger
logger = logging.getLogger(__name__)

ANNOTATION_UNIT_PADDING = 75


def annotation_log_label():
    """
    Provides a label for logging in the annotation section to make it easier to search on.
    Changing this label will be uniform throughout the annotation section.
    """
    return 'Annotation:'


def format_annotation_logging(annotation_unit, dataset=""):
    """
    Provides a formatted string for logging that is consistent with
    annotation unit's genomic_unit and corresponding dataset to the console
    The string is padded to make the logs uniform and easier to read.
    """
    if dataset != "":
        annotation_unit_string = f"{annotation_unit.get_genomic_unit()} for {dataset}"
    else:
        annotation_unit_string = annotation_unit.to_name_string()
    return f"{annotation_log_label()} {annotation_unit_string}".ljust(ANNOTATION_UNIT_PADDING)


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
                latest = False
                if genomic_unit_collection.annotation_exist(annotation_unit.genomic_unit, annotation_unit.dataset
                                                           ) and annotation_unit.is_version_latest():
                    logger.info('%s Annotation Exists...', format_annotation_logging(annotation_unit))
                    latest = True
                    continue
                ready = True

                if annotation_unit.has_dependencies():
                    missing_dependencies = annotation_unit.get_missing_dependencies()
                    for missing in missing_dependencies:
                        annotation_value = genomic_unit_collection.find_genomic_unit_annotation_value(
                            annotation_unit.genomic_unit, missing
                        )
                        ready = annotation_unit.ready_for_annotation(annotation_value, missing)

                if not ready and not latest:
                    if annotation_unit.should_continue_annotation():
                        logger.info(
                            '%s Delaying Annotation, Missing %s Dependencies...',
                            format_annotation_logging(annotation_unit), annotation_unit.get_missing_dependencies()
                        )
                        annotation_queue.put(annotation_unit)
                    else:
                        logger.info(
                            '%s Canceling Annotation, Missing %s  Dependencies...',
                            format_annotation_logging(annotation_unit), annotation_unit.get_missing_dependencies()
                        )

                    continue

                task = AnnotationTaskFactory.create(annotation_unit.genomic_unit, annotation_unit.dataset)
                logger.info('%s Creating Task To Annotate...', format_annotation_logging(annotation_unit))

                annotation_task_futures[executor.submit(task.annotate)] = (annotation_unit.genomic_unit, task)

                for future in concurrent.futures.as_completed(annotation_task_futures):
                    annotation_unit.genomic_unit, annotation_task = annotation_task_futures[future]
                    logger.info('%s Query completed...', format_annotation_logging(annotation_unit))

                    try:
                        result_temp = future.result()

                        for annotation in annotation_task.extract(result_temp):
                            logger.info(
                                '%s Saving %s...',
                                format_annotation_logging(annotation_unit, annotation_task.dataset['data_set']),
                                annotation['value']
                            )
                            genomic_unit_collection.annotate_genomic_unit(annotation_task.genomic_unit, annotation)

                    except FileNotFoundError as error:
                        logger.info(
                            '%s exception happened %s with %s and %s', annotation_log_label(), error,
                            annotation_unit.genomic_unit, annotation_task
                        )

                    del annotation_task_futures[future]

            logger.info("%s Processing annotation tasks queue complete", annotation_log_label())
