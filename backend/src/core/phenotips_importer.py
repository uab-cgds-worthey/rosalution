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

        phenotips_variants = []
        variant_annotations = [
            "inheritance", "zygosity", "interpretation", "transcript", "cdna", "reference_genome", "protein", "gene"
        ]

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

        for gene in phenotips_json_data["genes"]:
            genomic_unit_data = self.import_genomic_unit_collection_data(gene, "gene")
            self.genomic_unit_collection.create_genomic_unit(genomic_unit_data)

        for variant in phenotips_variants:
            genomic_unit_data = self.import_genomic_unit_collection_data(variant, "hgvs")
            self.genomic_unit_collection.create_genomic_unit(genomic_unit_data)

        analysis_data = self.import_analysis_data(phenotips_json_data, phenotips_variants, phenotips_json_data["genes"])

        analysis_data['discussions'] = []
        analysis_data['attachments'] = []
        analysis_data['timeline'] = []
        analysis_data['project_id'] = ""
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
            genomic_data = {"gene_symbol": data['gene'], "gene": data['gene'], "annotations": []}
        else:
            warnings.warn("Invalid data format for import_genomic_unit_collection_data method", UserWarning)
            return None
        return genomic_data

    def import_analysis_data(self, phenotips_json_data, phenotips_variants, phenotips_genes):
        """Formats the analysis data from the phenotips.json file"""

        analysis_data = {
            "name": str(phenotips_json_data["external_id"]).replace("-", ""), "description": "", "nominated_by": "",
            "genomic_units": [], "sections": [{
                "header": 'Brief', "content": [
                    {"type": "section-text", "field": 'Nominator', "value": []},
                    {"type": "section-text", "field": 'Participant', "value": []},
                    {"type": "section-text", "field": 'Phenotype', "value": []},
                    {"type": "section-text", "field": 'ACMG Classification', "value": []},
                    {"type": "section-text", "field": 'ACMG Classification Criteria', "value": []},
                    {"type": "section-text", "field": 'ACMG Criteria To Add', "value": []},
                    {"type": "section-text", "field": 'Decision', "value": []},
                ]
            }, {
                "header": 'Clinical History', "content": [
                    {"type": "section-text", "field": 'Clinical Diagnosis', "value": []},
                    {"type": "section-text", "field": 'Affected Individuals Identified', "value": []},
                    {"type": "section-text", "field": 'Sequencing', "value": []},
                    {"type": "section-text", "field": 'Testing', "value": []},
                    {"type": "section-text", "field": 'Systems', "value": []},
                    {"type": "section-text", "field": 'Additional Details', "value": []},
                ]
            }, {
                "header": 'Pedigree', "attachment_field": "Pedigree",
                "content": [{"type": "images-dataset", "field": "Pedigree", "value": []}]
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
                        "c_dot": phenotips_variant["cdna"], "p_dot": phenotips_variant["protein"],
                        "build": str(phenotips_variant['reference_genome']),
                        "case": self.format_case_data(phenotips_variant)
                    })

                if 'transcript' in phenotips_variant:
                    new_transcript = {'transcript': phenotips_variant['transcript']}
                    if new_transcript not in analysis_unit['transcripts']:
                        analysis_unit['transcripts'].append(new_transcript)

            analysis_data['genomic_units'].append(analysis_unit)

        for genomic_unit in analysis_data['genomic_units']:
            if genomic_unit['gene']:
                new_sections = [{
                    "header": str(genomic_unit["gene"] + " Gene To Phenotype"),
                    "attachment_field": str(genomic_unit["gene"] + " Gene To Phenotype"), "content": [
                        {
                            "type": "images-dataset", "field": str(genomic_unit["gene"] + " Gene To Phenotype"),
                            "value": []
                        },
                        {
                            "type": "section-text", "field": 'HPO Terms',
                            "value": [self.extract_hpo_terms(phenotips_json_data["features"])]
                        },
                    ]
                }, {
                    "header": str(genomic_unit["gene"] + " Molecular Mechanism"), "content": [{
                        "type": "section-text", "field": str(genomic_unit["gene"] + " Molecular Mechanism"), "value": []
                    }]
                }, {
                    "header": str(genomic_unit["gene"] + " Function"),
                    "attachment_field": str(genomic_unit["gene"] + " Function"), "content": [
                        {"type": "images-dataset", "field": str(genomic_unit["gene"] + " Function"), "value": []},
                    ]
                }]
                analysis_data['sections'].extend(new_sections)

        model_goals_section = {
            "header": 'Model Goals', "content": [
                {"type": "section-text", "field": 'Model of Interest', "value": []},
                {"type": "section-text", "field": 'Goals', "value": []},
                {"type": "section-text", "field": 'Proposed Model/Project', "value": []},
                {"type": "section-text", "field": 'Existing Collaborations', "value": []},
                {"type": "section-text", "field": 'Existing Funding', "value": []},
            ]
        }
        analysis_data['sections'].append(model_goals_section)

        return analysis_data

    @staticmethod
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
                case_data.append({
                    "field": case_annotation,
                    "value": [str(variant_data[phenotips_json_attribute])],
                })
        return case_data

    @staticmethod
    def extract_hpo_terms(phenotips_json_features):
        """Extracts the HPO terms from the Phenotips JSON 'features' list and returns it as a string"""
        return '; '.join([f"{term['id']}: {term['label']}" for term in phenotips_json_features]).replace('\n', '')
