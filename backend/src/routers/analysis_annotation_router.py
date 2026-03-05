""" Analysis endpoint routes that provide an interface to interact with an Analysis' discussions """
from fastapi import (APIRouter, Depends, HTTPException, Security)

from ..security.security import get_project_authorization

from ..dependencies import database
from ..enums import GenomicUnitType

router = APIRouter(tags=["analysis annotations"])


@router.get("/{analysis_name}/gene/{gene}", dependencies=[Security(get_project_authorization)])
def get_annotations_by_gene(analysis_name, gene, repositories=Depends(database)):
    """Returns annotations data by calling method to find annotations by gene"""

    genomic_unit = {
        'type': GenomicUnitType.GENE,
        'unit': gene,
    }

    dataset_manifest = repositories["analysis"].get_dataset_manifest(analysis_name)
    genomic_unit_json = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if genomic_unit_json is None:
        raise HTTPException(status_code=404, detail=f"Gene'{gene}' annotations not found.")

    manifest = AnalysisDatasetManfiest(dataset_manifest)
    annotations = manifest.retrieve_annotations(gene, genomic_unit_json['annotations'])

    return annotations


@router.get("/{analysis_name}/hgvsVariant/{variant}", dependencies=[Security(get_project_authorization)])
def get_annotations_by_hgvs_variant(analysis_name: str, variant: str, repositories=Depends(database)):
    """Returns annotations data by calling method to find annotations for variant and relevant transcripts
    by HGVS Variant"""

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': variant,
    }

    dataset_manifest = repositories["analysis"].get_dataset_manifest(analysis_name)
    genomic_unit_json = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if genomic_unit_json is None:
        raise HTTPException(status_code=404, detail=f"Variant'{variant}' annotations not found.")

    manifest = AnalysisDatasetManfiest(dataset_manifest)
    annotations = manifest.retrieve_annotations(variant, genomic_unit_json['annotations'])

    transcript_annotation_list = []
    for transcript_annotation in genomic_unit_json['transcripts']:
        transcript_annotations = manifest.retrieve_annotations(variant, transcript_annotation['annotations'])
        transcript_annotation_list.append(transcript_annotations)

    return {**annotations, "transcripts": transcript_annotation_list}


class AnalysisDatasetManfiest():
    """ 
    Retrieves dataset annotations based on an analysis' manifest.
    
    An analysis' manifest comprises of entries for each dataset in the following
    example:
    {
        'CADD': {
            data_source: 'Ensembl',
            version: '120'
        }
    }
    """

    def __init__(self, analysis_dataset_manifest):
        """
        Initializes with a list of analysis' dataset manifest entries.
        """
        self.manifest = analysis_dataset_manifest

    def retrieve_annotations(self, omic_unit: str, unit_annotations):
        """
        Extracts annotations from the provided list of unit annotations and returns a dictionary
        of datasets and their corresponding values.

        unit_annotations is a list of annotations for a genomic unit, where each annotation is structured as the
        following example

        {
            'CADD': [{
                'data_source': 'Ensembl',
                'version': '112',
            }]
        }
        """
        annotations = {}
        for annotation_json in unit_annotations:
            for dataset in annotation_json:
                if len(annotation_json[dataset]) > 0:
                    analysis_dataset = self.get_value_for_dataset(dataset, omic_unit, annotation_json[dataset])
                    annotations[dataset] = analysis_dataset[
                        'value'] if analysis_dataset is not None else annotation_json[dataset][0]['value']
        return annotations

    def get_value_for_dataset(self, dataset_name: str, omic_unit: str, annotation_json_list: list):
        """
        Retrieves the annotation according to the analysis' dataset manifest entry matching the dataset's name,
        'data_source', and 'version'. None is returned when there isn't an entry in the manifest.
        """

        omic_manifest = next((manifest for manifest in self.manifest if manifest['unit'] == omic_unit), None)
        if omic_manifest is None:
            return None

        dataset_config = next(
            (configuration for configuration in omic_manifest['manifest'] if dataset_name in configuration), None
        )

        if dataset_config is None:
            return None

        configuration = dataset_config[dataset_name]

        return next((
            annotation for annotation in annotation_json_list
            if annotation['data_source'] == configuration['data_source'] and
            annotation['version'] == configuration['version']
        ), None)
