"""
Module for adapting the GenomicUnitCollection to streamline support for Transcripts as a genomic unit
within MongoDB.
"""
from ..core.annotation_unit import AnnotationUnit


class AnnotationUnitTranscriptQuery():
    """
    Represents the MongoDB query's filter and update arguments for transcripts of an AnnotationUnit.
    """

    def __init__(self, annotation_unit: AnnotationUnit):
        """Initializes this query builder with an AnnotationUnit"""
        self.annotation_unit = annotation_unit

    @property
    def dataset_name(self):
        """Name of the dataset for the annotation."""
        return self.annotation_unit.get_dataset_name()

    @property
    def genomic_unit_type_string(self):
        """The type of genomic unit as a string for the annotation."""
        return self.annotation_unit.get_genomic_unit_type_string()

    @property
    def genomic_unit_name(self):
        """The name of the genomic unit for the annotation."""
        return self.annotation_unit.get_genomic_unit()

    def find_genomic_unit_query(self):
        """
        Constructs the find filter to query MongoDB for the genomic unit for this annotation.
        """
        return {self.genomic_unit_type_string: self.genomic_unit_name}

    def find_annotation_query(self, transcript_id):
        """
        Constructs the find filter to query MongoDB for the annotation unit for by its genomic unit name, transcript_id,
        dataset, data source, and calculated version.

        ex.
        find_query = {
            "hgvs_variant": "NM_001017980.3:c.164G>T"
            "transcripts.transcript_id": "NM_001017980.4",
            "transcripts.annotations.SIFT Score": {$exists: true},
            "transcripts.annotations.SIFT Score.data_source": "Ensembl",
            "transcripts.annotations.SIFT Score.version": 113,
        }
        """
        find_query = {
            self.genomic_unit_type_string: self.genomic_unit_name, "transcripts.transcript_id": transcript_id,
            f"transcripts.annotations.{self.dataset_name}": {'$exists': True},
            f"transcripts.annotations.{self.dataset_name}.data_source": self.annotation_unit.get_dataset_source(),
            f"transcripts.annotations.{self.dataset_name}.version": self.annotation_unit.version
        }

        return find_query


class GenomicUnitTranscriptQuery():
    """
    Represents the MongoDB query's filter, update, and arraysFilter arguments for transcripts of a genomic unit
    an its annotation.
    """

    def __init__(self, genomic_unit, genomic_annotation):
        """Initializes this query builder with the genomic unit and the gathered annotation for transcripts."""
        self.genomic_unit = genomic_unit
        self.genomic_annotation = genomic_annotation
        self.dataset_name = self.genomic_annotation['data_set']

    def provision_transcript_id(self):
        """Constructs a query and update operation to provision a transcript ID in a unit's transcripts list'"""
        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            "transcripts.transcript_id": {'$ne': self.genomic_annotation['transcript_id']},
        }

        update_operation = {
            '$addToSet': {
                'transcripts': {'transcript_id': self.genomic_annotation['transcript_id'], 'annotations': []}
            }
        }

        return query_filter, update_operation

    def provision_dataset_query_and_update(self):
        """Constructs a query, update, and arraysFilter MongoDB arguments to provision a dataset for a transcript id."""

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'], "transcripts.transcript_id": {'$exists': True},
            f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}": {'$exists': False}
        }

        update_operation = {'$addToSet': {"transcripts.$[transcript].annotations": {self.dataset_name: []}}}

        arrays_filter = [
            {"transcript.transcript_id": self.genomic_annotation['transcript_id']},
        ]

        return query_filter, update_operation, arrays_filter

    def annotate_dataset_query_and_update(self):
        """Constructs a query, update, and arraysFilter MongoDB arguments for annotating a transcript dataset."""

        query_filter = {
            self.genomic_unit['type'].value: self.genomic_unit['unit'],
            "transcripts.transcript_id": self.genomic_annotation['transcript_id']
        }

        annotation_entry = {
            'data_source': self.genomic_annotation['data_source'],
            'version': self.genomic_annotation['version'],
            'value': self.genomic_annotation['value'],
        }

        update_operation = {
            '$addToSet': {f"transcripts.$[transcript].annotations.$[dataset].{self.dataset_name}": annotation_entry}
        }

        arrays_filter = [{"transcript.transcript_id": self.genomic_annotation['transcript_id']},
                         {f"dataset.{self.dataset_name}": {'$exists': True}}]

        return query_filter, update_operation, arrays_filter


class GenomicUnitCollectionForTranscripts():
    """
    Repository adapter for the genomic unit collection for managing Transcripts for a given HGVS variant genomic unit.
    """

    def __init__(self, genomic_unit_collection):
        """Initializes the this repository adapter with the GenomicUnitCollection it is adapting."""
        self.collection = genomic_unit_collection.collection

    def annotation_exist(self, annotation_unit: AnnotationUnit):
        """
        Returns True if the annotation exists by transcript_id, dataset, data source, and version of an AnnotationUnit,
        otherwise returns False.
        """
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

    def annotate_transcript_dataset(self, genomic_unit, genomic_annotation):
        """
        Annotates a dataset in a transcript for a genomic unit. It will provision a transcript and dataset for a
        transcript if it does not exist.
        """
        transcript_query = GenomicUnitTranscriptQuery(genomic_unit, genomic_annotation)

        provision_transcript, provision_transcript_update = transcript_query.provision_transcript_id()
        genomic_unit = self.collection.update_one(provision_transcript, provision_transcript_update)

        provision_dataset, update_operation, array_filters = transcript_query.provision_dataset_query_and_update()
        genomic_unit = self.collection.update_one(provision_dataset, update_operation, array_filters=array_filters)

        add_annotation_query, add_annotation_update_operation, add_annotation_array_filters = \
            transcript_query.annotate_dataset_query_and_update()

        result = self.collection.update_one(
            add_annotation_query, add_annotation_update_operation, array_filters=add_annotation_array_filters
        )

        return result
