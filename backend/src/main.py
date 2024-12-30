"""
End points for backend
"""
import logging
import logging.config
from os import path
import urllib3

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .config import get_settings
from .routers import analysis_router, annotation_router, auth_router

urllib3.disable_warnings()

DESCRIPTION = """
rosalution REST API assists researchers study 🧬 variation in patients 🧑🏾‍🤝‍🧑🏼
by helping select candidate animal models 🐀🐁🐠🪱 to replicate the variation
to further research to dervice a diagnose and provide therapies for
ultra-rare diseases.
"""

tags_metadata = [
    {
        "name": "analysis",
        "description": "Analyses of cases with information such as target gene, variation, phenotyping, and more.",
    },
    {
        "name": "analysis sections",
        "description": "Adds, updates, and removes content from an Analysis Section's fields within an analysis.",
    },
    {
        "name": "analysis discussions",
        "description": "Adds, updates, and removes discussion messages from an Analysis.",
    },
    {
        "name": "analysis attachments",
        "description": "Adds, updates, and removes attachments from an Analysis.",
    },
    {
        "name": "annotation",
        "description":
            ("Temporary endpoint to facilitate annotating an analysis from a default annotation configuration"),
    },
    {
        "name": "lifecycle",
        "description": "Heart-beat that external services use to verify if the application is running.",
    },
    {
        "name": "auth",
        "description": "Handles user authentication",
    },
]

## CORS Policy ##
settings = get_settings()
origins = [settings.origin_domain_url, settings.cas_server_url]

log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

# create logger
logger = logging.getLogger(__name__)

app = FastAPI(title="rosalution API", description=DESCRIPTION, openapi_tags=tags_metadata, root_path="/rosalution/api/")

app.include_router(analysis_router.router)
app.include_router(annotation_router.router)
app.include_router(auth_router.router)

