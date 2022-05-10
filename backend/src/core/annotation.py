"""
Models annotation sources.
"""
# pylint: disable=too-few-public-methods
from pydantic import BaseModel

from ..enums import GenomicUnitType


class AnnotationSource(BaseModel):
    """An annotation source that matches a data set with the type of data it is used to annotate and its source"""
    type: GenomicUnitType
    data_set: str
    data_source: str


# def is_ready(self, source):

    
# def process_url(self, source):
#     # build our URL from self.source.url
#     #                    self.source.identifier
#     #                    self.source.query_params

# def process_csv(self, source):
#     # source.filepath
#     #source.version