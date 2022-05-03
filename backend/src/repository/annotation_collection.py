"""
Manges the annotation configuration of various genomic units
according to the type of Genomic Unit. 
"""

from ..utils import read_fixture

class AnnotationCollection():
  def all(self):
    return read_fixture("annotation-sources.json")