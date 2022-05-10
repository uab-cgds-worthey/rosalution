
from .repository.analysis_collection import AnalysisCollection
from .repository.annotation_collection import AnnotationCollection

class Database:
    def __init__(self, client: dict):
        self.client = client
        self.collections = {
          'analysis':  AnalysisCollection(),
          'annotation': AnnotationCollection
        }

    def __call__(self):
        return self.collections