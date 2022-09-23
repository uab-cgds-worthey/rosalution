"""
Class to support the importing of phenotips data
"""
import warnings


class PhenotipsImporter:
    """imports the incoming phenotips json data"""

    def __init__(self, analysis_collection, genomic_unit_collection):
        """Initializes with the Rosalution repositories analysis and genomic unit which wrap 'PyMongo'"""
        self.analysis_collection = analysis_collection
        self.genomic_unit_collection = genomic_unit_collection

    def import_phenotips_json(self, phenotips_json_data):
        """Imports the phenotips json data into the database"""
        phenotips_json_data = phenotips_json_data.dict()
        phenotips_variants = []
        variant_annotations = ["inheritance", "zygosity",
                               "interpretation", "transcript",
                               "cdna", "reference_genome",
                               "protein", "gene"]

        for variant in phenotips_json_data["variants"]:
            variant_data = {}
            for annotation in variant_annotations:
                if annotation in variant:
                    variant_data[annotation] = variant[annotation]
            if 'gene' in variant_data:
                for gene in phenotips_json_data["genes"]:
                    if gene['id'] == variant_data['gene']:
                        variant_data['gene'] = gene['gene']

            phenotips_variants.append(variant_data)

        # It looks like we're just overwriting the set gene in variant to be the last gene?
        # for gene in phenotips_json_data["genes"]:
        #     for phenotips_variant in phenotips_variants:
        #         phenotips_variant["gene"] = gene["gene"]

        # Commenting this, we assume that each variant has an associated gene. Otherwise we don't handle it.

        for gene in phenotips_json_data["genes"]:
            genomic_unit_data = self.import_genomic_unit_collection_data(gene, "gene")
            self.genomic_unit_collection.create_genomic_unit(genomic_unit_data)

        for variant in phenotips_variants:
            genomic_unit_data = self.import_genomic_unit_collection_data(variant, "hgvs")
            self.genomic_unit_collection.create_genomic_unit(genomic_unit_data)

        analysis_data = self.import_analysis_data(phenotips_json_data, phenotips_variants, phenotips_json_data["genes"])
        self.analysis_collection.create_analysis(analysis_data)
        return analysis_data

    @staticmethod
    def import_genomic_unit_collection_data(data, data_format):
        """Formats the genomic unit data from the phenotips.json file"""
        if data_format == "hgvs":
            genomic_data = {
                "hgvs_variant": str(data["transcript"] + ":" + data["cdna"]),
                "chromosome": "",
                "position": "",
                "reference": "",
                "alternate": "",
                "build": data['reference_genome'],
                "transcripts": [],
                "annotations": [],
            }
        elif data_format == "gene":
            genomic_data = { "gene_symbol": data['gene'], "gene": data['gene'], "annotations": []}
        else:
            warnings.warn(
                "Invalid data format for import_genomic_unit_collection_data method")
            return None
        return genomic_data

    def import_analysis_data(self, phenotips_json_data, phenotips_variants, phenotips_genes):
        """Formats the analysis data from the phenotips.json file"""

        analysis_data = {
            "name": str(phenotips_json_data["external_id"]).replace("-", ""),
            "description": "",
            "nominated_by": "",
            "latest_status": "Annotation",  # set as Annotation as default for now
            "created_date": str(phenotips_json_data["date"]).split(" ", maxsplit=1)[0],
            "last_modified_date": str(phenotips_json_data["last_modification_date"]).split(" ", maxsplit=1)[0],
            "genomic_units": [],
            "sections": [{
                "header": 'Brief',
                "content": [
                    {"field": 'Nominated', "value": []},
                    {"field": 'Reason', "value": []},
                    {"field": 'Desired Outcomes', "value": []}
                ]
            }, {
                "header": 'Medical Summary',
                "content": [
                    {"field": 'Clinical Diagnosis', "value": []},
                    {"field": 'Affected Individuals Identified', "value": []}
                ]
            }, {
                "header": 'Case Information',
                "content": [
                    {"field": 'Systems', "value": []},
                    {"field": 'HPO Terms', "value": []},
                    {"field": 'Additional Details', "value": []},
                    {"field": 'Experimental Design', "value": []},
                    {"field": 'Prior Testing', "value": []}
                ]
            }]
        }

        for phenotips_gene in phenotips_genes:
            analysis_unit = {
                "gene": phenotips_gene["gene"],
                "transcripts": [],
                "variants": [],
            }

            for phenotips_variant in phenotips_variants:
                if phenotips_variant['gene'] == phenotips_gene['gene']:
                    analysis_unit['variants'].append({
                        "hgvs_variant": str(phenotips_variant["transcript"] + ":" + phenotips_variant["cdna"]),
                        "c_dot": phenotips_variant["cdna"],
                        # "p_dot": phenotips_variant["protein"],
                        "p_dot": "",
                        "build": str(phenotips_variant['reference_genome']),
                        "case": self.format_case_data(phenotips_variant)
                    })
                
                if 'transcript' in phenotips_variant:
                    new_transcript = { 'transcript': phenotips_variant['transcript'] }
                    if new_transcript not in analysis_unit['transcripts']:
                        analysis_unit['transcripts'].append(new_transcript)
            
            analysis_data['genomic_units'].append(analysis_unit)
        
        return analysis_data

    @ staticmethod
    def format_case_data(variant_data):
        """Formats the case data from the phenotips.json file using the variant data"""
        case_data = []
        genomic_unit_case_annotations = {
            "interpretation": "Interpretation",
            "zygosity": "Zygosity",
            "inheritance": "Inheritance",
        }

        for annotation in genomic_unit_case_annotations.items():
            phenotips_json_attribute = annotation[0]
            case_annotation = annotation[1]

            if variant_data[phenotips_json_attribute]:
                case_data.append(
                    {
                        "field": case_annotation,
                        "value": [str(variant_data[phenotips_json_attribute])],
                    }
                )
        return case_data
