"""
Collection with retrieves, creates, and modify analyses.
"""
# pylint: disable=no-self-use
# This linting disable will be removed once database is added

class AnalysisCollection:
    """Repository to access analyses for projects"""

    def __init__(self, analysis_collection):
        self.collection = analysis_collection

    def all(self):
        """Returns all analyses within the system"""
        return list(self.collection.find())

    def all_summaries(self):
        """Returns all of the summaries for all of the analyses within the system"""

        print("querrying all of the summaries for the analyses...")
        query_result =  self.collection.find({}, {
            "name": 1,
            "description": 1,
            "genomic_units": 1,
            "nominated_by": 1,
            "latest_status": 1,
            "created_date": 1,
            "last_modified_date": 1,
        })

        print(query_result)

        for summary in query_result:
            print(f"the summary{summary}")
            genes_list =  map(lambda unit: unit['gene'], summary.genomic_units)
            genes_string_list = ', '.join(genes_list)

            transcripts_list = [[ transcript_unit['transcript'] for transcript_unit in unit['transcripts']] for unit in summary.genomic_units]

            variants_list = map(lambda unit: (filter(lambda variant: variant['hgvs_variant']), unit['variants']), summary.variants)

            genomic_units_summary = [{
                "gene": genes_string_list,
                "transcripts": transcripts_list,
                "variants": variants_list
            }]
    
            summary.genomic_units = genomic_units_summary
        print(list(query_result))
        return list(query_result)

    def find_by_name(self, name: str):
        """Returns analysis by searching for name"""
        return self.collection.findOne( { "name": name } )
