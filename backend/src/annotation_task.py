"""Tasks for annotating a genomic unit with datasets"""
from abc import abstractmethod
from random import randint
from functools import reduce
import time
import requests


class AnnotationTaskInterface():
    """ Abstract class to define the interface for the the types of Annotation Task"""

    def __init__(self, genomic_unit_json: dict):
        self.datasets = []
        self.genomic_unit = genomic_unit_json

    @abstractmethod
    def identifier(self):
        """Interface for implementations to create an identifer using a genomic unit and a dataset"""

    def append(self, dataset: dict):
        """Adds the dataset configuration to the list of datasets batched with this annotation"""
        self.datasets.append(dataset)

    @abstractmethod
    def annotate(self):
        """Interface for implementation of of retrieving the annotation for a genomic unit and its set of datasets"""


class NoneAnnotationTask(AnnotationTaskInterface):
    """An empty annotation task to be a place holder for datasets that do not have an annotation type yet"""

    def __init__(self, genomic_unit_json):
        """Instantiates the annotation task for the fake annotation with a genomic unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def identifier(self):
        """Bundles a genomic unit and the set of datasets by their source"""
        return f"{self.genomic_unit['unit']}-{self.datasets[0]['data_source']}"

    def annotate(self):
        """Createsa fake 'annotation' using a randomly generated pause time to a query io operation"""
        value = randint(0, 10)
        time.sleep(value)
        datasets_list = map(
            lambda dataset: dataset['data_set'], self.datasets)
        datasets_string = ', '.join(datasets_list)
        return \
            f'Slept: {value} - Fake annotation for {self.genomic_unit["unit"]}' \
            f'for datasets {datasets_string} from {self.datasets[0]["data_source"]}'


class CsvAnnotationTask(AnnotationTaskInterface):
    """ Example placeholder for a future type of annotation task """

    def __init__(self, genomic_unit_json):
        """Insantiates the annotation task associated with the genomic unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def identifier(self):
        """placeholder for generating a unique identifier of the task used to determine if a task exists already"""
        return 'not-implemented'

    def annotate(self):
        """placeholder for annotating a genomic unit"""
        return 'not-implemented'


class HttpAnnotationTask(AnnotationTaskInterface):
    """ Initializes the annotation that uses an HTTP request to fetch the annotation"""

    def __init__(self, genomic_unit_json):
        """initializes the task with the genomic_unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def identifier(self):
        """Uses the base url for the http request as an identifier for the annotation task"""
        return self.base_url()

    def annotate(self):
        """builds the complete url and fetches the annotation with an http request"""
        url_to_query = self.build_url()
        result = requests.get(url_to_query)
        return f'Batching with an Annotation Task Object: \n {result.json()}'

    def base_url(self):
        """
        creates the base url for the annotation according to the configuration,  searches for the {genomic_unit_type}
        within the 'url' attribute in the description and replaces it with the genomic_unit being annotated.
        """
        first_dataset = self.datasets[0]
        string_to_replace = f"{{{first_dataset['genomic_unit_type']}}}"
        return f"{first_dataset['url'].replace(string_to_replace, self.genomic_unit['unit'])};"

    def build_url(self):
        """
        Builds the URL from the base_url and then appends the list of query parameters for the list of datasets.
        """
        base_url_string = self.base_url()
        query_param_list = map(
            lambda dataset: dataset['query_param'], self.datasets)
        url = reduce(lambda url_string, query_param:
                     url_string + query_param,
                     query_param_list,
                     base_url_string
                     )
        return url if base_url_string is not None else None


class AnnotationTaskFactory():
    """
    Factory that creates the annotation task according to the annotation type from a dataset's configuration. This
    will determine the method used to create the unique identifier that bundles annotations.
    """
    tasks = {
        'http': HttpAnnotationTask,
        'csv': CsvAnnotationTask,
        'none': NoneAnnotationTask
    }

    @classmethod
    def register(cls, key: str, annotation_task_interface: AnnotationTaskInterface):
        """
        Allows the addition of new annotation tasks to be registered. Allowing the new annotation tasks to
        be created if this codebase gets abstracted to a library
        """
        cls.tasks[key] = annotation_task_interface

    @classmethod
    def create(cls, genomic_unit_json: dict, dataset: dict):
        """
        Creates an annotation task with a genomic_units and dataset json.  Instantiates the class according to
        a datasets 'annotation_source_type' from the datasets configurtion.
        """
        ### In the future, this could be modified to use a static function instead
        ### and those would be set to the dict, or an additional dictionary
        new_task = cls.tasks[dataset['annotation_source_type']](
            genomic_unit_json)
        new_task.append(dataset)
        return (new_task.identifier(), new_task)
