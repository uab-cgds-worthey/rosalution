from pymongo import ReturnDocument


class AnnotationUnitTranscriptQuery():

    def __init__(self, annotation_unit):
        self.annotation_unit = annotation_unit

    @property
    def dataset_name(self):
        return self.annotation_unit.get_dataset_name()

    @property
    def genomic_unit_type_string(self):
        return self.annotation_unit.get_genomic_unit_type_string()

    @property
    def genomic_unit_name(self):
        return self.annotation_unit.get_genomic_unit()

    @property
    def annotation_dataset_field_name(self):
        return f"transcripts.annotations.{self.dataset_name}"

    @property
    def annotations_add_dataset_field_name(self):
        return f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}"

    def find_genomic_unit_query(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        return {self.genomic_unit_type_string: self.genomic_unit_name}

    def find_dataset_query(self):
        genomic_unit_query = self.find_genomic_unit_query()

        data_set_name = self.annotation_unit.get_dataset_name()
        dataset_property = f"annotations.{data_set_name}"
        genomic_unit_query[dataset_property] = {'$exists': True}

    def find_annotation_query(self, transcript_id):
        """
            find_query = {
              "hgvs_variant": "NM_001017980.3:c.164G>T"
                "transcripts.transcript_id": "NM_001017980.4",
                "transcripts.annotations.SIFT Score": {$exists: true},
                "transcripts.annotations.SIFT Score.data_source": "Ensembl",
                "transcripts.annotations.SIFT Score.version": 113,
            }
        """

        data_source_field = f"{self.annotation_dataset_field_name}.data_source"
        version_field = f"{self.annotation_dataset_field_name}.version"

        find_query = {
            self.genomic_unit_type_string: self.genomic_unit_name, "transcripts.transcript_id": transcript_id,
            self.annotation_dataset_field_name: {'$exists': True},
            data_source_field: self.annotation_unit.get_dataset_source(),
            version_field: self.annotation_unit.get_version()
        }

        return find_query

    def find_annotation_value_projection(self):
        return {f"annotations.{self.annotation_unit.get_dataset_name()}.$": 1, "_id": 0}


class GenomicUnitTranscriptQuery():

    def __init__(self, genomic_unit, genomic_annotation):
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation
        self.dataset_name = self.genomic_annotation['data_set']

    @property
    def annotations_dataset_field_name(self):
        return f"annotations.{self.dataset_name}"

    @property
    def annotations_add_dataset_field_name(self):
        return f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}"

    def provision_dataset_query_and_update(self):
        """
            # find_query = {
            #   'gene': 'VMA21',
            #}
        """
        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'], "transcripts.transcript_id": {'$exists': True},
            self.annotations_add_dataset_field_name: {'$exists': False}
        }

        update_operation = {'$addToSet': {"transcripts.$[transcript].annotations": {self.dataset_name: []}}}

        arrays_filter = [
            {"transcript.transcript_id": self.genomic_annotation['transcript_id']},
        ]

        return query_filter, update_operation, arrays_filter

    def annotate_dataset_query_and_update(self):

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            "transcripts.transcript_id": self.genomic_annotation['transcript_id']
        }

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        update_operation = {'$addToSet': {self.annotations_add_dataset_field_name: annotation_entry}}

        arrays_filter = [{"transcript.transcript_id": self.genomic_annotation['transcript_id']},
                         {f"dataset.{self.dataset_name}": {'$exists': True}}]

        return query_filter, update_operation, arrays_filter


class GenomicUnitCollectionForTranscripts():

    def __init__(self, genomic_unit_collection):
        self.collection = genomic_unit_collection

    def annotation_exist(self, annotation_unit):
        annotation_query_adapter = AnnotationUnitTranscriptQuery(annotation_unit)

        find_query = annotation_query_adapter.find_genomic_unit_query()
        hgvs_genomic_unit_json = self.collection.find_one(find_query)

        if 'transcripts' not in hgvs_genomic_unit_json or len(hgvs_genomic_unit_json['transcripts']) == 0:
            return False

        for transcript in hgvs_genomic_unit_json['transcripts']:
            find_transcript_query = annotation_query_adapter.find_annotation_query(transcript['transcript_id'])

            if not bool(self.collection.count_documents(find_transcript_query, limit=1)):
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

        result = self.collection.find_one_and_update(query, operation, return_document=ReturnDocument.AFTER)

        return result

    def annotate_transcript_dataset(self, genomic_unit, genomic_annotation):
        transcript_query = GenomicUnitTranscriptQuery(genomic_unit, genomic_annotation)

        provision_dataset, update_operation, array_filters = transcript_query.provision_dataset_query_and_update()
        genomic_unit = self.collection.update_one(provision_dataset, update_operation, array_filters=array_filters)

        add_annotation_query, add_annotation_update_operation, add_annotation_array_filters = \
            transcript_query.annotate_dataset_query_and_update()
        result = self.collection.update_one(
            add_annotation_query, add_annotation_update_operation, array_filters=add_annotation_array_filters
        )

        return result
