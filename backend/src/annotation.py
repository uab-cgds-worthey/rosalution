"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import queue
import requests

from functools import reduce

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


class AnnotationTask():

    def __init__(self, genomic_unit_json):
        self.datasets = []
        self.genomic_unit = genomic_unit_json
    
    @classmethod
    def create(cls, genomic_unit_json, dataset):
        instance = cls(genomic_unit_json)
        instance.append(dataset)
        return (instance.identifier, instance)

    def identifier(self):
        return None if not self.datasets else self.datasets[0].base_url(self.genomic_unit)

    def append(self, dataset: DataSetSource):
        self.datasets.append(dataset)
    
    # def annotate(self):
        

class HttpAnnotationTask(AnnotationTask):
    def __init__(self, genomic_unit_json):
        AnnotationTask.__init__(self, genomic_unit_json)

    def identifier(self):
      return None if not self.datasets else self.datasets[0].base_url(self.genomic_unit)
    
    def append(self, dataset: DataSetSource):
        self.datasets.append(dataset)
    
    def annotate(self):
        url_to_query = self.build_url()
        result = requests.get(url_to_query)
        return  f'Batching with an Annotation Task Object: \n {result.json()}'

    def build_url(self):
      base_url_string = self.base_url()
      query_param_list = map(lambda dataset: dataset.query_param, self.datasets)
      url = reduce(lambda url_string, query_param: url_string + query_param, query_param_list, base_url_string)
      return url if base_url_string is not None else None 

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
            batched_annotation_tasks = {}
            while not annotation_queue.empty():
                genomic_unit, dataset_json = annotation_queue.get()
                dataset = DataSetSource(**dataset_json)

                if(dataset.url is not None):
                    dataset_base_url = dataset.base_url(genomic_unit)
                    if(dataset_base_url not in batched_annotation_tasks):
                        log_to_file(f"{dataset_base_url}")
                        batched_annotation_tasks[dataset_base_url] = AnnotationTask(genomic_unit)
                    batched_annotation_tasks[dataset_base_url].append(dataset)
                    log_to_file(f"Batched: {genomic_unit} for datasets {dataset_json}\n")
                else:
                    log_to_file(f"Que: {genomic_unit} for datasets {dataset_json}\n")
                    annotation_task_futures[executor.submit(
                        dataset.annotate, genomic_unit)] = (genomic_unit, dataset)

            for batch_task in batched_annotation_tasks.values():
                annotation_task_futures[executor.submit(batch_task.annotate)] = (genomic_unit, batch_task)

            log_to_file('------done submitting tasks\n')

            for future in concurrent.futures.as_completed(annotation_task_futures):
                genomic_unit, dataset_json = annotation_task_futures[future]
                try:
                    log_to_file(f"{future.result()}")
                    if isinstance(dataset_json, AnnotationTask):
                      log_to_file(f'{dataset_json.datasets}')
                      log_to_file(f'{genomic_unit}')
                except FileNotFoundError as error:
                    log_to_file(f"exception happened {error}")
                except Exception as error:
                    log_to_file(f"exception happened {error}")

                log_to_file('\n')
                del annotation_task_futures[future]
            
            log_to_file('after for loop for waiting for all of the futures to finis\n\n')
