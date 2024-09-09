"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import logging
import queue

from ..repository.analysis_collection import AnalysisCollection
from ..repository.genomic_unit_collection import GenomicUnitCollection

from .annotation_task import AnnotationTaskFactory, VersionAnnotationTask
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
    def process_tasks(
        annotation_queue: AnnotationQueue, analysis_name: str, genomic_unit_collection: GenomicUnitCollection,
        analysis_collection: AnalysisCollection
    ):  # pylint: disable=too-many-branches
        """Processes items that have been added to the queue"""
        logger.info("%s Processing annotation tasks queue ...", annotation_log_label())

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            annotation_task_futures = {}
            while not annotation_queue.empty():
                annotation_unit = annotation_queue.get()

                if not annotation_unit.version_exists():  #is configured dataset version calculated
                    version_task = AnnotationTaskFactory.create_version_task(annotation_unit)
                    logger.info('%s Creating Task To Version...', format_annotation_logging(annotation_unit))
                    annotation_task_futures[executor.submit(version_task.annotate)] = version_task
                else:
                    if genomic_unit_collection.annotation_exist(annotation_unit):
                        logger.info('%s Annotation Exists...', format_annotation_logging(annotation_unit))
                        continue

                    if annotation_unit.has_dependencies():
                        missing_dependencies = annotation_unit.get_missing_dependencies()
                        for missing_dataset_name in missing_dependencies:
                            # missing_dataset_name
                            dependency_dataset = analysis_collection.get_manifest_dataset_config(
                                analysis_name, missing_dataset_name
                            )
                            dependency_annotation_unit = AnnotationUnit(
                                annotation_unit.genomic_unit, dependency_dataset
                            )
                            annotation_value = genomic_unit_collection.find_genomic_unit_annotation_value(
                                dependency_annotation_unit
                            )
                            if annotation_value:
                                annotation_unit.set_annotation_for_dependency(missing_dataset_name, annotation_value)

                    if not annotation_unit.conditions_met_to_gather_annotation():
                        if annotation_unit.should_continue_annotation():  #maybe could try to annotation
                            logger.info(
                                '%s Delaying Annotation, Missing %s Dependencies %s/10 times...',
                                format_annotation_logging(annotation_unit), annotation_unit.get_missing_dependencies(),
                                annotation_unit.get_delay_count() + 1
                            )
                            annotation_queue.put(annotation_unit)
                        else:
                            logger.info(
                                '%s Canceling Annotation, Missing %s Dependencies...',
                                format_annotation_logging(annotation_unit), annotation_unit.get_missing_dependencies()
                            )
                        continue

                    annotation_task = AnnotationTaskFactory.create_annotation_task(annotation_unit)
                    logger.info('%s Creating Task To Annotate...', format_annotation_logging(annotation_unit))

                    annotation_task_futures[executor.submit(annotation_task.annotate)] = annotation_task

                for future in concurrent.futures.as_completed(annotation_task_futures):
                    task = annotation_task_futures[future]

                    try:
                        task_process_result = future.result()
                        if isinstance(task, VersionAnnotationTask):
                            annotation_unit = task.annotation_unit
                            annotation_unit.set_latest_version(task_process_result)
                            logger.info(
                                '%s Version Calculated %s...', format_annotation_logging(annotation_unit),
                                task_process_result
                            )
                            annotation_queue.put(annotation_unit)
                        else:
                            for annotation in task.extract(task_process_result):
                                logger.info(
                                    '%s Saving %s...',
                                    format_annotation_logging(annotation_unit, task.annotation_unit.get_dataset_name()),
                                    annotation['value']
                                )

                                genomic_unit_collection.annotate_genomic_unit(
                                    task.annotation_unit.genomic_unit, annotation
                                )
                                analysis_collection.add_dataset_to_manifest(analysis_name, annotation_unit)

                    except FileNotFoundError as error:
                        logger.info(
                            '%s exception happened %s with %s and %s', annotation_log_label(), error,
                            annotation_unit.genomic_unit, task
                        )

                    del annotation_task_futures[future]

            logger.info("%s Processing annotation tasks queue complete", annotation_log_label())
