"""
Collection with retrieves, creates, and modify analyses.
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added

from ..utils import read_fixture


class AnalysisCollection():
    """Repository to access analyses for projects"""
    # def __init__(self, analysis_collection):
    #     self.collection = analysis_collection

    def all(self):
        """Returns all analyses within the system"""
        return read_fixture("analyses.json")

    def all_summaries(self):
        """Returns all of the summaries for all of the analyses within the system"""
        return read_fixture("analyses-summary.json")

    def find_by_name(self, name: str):
        """ Returns analysis by searching for name"""
        print("and this is still happening?")
        analyses = read_fixture("analyses.json")
        for analysis in analyses:
            analysis_name = analysis.get('name')
            if analysis_name == name:
                return analysis

        return None
