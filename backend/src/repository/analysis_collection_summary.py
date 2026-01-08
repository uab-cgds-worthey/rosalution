"""
Module for queryihng and transforming Rosalution Analyses in MongoDB to create summaries.
"""


class AnalysisCollectionSummary:
    """A helper static class to support querying and transforming analyses json to a standard summary format """

    @staticmethod
    def query_projection():
        """The MongoDB projection argument to query the nessecary subset of fields for an analysis summary"""
        return {
            "name": 1,
            "description": 1,
            "genomic_units": 1,
            "nominated_by": 1,
            "timeline": 1,
            "third_party_links": 1,
        }

    @staticmethod
    def omic_unit_json_summary(genomic_units_by_query: list):
        """Transforms the 'omic units of an analysis to a standard summary structure"""
        genomic_unit_summaries = []
        for unit in genomic_units_by_query:
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

        return genomic_unit_summaries
