"""
Collection with retrieves, creates, and modify analyses.
"""

from repository.annotation_collection import AnnotationCollection

class AnnotationService:
  def __init__(self, annotation_collection: AnnotationCollection):
    self.annotation_collection = annotation_collection
  
  def annotate(self, units, types):
    print(units)
    return self.annotation_collection.getDataSetsConfiguration(types)
