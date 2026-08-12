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

    async def all_projects(self, client_id: str) -> list:
        """Returns all projects available to the user by client id"""
        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "projects", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$_id", "$$projectIds"]}}}], "as": "projects"
            }
        }, {"$unwind": "$projects"}, {"$replaceRoot": {"newRoot": "$projects"}}]

        query_result = await self.user_collection.aggregate(pipeline)

        return await query_result.to_list()

    async def all_analyses(self, client_id: str) -> list:
        """Returns all analyses available to the user by client id"""
        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "analyses", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$project_id", "$$projectIds"]}}}], "as": "analyses"
            }
        }, {"$unwind": "$analyses"}, {"$replaceRoot": {"newRoot": "$analyses"}},
                    {"$project": AnalysisCollectionSummary.query_projection()}]

        query_result = await self.user_collection.aggregate(pipeline)

        return await query_result.to_list()

    async def all_summaries(self, client_id: str) -> list:
        """Returns all of the summaries for all of the analyses within the system"""

        pipeline = [{"$match": {"client_id": client_id}}, {
            "$lookup": {
                "from": "analyses", "let": {"projectIds": '$project_ids'},
                "pipeline": [{"$match": {"$expr": {"$in": ["$project_id", "$$projectIds"]}}}], "as": "analyses"
            }
        }, {"$unwind": "$analyses"}, {"$replaceRoot": {"newRoot": "$analyses"}},
                    {"$project": AnalysisCollectionSummary.query_projection()}]

        summaries = []

        async with await self.user_collection.aggregate(pipeline) as cursor:
            async for analysis in cursor:
                genomic_unit_summaries = AnalysisCollectionSummary.omic_unit_json_summary(analysis['genomic_units'])
                analysis['genomic_units'] = genomic_unit_summaries
                summaries.append(analysis)

        return summaries
