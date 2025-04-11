"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import time
from requests.exceptions import JSONDecodeError
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
                annotation_unit_queued = AnnotationUnit(genomic_unit, dataset, analysis_name=analysis.name)
                annotation_task_queue.put(annotation_unit_queued)

    @staticmethod
    def process_tasks(
        annotation_queue: AnnotationQueue, genomic_unit_collection: GenomicUnitCollection,
        analysis_collection: AnalysisCollection
    ):  # pylint: disable=too-many-branches,too-many-locals
        """Processes items that have been added to the queue"""
        logger.info("%s Processing annotation tasks queue ...", annotation_log_label())

        processor = AnnotationProcess(annotation_queue, genomic_unit_collection, analysis_collection)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as task_executor:
            processor.set_tasks_executor(task_executor)

            while not processor.annotation_unit_queue_empty() or processor.are_tasks_processing():
                annotation_unit = processor.queue.get()

                processor.process_annotation_unit(annotation_unit)
                for task_future in concurrent.futures.as_completed(processor.annotation_task_futures):
                    processor.on_task_complete(task_future)

            logger.info("%s Processing annotation tasks queue complete", annotation_log_label())


class AnnotationProcess():
    """Processes the annotation queue for annotations"""

    def __init__(
        self, annotation_queue: AnnotationQueue, genomic_unit_collection: GenomicUnitCollection,
        analysis_collection: AnalysisCollection
    ):
        """
        Initializes the annotation process to take a queue of AnnotationUnits and run the tasks to annotate them.
        """
        self.queue = annotation_queue
        self.genomic_unit_collection = genomic_unit_collection
        self.analysis_collection = analysis_collection

        self.annotation_task_futures = {}
        self.version_cache = {}

        self.task_executor = None

    def set_tasks_executor(self, task_executor):
        """Sets the task executor for handling the annotate tasks."""
        self.task_executor = task_executor

    def annotation_unit_queue_empty(self) -> bool:
        """Checks if the annotations queue is empty."""
        return self.queue.empty()

    def are_tasks_processing(self) -> bool:
        """"Returns True if there are annotation tasks processing, otherwise returns False."""
        return len(self.annotation_task_futures) > 0

    def queue_task_in_tasks_worker(self, task):
        """Submits an Annotation task to run within the task executor pool."""
        self.annotation_task_futures[self.task_executor.submit(task.annotate)] = task

    def process_annotation_unit(self, annotation_unit):
        """
        Processes an individual annotation unit by handling versions and its dependencies needed before an
        annotation task can be created. If the annotation unit is ready to annotate, it will be submitted to run
        on the task execeutor thread pool.
        """
        if not annotation_unit.version_exists():
            self.handle_annotation_unit_version_calcuation(annotation_unit)
            return
        
        dataset_in_manifest = self.analysis_collection.get_manifest_dataset_config(annotation_unit.analysis_name, annotation_unit.get_dataset_name())
        if dataset_in_manifest:
            if annotation_unit.get_dataset_name() == "CADD":
                logger.warning("NOT IN MANIFEST?")
            checing_annotation_unit = AnnotationUnit(annotation_unit.genomic_unit, annotation_unit.dataset, annotation_unit.analysis_name)
            try:

                checing_annotation_unit.set_latest_version(dataset_in_manifest[annotation_unit.get_dataset_name()].version)
                if annotation_unit.get_dataset_name() == "CADD":
                    logger.warning("WHY IS CADD DOING THE THING")
                    logger.warning(checing_annotation_unit.get_version())
                if not self.genomic_unit_collection.annotation_exist(checing_annotation_unit):
                    logger.warning("%s Annotation Exists in Manifest but does not have annotation saved", format_annotation_logging(annotation_unit))
            except KeyError as error:
                logger.warning(error)
                logger.warning(dataset_in_manifest)

        if self.genomic_unit_collection.annotation_exist(annotation_unit):
            logger.info('%s Annotation Exists...', format_annotation_logging(annotation_unit))
            return

        if annotation_unit.has_dependencies():
            self.handle_annotation_unit_dependencies(annotation_unit)

        if not annotation_unit.conditions_met_to_gather_annotation():
            if annotation_unit.should_continue_annotation():
                logger.info(
                    '%s Delaying Annotation, Missing %s Dependencies %s/10 times...',
                    format_annotation_logging(annotation_unit), annotation_unit.get_missing_conditions(),
                    annotation_unit.get_delay_count() + 1
                )
                self.queue.put(annotation_unit)
                time.sleep(0)
                # time.sleep(1)
            else: 
                logger.info(
                    '%s Canceling Annotation, Missing %s Dependencies...', format_annotation_logging(annotation_unit),
                    annotation_unit.get_missing_conditions()
                )
            return

        annotation_task = AnnotationTaskFactory.create_annotation_task(annotation_unit)
        logger.info('%s Creating Task To Annotate...', format_annotation_logging(annotation_unit))

        self.queue_task_in_tasks_worker(annotation_task)

    def on_task_complete(self, future):
        """
        Runs on a completed future that contains the annotation unit that was executed. Will extract the
        annotation or version. Save it to the database or put the annotation unit back on the queue with its version.
        """
        task = self.annotation_task_futures[future]
        annotation_unit = task.annotation_unit

        try:
            task_process_result = future.result()

            if isinstance(task, VersionAnnotationTask):
                version_cache_id = task.get_version_cache_id()
                version = task.extract_version(task_process_result)

                self.set_version_in_cache(version_cache_id, version)
                annotation_unit.set_latest_version(version)

                logger.info('%s Version Calculated %s...', format_annotation_logging(annotation_unit), version)
                self.queue.put(annotation_unit)
            else:
                for annotation in task.extract(task_process_result):
                    # if(annotation_unit.get_dataset_name() == 'ClinVar_Variant_Id' and "NM_001360016.2:c.563C>T" in annotation_unit.to_name_string()):
                    #     logger.warning(
                    #         '%s ProcessTaskResult for ClinVar_Variant_id %s...',
                    #         format_annotation_logging(annotation_unit,
                    #                                 annotation_unit.get_dataset_name()), task_process_result
                    #     )
                    logger.info(
                        '%s Saving %s...',
                        format_annotation_logging(annotation_unit,
                                                  annotation_unit.get_dataset_name()), annotation['value']
                    )

                    self.genomic_unit_collection.annotate_genomic_unit(annotation_unit.genomic_unit, annotation)
                    self.analysis_collection.add_dataset_to_manifest(annotation_unit.analysis_name, annotation_unit)

        except FileNotFoundError as error:
            logger.error(
                '%s Exception [%s] with Not Found [%s]', format_annotation_logging(annotation_unit), error, task
            )
            logger.exception(error)
        except (JSONDecodeError, TypeError) as exceptionError:
            logger.error(
                '%s Exception [%s] with note: %s', format_annotation_logging(annotation_unit), exceptionError
            )
            logger.exception(exceptionError)
        except RuntimeError as runtimeError:
            logger.error('%s Exception [%s] with [%s]', format_annotation_logging(annotation_unit), runtimeError, task)
            logger.exception(runtimeError)

        del self.annotation_task_futures[future]

    def is_version_cache_setup(self, version_cache_id: str) -> bool:
        """Returns True if the Version with its version_cache_id is setup within the cache"""
        return version_cache_id in self.version_cache

    def setup_version_cache(self, version_cache_id: str):
        """Setups up the version cache for the version cache id. """
        self.version_cache[version_cache_id] = ""

    def is_version_cached(self, version_cache_id: str) -> bool:
        """ Returns True if the version cache id has a version cached, otherwise returns False."""
        return self.version_cache[version_cache_id] != ""

    def set_version_in_cache(self, version_cache_id: str, version):
        """Sets the version to be cached in the version cache"""
        self.version_cache[version_cache_id] = version

    def handle_annotation_unit_version_calcuation(self, annotation_unit):
        """
        Processes the annotation unit to derive the annotation unit's calculated version according to the configuration.
        If the version of that annotation source exists in the version cache.  
        """
        version_task = AnnotationTaskFactory.create_version_task(annotation_unit)
        version_cache_id = version_task.get_version_cache_id()
        logger.info("%s Creating Version Cache Id...%s", format_annotation_logging(annotation_unit), version_cache_id)

        if not self.is_version_cache_setup(version_cache_id):
            logger.info('%s Creating Task To Version...', format_annotation_logging(annotation_unit))
            self.setup_version_cache(version_cache_id)
            self.queue_task_in_tasks_worker(version_task)
            return

        if self.is_version_cached(version_cache_id):
            logger.debug("Version Cache... %s", self.version_cache)
            cached_version = self.version_cache[version_cache_id]
            logger.info("%s Version Cache Exists for %s... %s", format_annotation_logging(annotation_unit), version_cache_id, cached_version)
            annotation_unit.set_latest_version(cached_version)
            logger.info(
                '%s Version Gathered from Cache %s...', format_annotation_logging(annotation_unit), cached_version
            )
        self.queue.put(annotation_unit)

    def handle_annotation_unit_dependencies(self, annotation_unit):
        """Retrieves the an annotation unit's dependencies if they exist."""
        missing_dependencies = annotation_unit.get_missing_dependencies()
        for missing_dataset_name in missing_dependencies:
            analysis_manifest_dataset = self.analysis_collection.get_manifest_dataset_config(
                annotation_unit.analysis_name, missing_dataset_name
            )

            # if(missing_dataset_name == 'pos'):
            #     logger.warning('whats going on with psoition: handle_annotation_dependencies_missing_dataset_name')
            #     logger.warning(analysis_manifest_dataset)

            if analysis_manifest_dataset is None:
                continue

            dependency_annotation_unit = self._create_temporary_annotation_unit(
                annotation_unit.genomic_unit, analysis_manifest_dataset, annotation_unit.analysis_name
            )

            # if(missing_dataset_name == 'pos'):
            #     logger.warning('whats going on with psoition: handle_annotation_dependencies_missing_dataset_name')
            #     logger.warning(dependency_annotation_unit.to_name_string())
            #     logger.warning('------ got from manifest')        

            annotation_value = self.genomic_unit_collection.find_genomic_unit_annotation_value(
                dependency_annotation_unit
            )

            # if(missing_dataset_name == 'pos'):
            #     logger.warning('whats going on with psoition: handle_annotation_dependencies_missing_dataset_name')
            #     logger.warning(annotation_value)
            #     logger.warning('------ got the value')      

            if annotation_value:
                # if(missing_dataset_name == 'pos'):
                #     logger.warning('setting the missing value')
                annotation_unit.set_annotation_for_dependency(missing_dataset_name, annotation_value)

        if annotation_unit.if_transcript_needs_provisioning() :
            transcript_id_manifest_dataset = self.analysis_collection.get_manifest_dataset_config(
                annotation_unit.analysis_name, "transcript_id"
            )

            if transcript_id_manifest_dataset is not None:
                transcript_id_manifest_dataset['transcript'] = True
                # if( "NM_001017980.3:c.164G>T" in annotation_unit.to_name_string() ):
                #     logger.warning("%s handle_annotation_unit_dependencies(): transcript_id in Manifest", format_annotation_logging(annotation_unit))
                #     logger.warning(transcript_id_manifest_dataset)
                #     logger.warning('looking for the transcript_id in manifest for annotation_unit')
                transcript_id_annotation_unit = self._create_temporary_annotation_unit(
                    annotation_unit.genomic_unit, transcript_id_manifest_dataset, annotation_unit.analysis_name
                )

                transcript_id_dataset_saved = self.genomic_unit_collection.annotation_exist(transcript_id_annotation_unit)

                # if( "NM_001017980.3:c.164G>T" in annotation_unit.to_name_string() ):
                #     logger.warning("%s handle_annotation_unit_dependencies(): transcript_id saved in database %s", format_annotation_logging(annotation_unit), transcript_id_dataset_saved)
                if transcript_id_dataset_saved:
                    annotation_unit.set_transcript_provisioned(True)
            else:
                # if( "NM_001360016.2:c.563C>T" in annotation_unit.to_name_string() ):
                # logger.warning("%s handle_annotation_unit_dependencies(): transcript_id is not in manifest. rip.s", format_annotation_logging(annotation_unit))
                pass

    def _create_temporary_annotation_unit(self, genomic_unit, manifest_dataset, analysis_name ):
        """private helper method to create a temporary annotation unit for finding within repository"""
        temporary = AnnotationUnit(genomic_unit, manifest_dataset, analysis_name)
        temporary.set_latest_version(manifest_dataset['version'])

        return temporary