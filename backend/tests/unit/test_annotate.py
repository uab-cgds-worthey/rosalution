
import pytest

from src.core.analysis import Analysis
from src.repository.analysis_collection import AnalysisCollection
from src.repository.annotation_collection import AnnotationCollection
from src.annotation_service import AnnotationService

def test_queuing_annotations_for_genomic_units(analysis, annotation_collection):
    unitsToAnnotate = analysis.unitsToAnnotate()
    typestoAnnotate = set(map(lambda x: x['type'], unitsToAnnotate))

    annotation_service = AnnotationService(annotation_collection)
    datasetsToAnnotation = annotation_service.annotate(unitsToAnnotate, typestoAnnotate)
    print('called annotate')
    print(datasetsToAnnotation)

@pytest.fixture
def analysis_collection():
  return AnalysisCollection()

@pytest.fixture
def analysis(analysis_collection):
  analysisJson = analysis_collection.find_by_name('CPAM0002')
  return Analysis(**analysisJson)

@pytest.fixture
def annotation_collection():
  return AnnotationCollection()