"""Tasks for annotating a genomic unit with datasets"""
from abc import abstractmethod
import json
from random import randint
import time

# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class
import jq
import requests

def log_to_file(string):
    """
    Temprorary utility function for development purposes abstracted for testing.
    Will remove once feature is completed.
    """
    with open("rosalution-annotation-log.txt", mode="a", encoding="utf-8") as log_file:
        log_file.write(string)
    print(string)


class AnnotationTaskInterface:
    """Abstract class to define the interface for the the types of Annotation Task"""

    def __init__(self, genomic_unit_json: dict):
        self.dataset = {}
        self.genomic_unit = genomic_unit_json

    def set(self, dataset: dict):
        """Adds the dataset configuration for the annotation"""
        self.dataset = dataset

    def aggregate_string_replacements(self, base_string):
        """
        Replaces the content 'base_string' where strings within the pattern
        {item} are replaced, 'item' can be the genomic unit's type such as
        {gene} or {hgvs_variant} or a dataset dependency, such as {Entrez Gene Id}.

        The follow are examples of the genomic_unit's dict's attributes like
        genomic_unit['gene'] or genomic_unit['Entrez Gene Id']
        """
        genomic_unit_string = f"{{{self.dataset['genomic_unit_type']}}}"
        # print(f"Replacing {genomic_unit_string} with {self.genomic_unit['unit']} in {base_string}")
        # print(f"{base_string.replace(genomic_unit_string, self.genomic_unit['unit'])}")

        replace_string = base_string.replace(genomic_unit_string, self.genomic_unit['unit'])

        if 'dependencies' in self.dataset:
            for dependency in self.dataset['dependencies']:
                dependency_string = f"{{{dependency}}}"
                replace_string = replace_string.replace(dependency_string, str(self.genomic_unit[dependency]))

        return replace_string

    @abstractmethod
    def annotate(self):
        """Interface for implementation of of retrieving the annotation for a genomic unit and its set of datasets"""

    def extract(self, json_result):
        """ Interface extraction method for annotation tasks """
        annotations = []

        log_to_file(f"{self.genomic_unit['unit']} for {self.dataset['data_set']} - Extract initation...\n")

        if 'attribute' in self.dataset:
            annotation_unit = {
                "data_set": self.dataset['data_set'],
                "data_source": self.dataset['data_source'],
                "version": "",
                "value": ""
            }

            replaced_attributes = self.aggregate_string_replacements(self.dataset['attribute'])

            jq_results = jq.compile(replaced_attributes).input(json_result).all()

            jq_results = iter(jq_results)

            jq_result = next(jq_results, None)
            while jq_result is not None:
                result_keys = list(jq_result.keys())

                if 'transcript' in self.dataset:
                    transcript_annotation_unit = annotation_unit.copy()
                    for key in result_keys:
                        if key == 'transcript_id':
                            transcript_annotation_unit['transcript_id'] = jq_result['transcript_id']
                        else:
                            transcript_annotation_unit['value'] = jq_result[key]
                    annotations.append(transcript_annotation_unit)
                else:
                    annotation_unit['value'] = jq_result[result_keys[0]]
                    log_to_file("DOING A DUMP\n")
                    log_to_file(f"{json.dumps(annotation_unit)}")
                    annotations.append(annotation_unit)

                jq_result = next(jq_results, None)

        return annotations


class NoneAnnotationTask(AnnotationTaskInterface):
    """An empty annotation task to be a place holder for datasets that do not have an annotation type yet"""

    def __init__(self, genomic_unit_json):
        """Instantiates the annotation task for the fake annotation with a genomic unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def annotate(self):
        """Creates a fake 'annotation' using a randomly generated pause time to a query io operation"""
        value = randint(0, 10)
        time.sleep(value)
        # log_to_file(f'Slept: {value} - Fake annotation for {self.genomic_unit["unit"]}'
        #             f' for dataset {self.dataset["data_set"]} from {self.dataset["data_source"]}\n')

        result = {'not-real': self.dataset["data_set"]}
        return result


class CsvAnnotationTask(AnnotationTaskInterface):
    """Example placeholder for a future type of annotation task"""

    def __init__(self, genomic_unit_json):
        """Insantiates the annotation task associated with the genomic unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def annotate(self):
        """placeholder for annotating a genomic unit"""
        return "not-implemented"


class HttpAnnotationTask(AnnotationTaskInterface):
    """Initializes the annotation that uses an HTTP request to fetch the annotation"""

    def __init__(self, genomic_unit_json):
        """initializes the task with the genomic_unit"""
        AnnotationTaskInterface.__init__(self, genomic_unit_json)

    def annotate(self):
        """builds the complete url and fetches the annotation with an http request"""
        log_to_file(f"{self.genomic_unit['unit']} for {self.dataset['data_set']} - Annotating...\n")
        url_to_query = self.build_url()
        log_to_file(f"{self.genomic_unit['unit']} for {self.dataset['data_set']} - {url_to_query}...\n")
        # log_to_file(f'No Sleep: {url_to_query} - Real annotation for {self.genomic_unit["unit"]}'
        #             f' for dataset {s][''elf.dataset["data_set"]} from {self.dataset["data_source"]}\n')
        # print('i hope this is not running')
        result = requests.get(url_to_query, verify=False)
        log_to_file(f"{self.genomic_unit['unit']} for {self.dataset['data_set']} - {url_to_query} Returned...\n")
        json_result = result.json()
        log_to_file(json.dumps(json_result))
        return json_result

    def base_url(self):
        """
        Creates the base url for the annotation according to the configuration.  Searches for string {genomic_unit_type}
        within the 'url' attribute and replaces it with the genomic_unit being annotated.
        """
        string_to_replace = f"{{{self.dataset['genomic_unit_type']}}}"
        replace_string = self.dataset['url'].replace(
            string_to_replace, self.genomic_unit['unit'])

        if 'dependencies' in self.dataset:
            for depedency in self.dataset['dependencies']:
                depedency_replace_string = f"{{{depedency}}}"
                replace_string = replace_string.replace(
                    depedency_replace_string, self.genomic_unit[depedency])
        return replace_string

    def build_url(self):
        """
        Builds the URL from the base_url and then appends the list of query parameters for the list of datasets.
        """
        return self.aggregate_string_replacements(self.dataset['url'])


class AnnotationTaskFactory:
    """
    Factory that creates the annotation task according to the annotation type
    from a dataset's configuration.
    """

    tasks = {
        "http": HttpAnnotationTask,
        "csv": CsvAnnotationTask,
        "none": NoneAnnotationTask,
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
        # In the future, this could be modified to use a static function instead
        # and those would be set to the dict, or an additional dictionary
        new_task = cls.tasks[dataset["annotation_source_type"]](
            genomic_unit_json)
        new_task.set(dataset)
        return new_task