if __debug__:
    from .routers import dev_router
    app.include_router(dev_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/render-layout/annotations", tags=["config"])
def get_config():
    return [{
        "type": "section", "class": "", "header": "gene", "anchor": "Gene", "header_datasets": [{
            "dataset": "ClinGen_gene_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "logo-clin-gen.svg", "altText": "Clinical Genomic Resource Gene Linkout"}
        }, {
            "dataset": "NCBI_gene_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "ncbi-logo.png",
                "altText": "National Center for Biotechnology Information Gene Linkout"
            }
        }, {
            "dataset": "COSMIC_gene_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "cosmic_logo.png", "altText": "Catalogue Of Somatic Mutations In Cancer, COSMIC"
            }
        }, {
            "dataset": "gnomAD_gene_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "gnomad-logo.png",
                "altText": "Genome Aggregation Database (gnomAD) for variants from Broad Institute"
            }
        }], "rows": [{"class": "", "datasets": [{"dataset": "Gene Summary", "type": "text-dataset", "props": {}}]}, {
            "class": "", "datasets": [{
                "dataset": "OMIM", "type": "text-dataset", "linkout_dataset": "OMIM_gene_search_url",
                "props": {"label": "OMIM"}
            }]
        }, {
            "class": "", "datasets": [{
                "dataset": "HPO", "type": "tag-dataset", "linkout_dataset": "HPO_gene_search_url",
                "props": {"label": "HPO"}
            }]
        }]
    }, {
        "type": "section", "class": "", "header": "variant", "anchor": "Variant", "header_datasets": [{
            "dataset": "gnomAD_variant_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "gnomad-logo.png",
                "altText": "Genome Aggregation Database (gnomAD) for genes from Broad Institute"
            }
        }], "rows": [{
            "class": "fill-horizontal", "datasets": [{
                "dataset": "CADD", "type": "score-dataset", "props": {
                    "label": "CADD", "minimum": 0, "maximum": 99, "bounds": {"lowerBound": 9, "upperBound": 19},
                    "cutoff": 1
                }
            }, {
                "dataset": "DITTO", "type": "score-dataset", "props": {
                    "label": "DITTO", "minimum": 0, "maximum": 1, "bounds": {"lowerBound": 0.5, "upperBound": 0.79},
                    "cutoff": 1
                }
            }, {
                "dataset": "REVEL", "type": "score-dataset", "props": {
                    "label": "REVEL", "minimum": 0, "maximum": 1, "bounds": {"lowerBound": 0.5, "upperBound": 0.79},
                    "cutoff": 1
                }
            }, {
                "dataset": "alphamissense_pathogenicity", "type": "score-dataset", "props": {
                    "label": "AlphaMissense Score", "minimum": 0, "maximum": 1,
                    "bounds": {"lowerBound": 0.34, "upperBound": 0.564}, "cutoff": 1
                }
            }, {
                "dataset": "alphamissense_classification", "type": "set-dataset", "props": {
                    "label": "AlphaMissense Pathogenicity",
                    "set": [{"value": "likely_benign", "classification": "Likely Benign", "colour": "Blue"},
                            {"value": "ambiguous", "classification": "Ambiguous", "colour": "Yellow"},
                            {"value": "likely_pathogenic", "classification": "Likely Pathogenic", "colour": "Red"}]
                }
            }]
        }, {
            "datasets": [{
                "dataset": "ClinVar", "type": "clinvar-dataset", "linkout_dataset": "ClinVar_variant_url",
                "props": {"label": "ClinVar"}
            }]
        }, {"datasets": [{"dataset": "transcripts", "genomicType": "hgvs_variant", "type": "transcript-datasets"}]}]
    }, {
        "type": "section", "class": "", "header": "Chromosomal Localization", "anchor": "Chromosomal_Localization",
        "header_datasets": [],
        "props": {"attachmentDataset": "Chromosomal_Localization", "genomicAttachmentType": "hgvs_variant"}, "rows": [{
            "class": "", "datasets": [{
                "dataset": "Chromosomal_Localization", "genomicType": "hgvs_variant", "type": "images-dataset"
            }]
        }]
    }, {
        "type": "section", "class": "", "header": "Secondary Structure", "anchor": "Secondary_Structure",
        "header_datasets": [],
        "props": {"attachmentDataset": "Secondary_Structure", "genomicAttachmentType": "hgvs_variant"}, "rows": [{
            "class": "",
            "datasets": [{"dataset": "Secondary_Structure", "genomicType": "hgvs_variant", "type": "images-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Causal Variant In This Locus (ClinVar)", "anchor": "Causal_Variant",
        "header_datasets": [],
        "props": {"attachmentDataset": "Causal_Variant_In_This_Locus_ClinVar",
                  "genomicAttachmentType": "hgvs_variant"}, "rows": [{
                      "class": "", "datasets": [{
                          "dataset": "Causal_Variant_In_This_Locus_ClinVar", "genomicType": "hgvs_variant",
                          "type": "images-dataset"
                      }]
                  }]
    }, {
        "type": "section", "class": "", "header": "Variant Publications", "anchor": "Variant_Publications",
        "header_datasets": [],
        "props": {"attachmentDataset": "Variant_Publications", "genomicAttachmentType": "hgvs_variant"}, "rows": [{
            "class": "",
            "datasets": [{"dataset": "Variant_Publications", "genomicType": "hgvs_variant", "type": "images-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Gene Homology/Multi-Sequence Alignment", "anchor": "Gene_Homology",
        "header_datasets": [],
        "props": {"attachmentDataset": "GeneHomology_Multi-SequenceAlignment",
                  "genomicAttachmentType": "hgvs_variant"}, "rows": [{
                      "class": "", "datasets": [{
                          "dataset": "GeneHomology_Multi-SequenceAlignment", "genomicType": "hgvs_variant",
                          "type": "images-dataset"
                      }]
                  }]
    }, {
        "type": "section", "class": "", "header": "Human Gene Expression", "anchor": "Human_Gene_Expression",
        "header_datasets": [{
            "dataset": "GTEx_Human_Gene_Expression_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "gtex_logo.png", "altText": "GTEx Human Gene Expression URL"}
        }], "props": {"attachmentDataset": "Human_Gene_Expression", "genomicAttachmentType": "gene"}, "rows": [{
            "class": "",
            "datasets": [{"dataset": "Human_Gene_Expression", "genomicType": "gene", "type": "images-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Human Gene versus Protein Expression Profile",
        "anchor": "Human_Gene_versus_Protein_Expression", "header_datasets": [{
            "dataset": "Human_Protein_Atlas_Protein_Gene_Search_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "protein_atlas_icon.png", "altText": "Protein Atlas Gene Search URL"}
        }],
        "props": {"attachmentDataset": "Human_Gene_versus_Protein_Expression_Profile",
                  "genomicAttachmentType": "gene"}, "rows": [{
                      "class": "", "datasets": [{
                          "dataset": "Human_Gene_versus_Protein_Expression_Profile", "genomicType": "gene",
                          "type": "images-dataset"
                      }]
                  }]
    }, {
        "type": "section", "class": "", "header": "Model System Expression Profiles", "anchor": "Expression_Profiles",
        "header_datasets": [{
            "dataset": "CoSIA_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "CoSIA_logo.png", "altText": "COSIA_LINKOUT",
                "value": "https://lasseignelab.shinyapps.io/CoSIA/"
            }
        }, {
            "dataset": "Frog_General_Xenbase_Database_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "xenbase_logo.png", "altText": "Xenbase Xenopus General Gene Linkout"}
        }], "props": {"attachmentDataset": "Model_System_Expression_Profiles", "genomicAttachmentType": "gene"},
        "rows": [{
            "class": "", "datasets": [{
                "dataset": "Model_System_Expression_Profiles", "genomicType": "gene", "type": "images-dataset"
            }]
        }]
    }, {
        "type": "section", "class": "", "header": "Orthology", "anchor": "Orthology", "header_datasets": [{
            "dataset": "Human_Alliance_Genome_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "alliance-genome-logo.png", "altText": "Human Alliance Genome Linkout"}
        }], "props": {"attachmentDataset": "Orthology", "genomicAttachmentType": "gene"},
        "rows": [{"class": "", "datasets": [{"dataset": "Orthology", "genomicType": "gene", "type": "images-dataset"}]}]
    }, {
        "type": "section", "class": "", "header": "Rattus norvegicus (Rat) Model System",
        "anchor": "Rattus_norvegicus_Model_System", "header_datasets": [{
            "dataset": "Rat_Alliance_Genome_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "alliance-genome-logo.png", "altText": "Alliance Genome Linkout"}
        }, {
            "dataset": "Rat_Rat_Genome_Database_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "rat-dataset-logo.png", "altText": "Rat Genome Database Linkout"}
        }], "rows": [{
            "class": "", "datasets": [{
                "dataset": "Rat_Alliance_Genome_Automated_Summary", "type": "text-dataset",
                "props": {"label": "AG Summary"}
            }, {
                "dataset": "Rat_Alliance_Genome_RGD_Summary", "type": "text-dataset", "props": {"label": "RGD Summary"}
            }, {"dataset": "Rat_Alliance_Genome_Models", "type": "card-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Mus musculus (Mouse) Model System",
        "anchor": "Mus_musculus_Model_System", "header_datasets": [{
            "dataset": "Mouse_Alliance_Genome_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "alliance-genome-logo.png", "altText": "Alliance Genome Linkout"}
        }, {
            "dataset": "Mouse_Mouse_Genome_Database_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "mouse-dataset-logo.png", "altText": "Mouse Genome Informatics Linkout"}
        }], "rows": [{
            "class": "", "datasets": [{
                "dataset": "Mouse_Alliance_Genome_Automated_Summary", "type": "text-dataset",
                "props": {"label": "AG Summary"}
            }, {
                "dataset": "Mouse_Alliance_Genome_MGI_Summary", "type": "text-dataset",
                "props": {"label": "MGI Summary"}
            }, {"dataset": "Mouse_Alliance_Genome_Models", "type": "card-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Danio rerio (Zebrafish) Model System",
        "anchor": "Danio_rerio_Model_System", "header_datasets": [{
            "dataset": "Zebrafish_Alliance_Genome_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "alliance-genome-logo.png", "altText": "Alliance Genome Linkout"}
        }, {
            "dataset": "Zebrafish_Zebrafish_Information_Network_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "zebrafish-dataset-logo.png", "altText": "Zebrafish Information Network Linkout"
            }
        }], "rows": [{
            "class": "", "datasets": [{
                "dataset": "Zebrafish_Alliance_Genome_Automated_Summary", "type": "text-dataset",
                "props": {"label": "AG Summary"}
            }, {
                "dataset": "Zebrafish_Alliance_Genome_ZFIN_Summary", "type": "text-dataset",
                "props": {"label": "ZFIN Summary"}
            }, {"dataset": "Zebrafish_Alliance_Genome_Models", "type": "card-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "C. elegans (Roundworm) Model System",
        "anchor": "C_elegans_Model_System", "header_datasets": [{
            "dataset": "C-Elegens_Alliance_Genome_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "alliance-genome-logo.png", "altText": "Alliance Genome Linkout"}
        }, {
            "dataset": "C-Elegens_Worm_Base_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "c-elegens-dataset-logo.png", "altText": "WormBase Linkout"}
        }], "rows": [{
            "class": "", "datasets": [{
                "dataset": "C-Elegens_Alliance_Genome_Automated_Summary", "type": "text-dataset",
                "props": {"label": "AG Summary"}
            }, {
                "dataset": "C-Elegens_Alliance_Genome_WB_Summary", "type": "text-dataset",
                "props": {"label": "WB Summary"}
            }, {"dataset": "C-Elegens_Alliance_Genome_Models", "type": "card-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Modelability", "anchor": "Modelability", "header_datasets": [{
            "dataset": "Gentar_url", "type": "icon-linkout-dataset", "props": {
                "imageFilename": "gentar_logo.png", "altText": "Gentar URL for Modelability",
                "value": "https://www.gentar.org/"
            }
        }], "props": {"attachmentDataset": "Modelability", "genomicAttachmentType": "gene"}, "rows": [{
            "class": "", "datasets": [{"dataset": "Modelability", "genomicType": "gene", "type": "images-dataset"}]
        }]
    }, {
        "type": "section", "class": "", "header": "Druggability", "anchor": "Druggability", "header_datasets": [{
            "dataset": "Pharos_Target_url", "type": "icon-linkout-dataset",
            "props": {"imageFilename": "pharos_logo.png", "altText": "Druggability Target in Pharos"}
        }], "props": {"attachmentDataset": "Druggability", "genomicAttachmentType": "gene"}, "rows": [{
            "class": "", "datasets": [{"dataset": "Druggability", "genomicType": "gene", "type": "images-dataset"}]
        }]
    }]


@app.get("/heart-beat", tags=["lifecycle"])
def heartbeat():
    """Returns a heart-beat that orchestration services can use to determine if the application is running"""

    return "thump-thump"
