"""
Collection with retrieves, creates, and modify analyses.
"""
from pymongo import ReturnDocument


class AnalysisCollection:
    """Repository to access analyses for projects"""

    def __init__(self, analysis_collection):
        """Initializes with the 'PyMongo' Collection object for the Analyses collection"""
        self.collection = analysis_collection

    def all(self):
        """Returns all analyses within the system"""
        return list(self.collection.find())

    def all_summaries(self):
        """Returns all of the summaries for all of the analyses within the system"""

        query_result = self.collection.find({}, {
            "name": 1,
            "description": 1,
            "genomic_units": 1,
            "nominated_by": 1,
            "latest_status": 1,
            "created_date": 1,
            "last_modified_date": 1,
        })

        summaries = []
        for summary in query_result:
            genes_list = map(
                lambda unit: unit['gene'], summary['genomic_units'])
            genes_string_list = ', '.join(genes_list)

            transcripts_list = [[transcript_unit['transcript']
                                 for transcript_unit in unit['transcripts']] for unit in summary['genomic_units']]
            flattened_transcripts_list = [
                transcript for transcript_items in transcripts_list for transcript in transcript_items]

            variant_list = [variant['c_dot'] for genomic_unit in summary['genomic_units']
                            for variant in genomic_unit['variants'] if variant['c_dot']]

            genomic_units_summary = [{
                "gene": genes_string_list,
                "transcripts": flattened_transcripts_list,
                "variants": variant_list
            }]

            summary['genomic_units'] = genomic_units_summary
            summaries.append(summary)

        return summaries

    def find_by_name(self, name: str):
        """Returns analysis by searching for name"""
        return self.collection.find_one({"name": name})

    def create_analysis(self, analysis_data: dict):
        """Creates a new analysis if the name does not already exist"""
        if self.collection.find_one({"name": analysis_data["name"]}) is not None:
            raise ValueError(
                f"Analysis with name {analysis_data['name']} already exists")

        # returns an instance of InsertOneResult.
        return self.collection.insert_one(analysis_data)

    def update_analysis(self, name: str, updated_analysis_data: dict):
        """Updates an existing analysis"""
        updated_document = self.collection.find_one_and_update({"name": name},
                                                               {"$set": updated_analysis_data},
                                                               return_document=ReturnDocument.AFTER)
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document
