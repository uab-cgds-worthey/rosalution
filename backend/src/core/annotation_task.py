"""Tasks for annotating a genomic unit with datasets"""
from abc import abstractmethod
from datetime import date
import json
from random import randint
import time

import logging
import jq
import requests

from ..core.annotation_unit import AnnotationUnit

logger = logging.getLogger(__name__)


def empty_gen():
    """
    Creates an empty iterator the emulate an empty return from extracting
    an annotation.  This is for use when there is a failure in extracting
    using jq.
    """
    yield from ()


class AnnotationTaskInterface:
    """Abstract class to define the interface for the the types of Annotation Task"""

    def __init__(self, annotation_unit: AnnotationUnit):
        self.annotation_unit = annotation_unit

    def aggregate_string_replacements(self, base_string) -> str:
        """
        Replaces the content 'base_string' where strings within the pattern
        {item} are replaced, 'item' can be the genomic unit's type such as
        {gene} or {hgvs_variant} or a dataset dependency, such as {Entrez Gene Id}.

        The follow are examples of the genomic_unit's dict's attributes like
        genomic_unit['gene'] or genomic_unit['Entrez Gene Id']

        example base string:
            https://grch37.rest.ensembl.org/vep/human/hgvs/{hgvs_variant}?content-type=application/json;CADD=1;refseq=1;
        return value: 
        https://grch37.rest.ensembl.org/vep/human/hgvs/NM_001017980.3:c.164G>T?content-type=application/json;CADD=1;refseq=1;
        
        example base string:
        .[].transcript_consequences[] | select( .transcript_id | contains(\"{transcript}\") ) | { CADD: .cadd_phred }
        
        return value: 
        .[].transcript_consequences[] | select( .transcript_id | contains(\"NM_001017980\") ) | { CADD: .cadd_phred }

        genomic unit within the annotation unit in this task to be
        {
            'hgvs_variant': "hgvs_variant",
            'transcript': 'NM_001017980',
        }
        """
        genomic_unit_string = f"{{{self.annotation_unit.get_genomic_unit_type()}}}"
        replace_string = base_string.replace(genomic_unit_string, self.annotation_unit.get_genomic_unit())

        if self.annotation_unit.has_dependencies():
            for dependency in self.annotation_unit.get_dependencies():
                dependency_string = f"{{{dependency}}}"
                replace_string = replace_string.replace(
                    dependency_string, str(self.annotation_unit.genomic_unit[dependency])
                )

        return replace_string

    @abstractmethod
    def annotate(self):
        """Interface for implementation of of retrieving the annotation for a genomic unit and its set of datasets"""

    def __json_extract__(self, jq_query, json_to_parse):
        """Private ethod to execute jq to extract JSON"""
        jq_results = iter(jq.compile(jq_query).input(json_to_parse).all())
        return jq_results

    def extract(self, incomming_json):
        """ Interface extraction method for annotation tasks """
        annotations = []

        # The following if statement has grown too large, however it would needs
        # to be refactored at a later time
        if 'attribute' in self.annotation_unit.dataset:  # pylint: disable=too-many-nested-blocks
            annotation_unit_json = {
                "data_set": self.annotation_unit.dataset['data_set'],
                "data_source": self.annotation_unit.dataset['data_source'], "value": "",
                "version": self.annotation_unit.version
            }

            jq_results = empty_gen()
            try:
                replaced_attributes = self.aggregate_string_replacements(self.annotation_unit.dataset['attribute'])
                jq_results = self.__json_extract__(replaced_attributes, incomming_json)
            except ValueError as value_error:
                logger.info((
                    'Failed to annotate "%s" from "%s" on %s with error "%s"', annotation_unit_json['data_set'],
                    annotation_unit_json['data_source'], json.dumps(incomming_json), value_error
                ))
            jq_result = next(jq_results, None)
            while jq_result is not None:
                print(jq_result)
                result_keys = list(jq_result.keys())

                if 'transcript' in self.annotation_unit.dataset:
                    transcript_annotation_unit = annotation_unit_json.copy()
                    for key in result_keys:
                        if key == 'transcript_id':
                            transcript_identifier = jq_result['transcript_id']
                            transcript_annotation_unit['transcript_id'] = transcript_identifier
                            if transcript_annotation_unit['value'] == '':
                                transcript_annotation_unit['value'] = transcript_identifier
                        else:
                            transcript_annotation_unit['value'] = jq_result[key]
                    annotations.append(transcript_annotation_unit)
                else:
                    annotation_unit_json['value'] = jq_result[result_keys[0]]
                    annotations.append(annotation_unit_json)

                jq_result = next(jq_results, None)

        return annotations

    def extract_version(self, incoming_version_json):
        """ Interface extraction method for Version Annotation tasks"""

        version = ""

        versioning_type = self.annotation_unit.get_dataset_version_type()
        if versioning_type == "rosalution":
            version = incoming_version_json["rosalution"]
        elif versioning_type == "date":
            version = incoming_version_json["date"]
        else:
            jq_query = self.annotation_unit.dataset['version_attribute']

            jq_result = empty_gen()
            try:
                jq_result = self.__json_extract__(jq_query, incoming_version_json)
            except ValueError as value_error:
                logger.info(('Failed to extract version', value_error))
            jq_result = next(jq_result, None)
            version = jq_result

        return version


