"""
Collection with retrieves, creates, and modify analyses.
"""
from ..utils import read_fixture

class AnalysisCollection():
  def all(self):
    return read_fixture("analyses.json")
  
  def all_summaries(self):
    return read_fixture("analyses-summary.json")
  
  def find_by_name(self, name: str):
    """ Returns analysis by searching for name"""
    analyses = read_fixture("analyses.json")
    for analysis in analyses:
        analysis_name = analysis.get('name')
        if analysis_name == name:
            return analysis

    return None
