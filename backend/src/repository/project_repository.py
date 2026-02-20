"""
Collection with retrieves, creates, and modify projects.
"""

from .analysis_collection_summary import AnalysisCollectionSummary


class ProjectRepository:
    """Repository to access users and analyses for projects"""

    def __init__(self, user_collection, analysis_collection):
        """Initializes with the 'PyMongo' Collection object for projects collection"""
        self.user_collection = user_collection
        self.analysis_collection = analysis_collection

    def all_projects(self, client_id: str):
        """Returns all projects available to the user by client id"""
        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "projects", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$_id", "$$projectIds"]}}}], "as": "projects"
            }
        }, {"$unwind": "$projects"}, {"$replaceRoot": {"newRoot": "$projects"}}]

        query_result = self.user_collection.aggregate(pipeline)

        return list(query_result)

    def all_analyses(self, client_id: str):
        """Returns all analyses available to the user by client id"""
        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "analyses", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$project_id", "$$projectIds"]}}}], "as": "analyses"
            }
        }, {"$unwind": "$analyses"}, {"$replaceRoot": {"newRoot": "$analyses"}},
                    {"$project": AnalysisCollectionSummary.query_projection()}]

        query_result = self.user_collection.aggregate(pipeline)

        return list(query_result)

    def all_summaries(self, client_id: str):
        """Returns all of the summaries for all of the analyses within the system"""

        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "analyses", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$project_id", "$$projectIds"]}}}], "as": "analyses"
            }
        }, {"$unwind": "$analyses"}, {"$replaceRoot": {"newRoot": "$analyses"}}, {
            "$project": {
                "name": 1,
                "description": 1,
                "genomic_units": 1,
                "nominated_by": 1,
                "timeline": 1,
                "third_party_links": 1,
            }
        }]

        query_result = self.user_collection.aggregate(pipeline)

        summaries = []
        for analysis in query_result:
            genomic_unit_summaries = []
            for unit in analysis['genomic_units']:
                genomic_unit_summary = {}
                if unit.get('gene'):
                    genomic_unit_summary['gene'] = unit['gene']
                genomic_unit_summary['variants'] = []
                for variant in unit['variants']:
                    summary_variant = variant['hgvs_variant']
                    if variant['p_dot'] is not None:
                        summary_variant = f"{summary_variant}({variant['p_dot']})"
                    genomic_unit_summary['variants'].append(summary_variant)
                genomic_unit_summaries.append(genomic_unit_summary)
            analysis['genomic_units'] = genomic_unit_summaries
            summaries.append(analysis)

        return summaries