class ForgeAnnotationTask(AnnotationTaskInterface):
    """
    An annotation task that will construct a dataset string from a series of
    annotation depedencies and its genomic unit
    """

    def __init__(self, annotation_unit):
        """Instantiates the force annotation task with the genomic unit's json"""
        AnnotationTaskInterface.__init__(self, annotation_unit)

    def annotate(self):
        """
        Annotates the dataset.  Compiles the datasets 'base_string' and does an aggregate string replacement
        of the genomic unit and its dataset depedencies to generate the new dataset.  Will be returned within
        an object that has the name of the dataset as the attribute.
        """
        return {
            self.annotation_unit.dataset['data_set']:
                self.aggregate_string_replacements(self.annotation_unit.dataset['base_string'])
        }


class NoneAnnotationTask(AnnotationTaskInterface):
    """An empty annotation task to be a place holder for datasets that do not have an annotation type yet"""

    def __init__(self, annotation_unit):
        """Instantiates the annotation task for the fake annotation with a genomic unit"""
        AnnotationTaskInterface.__init__(self, annotation_unit)

    def annotate(self):
        """Creates a fake 'annotation' using a randomly generated pause time to a query io operation"""
        value = randint(0, 10)
        time.sleep(value)
        # logger.info(f'Slept: {value} - Fake annotation for {self.annotation_unit.genomic_unit["unit"]}'
        #             f' for dataset {self.dataset["data_set"]} from {self.dataset["data_source"]}\n')

        result = {'not-real': self.annotation_unit.dataset["data_set"]}
        return result


class CsvAnnotationTask(AnnotationTaskInterface):
    """Example placeholder for a future type of annotation task"""

    def __init__(self, annotation_unit):
        """Insantiates the annotation task associated with the genomic unit"""
        AnnotationTaskInterface.__init__(self, annotation_unit)

    def annotate(self):
        """placeholder for annotating a genomic unit"""
        return "not-implemented"


class HttpAnnotationTask(AnnotationTaskInterface):
    """Initializes the annotation that uses an HTTP request to fetch the annotation"""

    def __init__(self, annotation_unit):
        """initializes the task with the genomic_unit"""
        AnnotationTaskInterface.__init__(self, annotation_unit)

    def annotate(self):
        """builds the complete url and fetches the annotation with an http request"""
        url_to_query = self.build_url()
        result = requests.get(url_to_query, verify=False, headers={"Accept": "application/json"}, timeout=30)
        json_result = result.json()
        return json_result

    def build_url(self):
        """
        Builds the URL from the base_url and then appends the list of query parameters for the list of datasets.
        """
        return self.aggregate_string_replacements(self.annotation_unit.dataset['url'])


class VersionAnnotationTask(AnnotationTaskInterface):
    """An annotation task that gets the version of the annotation"""

    version_types = {}

    def __init__(self, annotation_unit):
        """initializes the task with the annotation_unit.genomic_unit"""
        AnnotationTaskInterface.__init__(self, annotation_unit)
        self.version_types = {
            "rest": self.get_annotation_version_from_rest, "rosalution": self.get_annotation_version_from_rosalution,
            "date": self.get_annotation_version_from_date
        }

    def annotate(self):
        """Gets version by versioning type and returns the version data to the annotation unit"""

        version_type = self.annotation_unit.dataset['versioning_type']
        version = ""

        if version_type not in self.version_types:
            logger.error(('Failed versioning: "%s" is an Invalid Version Type', version_type))
            return {}

        version = self.version_types[version_type]()
        return version

    def get_annotation_version_from_rest(self):
        """Gets version for rest type and returns the version data"""
        version = {"rest": "rosalution-manifest-00"}

        url_to_query = self.annotation_unit.dataset['version_url']
        result = requests.get(url_to_query, verify=False, headers={"Accept": "application/json"}, timeout=30)
        version = result.json()
        return version

    def get_annotation_version_from_rosalution(self):
        """Gets version for rosalution type and returns the version data"""

        version = {"rosalution": "rosalution-manifest-00"}
        return version

    def get_annotation_version_from_date(self):
        """Gets version for date type and returns the version data"""

        version = {"date": str(date.today())}
        return version


class AnnotationTaskFactory:
    """
    Factory that creates the annotation task according to the annotation type
    from a dataset's configuration.
    """

    tasks = {
        "http": HttpAnnotationTask, "csv": CsvAnnotationTask, "none": NoneAnnotationTask, "forge": ForgeAnnotationTask,
        "version": VersionAnnotationTask
    }

    @classmethod
    def register(cls, key: str, annotation_task_interface: AnnotationTaskInterface):
        """
        Allows the addition of new annotation tasks to be registered. Allowing the new annotation tasks to
        be created if this codebase gets abstracted to a library
        """
        cls.tasks[key] = annotation_task_interface

    @classmethod
    def create_annotation_task(cls, annotation_unit: AnnotationUnit):
        """
        Creates an annotation task with a genomic_units and dataset json.  Instantiates the class according to
        a datasets 'annotation_source_type' from the datasets configurtion.
        """
        # In the future, this could be modified to use a static function instead
        # and those would be set to the dict, or an additional dictionary
        annotation_task_type = annotation_unit.dataset["annotation_source_type"]
        new_task = cls.tasks[annotation_task_type](annotation_unit)
        # new_task.set(annotation_unit.dataset)
        return new_task

    @classmethod
    def create_version_task(cls, annotation_unit: AnnotationUnit):
        """
        Creates an annotation task with a genomic_units and dataset json.  Instantiates the class according to
        a datasets 'annotation_source_type' from the datasets configurtion.
        """
        new_task = cls.tasks["version"](annotation_unit)
        return new_task
