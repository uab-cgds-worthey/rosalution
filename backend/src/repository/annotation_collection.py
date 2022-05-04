"""
Manges the annotation configuration of various genomic units
according to the type of Genomic Unit.
"""

from ..utils import read_fixture


class AnnotationCollection():
    """Repository for querying configurations for annotation"""
    def all(self):
        """Returns all annotation configurations"""
        return read_fixture("annotation-sources.json")

    def datasets_configuration(self, types):
        """gets dataset configurations according to the types"""
        configuration = self.all()
        return [dataset for dataset in configuration if dataset['type'] in types]
