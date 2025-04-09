
from pymongo import ReturnDocument
from .genomic_unit_collection import GenomicUnitCollection, AnnotationUnitQuery

def transcript_unit_exist(dataset, data_source, version, annotation):
    """Helper method to evaluate if transcript annotations have existing annotation"""
    # if( dataset == 'transcript_id' ):
    #     logger.warning('looking to find transcript ID exists in list!!!')
    #     logger.warning((dataset, data_source, version, annotation))
    #     logger.warning("-------------------------------------------------")
    if dataset not in annotation:
        return False
    

    annotation_unit_match = next(
        (unit for unit in annotation[dataset] if unit['data_source'] == data_source and unit['version'] == version),
        None
    )

    # if( dataset == 'transcript_id' ):
    #     logger.warning('MASTCH RESULT: %s', dataset)
    #     logger.warning(annotation_unit_match)
    #     logger.warning('what did it find')

    return annotation_unit_match is not None

class GenomicUnitCollectionForTranscripts():
    def __init__(self, genomic_unit_collection: GenomicUnitCollection):
        self.collection = genomic_unit_collection.collection

    def annotation_exist(self, annotation_unit):
        annotation_query_adapter = AnnotationUnitQuery(annotation_unit)

        find_query = annotation_query_adapter.find_genomic_unit_query()
        hgvs_genomic_unit_json = self.collection.find_one(find_query)

        if 'transcripts' not in hgvs_genomic_unit_json or len(hgvs_genomic_unit_json['transcripts']) == 0:
            return False

        data_set_name = annotation_unit.get_dataset_name()
        dataset_version = annotation_unit.get_version()
        dataset_source = annotation_unit.get_dataset_source()

        for transcript in hgvs_genomic_unit_json['transcripts']:
            # if( "NM_001365.4:c.1039del" in annotation_unit.to_name_string() ):
            #     logger.warning("LOOKING AT THE FOLLOWING TRANSCRIPT TO FIND: %s", transcript)
            #     logger.warning(transcript['annotations'])
            #     logger.warning(annotation_unit.to_name_string())
            #     logger.warning(data_set_name)
            dataset_in_transcript_annotation = next((
                annotation for annotation in transcript['annotations']
                if transcript_unit_exist(data_set_name, dataset_source, dataset_version, annotation)
            ), None)

            if not dataset_in_transcript_annotation:
                return False

        return True

    def find_genomic_unit_with_transcript_id(self, genomic_unit, transcript_id):
        """ Returns the genomic unit with the corresponding transcript if it exists """

        query = {
            genomic_unit['type'].value: genomic_unit['unit'],
            'transcripts.transcript_id': transcript_id,
        }
        result = self.collection.find_one(query)
        return result
    
    def add_transcript_to_genomic_unit(self, genomic_unit, transcript_id):
        """ Takes a genomic unit and transcript id and updates the document with a new transcript """
        query = {genomic_unit['type'].value: genomic_unit['unit']}
        operation = {'$addToSet': {'transcripts': {'transcript_id': transcript_id, 'annotations': []}}}

        result = self.collection.find_one_and_update(
            query,
            operation,
            return_document=ReturnDocument.AFTER
        )

        return result
    
    def annotate_transcript_dataset(self, genomic_unit, genomic_annotation):
            transcript_id = genomic_annotation['transcript_id']
            updated_document = self.__annotate_transcript_dataset(genomic_unit, transcript_id, genomic_annotation)
            return updated_document

    def __annotate_transcript_dataset(self, genomic_unit, transcript_id: str, genomic_annotation):
        dataset_name = genomic_annotation['data_set']

        genomic_unit_document = self.find_genomic_unit_with_transcript_id(genomic_unit, transcript_id)

        if not genomic_unit_document:
            # logger.warning('------- DID IT NOT EXIST?! thats ok, lets make it')
            # logger.warning(genomic_unit_document)
            genomic_unit_document = self.add_transcript_to_genomic_unit(genomic_unit, transcript_id)
            # genomic_unit_document = self.find_genomic_unit_with_transcript_id(genomic_unit, transcript_id)
            # if( not genomic_unit_document or isinstance(genomic_unit_document, NoneType) ):
            #     logger.warning('transcript did not work - fail whale')
            # logger.warning("ABOVE RESULT IS AFTER THE RE_QUERYING OF IT")

        # logger.warning(genomic_unit_document)
        for transcript in genomic_unit_document['transcripts']:
            if transcript["transcript_id"] == transcript_id:
                self.__add_to_annotations_from_document(transcript['annotations'], dataset_name, genomic_annotation)

        return self.update_genomic_unit_by_mongo_id(genomic_unit_document)