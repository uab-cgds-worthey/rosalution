"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import logging
import queue

from .annotation_logging import annotation_log_label, annotation_unit_string
from .annotation_task import AnnotationTaskFactory
from ..models.analysis import Analysis
from ..repository.annotation_config_collection import AnnotationConfigCollection

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
                annotation_task_queue.put((genomic_unit, dataset))

    @staticmethod
    def process_tasks(annotation_queue, genomic_unit_collection):  # pylint: disable=too-many-locals
        """Processes items that have been added to the queue"""
        logger.info("%s Processing annotation tasks queue ...", annotation_log_label())

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            annotation_task_futures = {}
            while not annotation_queue.empty():
                genomic_unit, dataset_json = annotation_queue.get()
                if genomic_unit_collection.annotation_exist(genomic_unit, dataset_json):
                    logger.info(
                        '%s %s Annotation Exists...',
                        annotation_log_label(),
                        annotation_unit_string(genomic_unit['unit'], dataset_json['data_set'])
                    )
                    continue

                ready = True
                if 'dependencies' in dataset_json:
                    missing_dependencies = [
                        dependency for dependency in dataset_json['dependencies'] if dependency not in genomic_unit
                    ]

                    for missing in missing_dependencies:
                        annotation_value = genomic_unit_collection.find_genomic_unit_annotation_value(
                            genomic_unit, missing
                        )
                        if annotation_value:
                            genomic_unit[missing] = annotation_value
                        else:
                            ready = False

                if not ready:
                    delay_count = dataset_json['delay_count'] + 1 if 'delay_count' in dataset_json else 0
                    dataset_json['delay_count'] = delay_count

                    if dataset_json['delay_count'] < 10:
                        logger.info(
                            '%s %s Delaying Annotation, Missing Dependency...',
                            annotation_log_label(),
                            annotation_unit_string(genomic_unit['unit'], dataset_json['data_set'])
                        )
                        annotation_queue.put((genomic_unit, dataset_json))
                    else:
                        missing_dependencies = [
                            dependency for dependency in dataset_json['dependencies'] if dependency not in genomic_unit
                        ]
                        logger.info(
                            '%s %s Canceling Annotation, Missing %s ...',
                            annotation_log_label(),
                            annotation_unit_string(genomic_unit['unit'], dataset_json['data_set']),
                            missing_dependencies 
                        )

                    continue

                task = AnnotationTaskFactory.create(genomic_unit, dataset_json)
                logger.info(
                    '%s %s Creating Task To Annotate...',
                    annotation_log_label(),
                    annotation_unit_string(genomic_unit['unit'], dataset_json['data_set'])
                )

                annotation_task_futures[executor.submit(task.annotate)] = (
                    genomic_unit,
                    task
                )

                for future in concurrent.futures.as_completed(annotation_task_futures):
                    genomic_unit, annotation_task = annotation_task_futures[future]
                    logger.info(
                        '%s %s Query completed...',
                        annotation_log_label(),
                        annotation_unit_string(genomic_unit['unit'], dataset_json['data_set'])
                    )

                    try:
                        result_temp = future.result()

                        for annotation in annotation_task.extract(result_temp):
                            # logger.info(
                            #     f'''{f"Annotation: {genomic_unit['unit']} for {annotation_task.dataset['data_set']}" :<75} Saving {annotation['value']}...'''
                            # )
                            logger.info(
                                '%s %s Saving %s...',
                                annotation_log_label(),
                                annotation_unit_string(genomic_unit['unit'], annotation_task.dataset['data_set']),
                                annotation['value']
                            )
                            genomic_unit_collection.annotate_genomic_unit(annotation_task.genomic_unit, annotation)

                    except FileNotFoundError as error:
                        # logger.info(f"Annotation: exception happened {error} with {genomic_unit} and {annotation_task}")
                        logger.info('%s exception happened %s with %s and %s',
                                    annotation_log_label(),
                                    error,
                                    genomic_unit,
                                    annotation_task
                        )

                    del annotation_task_futures[future]

            logger.info("%s ...after for loop for waiting for all of the futures to finish", annotation_log_label())
