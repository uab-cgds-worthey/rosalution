"""
Collection with retrieves, creates, and modify analyses.
"""
from ..utils import read_fixture

# database_client = FunctionCallToMakeDatabase()
# database_client.db = 'database base'
# analysis_collection = AnalysisCollection(database_client.db['analysis'])

class AnalysisCollection():
    """Repository to access analyses for projects"""
    def __init__(self, db_client = {}):
        # self.db = db_client
        self.db_collection = db_client

    def all(self):
        """Returns all analyses within the system"""
        return read_fixture("analyses.json")

    def all_summaries(self):
        """Returns all of the summaries for all of the analyses within the system"""
        return read_fixture("analyses-summary.json")

    def find_by_name(self, name: str):
        """ Returns analysis by searching for name"""
        analyses = read_fixture("analyses.json")
        for analysis in analyses:
            analysis_name = analysis.get('name')
            if analysis_name == name:
                return analysis

        return None
