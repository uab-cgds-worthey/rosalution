"""
Collection with retrieves, creates, and modify analyses.
"""
from uuid import uuid4

from pymongo import ReturnDocument
from ..models.event import Event

from ..enums import ThirdPartyLinkType

# pylint: disable=too-few-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class


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
            "timeline": 1,
        })

        summaries = []
        for summary in query_result:
            genes_list = map(lambda unit: unit['gene'], summary['genomic_units'])
            genes_string_list = ', '.join(genes_list)

            transcripts_list = [[transcript_unit['transcript']
                                 for transcript_unit in unit['transcripts']]
                                for unit in summary['genomic_units']]
            flattened_transcripts_list = [
                transcript for transcript_items in transcripts_list for transcript in transcript_items
            ]

            variant_list = [
                f"{variant['c_dot']} ({variant['p_dot']})" for genomic_unit in summary['genomic_units']
                for variant in genomic_unit['variants'] if variant['c_dot']
            ]

            genomic_units_summary = [{
                "gene": genes_string_list, "transcripts": flattened_transcripts_list, "variants": variant_list
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
            raise ValueError(f"Analysis with name {analysis_data['name']} already exists")

        # returns an instance of InsertOneResult.
        return self.collection.insert_one(analysis_data)

    def update_analysis_nominator(self, analysis_name: str, nominator: str):
        """Updates the Nominator field within an analysis"""
        updated_analysis_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"nominated_by": nominator,}},
            return_document=ReturnDocument.AFTER,
        )
        updated_analysis_document.pop("_id", None)
        return updated_analysis_document

    def update_analysis_section(self, name: str, section_header: str, field_name: str, updated_value: dict):
        """Updates an existing analysis section by name, section header, and field name"""
        query_results_to_update = self.collection.find_one({"name": name})
        for section in query_results_to_update["sections"]:
            if section["header"] == section_header:
                for content in section["content"]:
                    if content["field"] == field_name:
                        content["value"] = updated_value["value"]
        updated_document = self.collection.find_one_and_update(
            {"name": name},
            {"$set": query_results_to_update},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def find_file_by_name(self, analysis_name: str, file_name: str):
        """ Returns an attached file metadata attached to an analysis if it exists by name """
        analysis = self.collection.find_one({"name": analysis_name})

        if not analysis:
            return None

        if 'supporting_evidence_files' not in analysis:
            return None

        for file in analysis['supporting_evidence_files']:
            if file['filename'] == file_name:
                return file

        return None

    def attach_supporting_evidence_file(self, analysis_name: str, file_id: str, filename: str, comments: str):
        """Attachs supporting evidence documents and comments for an analysis"""
        new_uuid = str(file_id)
        new_evidence = {
            "name": filename,
            "attachment_id": new_uuid,
            "type": "file",
            "comments": comments,
        }
        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$push": {"supporting_evidence_files": new_evidence}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def attach_supporting_evidence_link(self, analysis_name: str, link_name: str, link: str, comments: str):
        """Attachs supporting evidence URL and comments to an analysis"""
        new_uuid = str(uuid4())
        new_evidence = {
            "name": link_name, "data": link, "attachment_id": new_uuid, "type": "link", "comments": comments
        }
        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$push": {"supporting_evidence_files": new_evidence}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)

        return updated_document

    def add_pedigree_file(self, analysis_name: str, file_id: str):
        """ Adds a pedigree file to an analysis """
        updated_document = self.collection.find_one({"name": analysis_name})
        if "_id" in updated_document:
            updated_document.pop("_id", None)

        updated_section = None
        for section in updated_document['sections']:
            if section["header"] == "Pedigree":
                if len(section["content"]) == 0:
                    updated_section = {
                        "field": 'image',
                        "value": [str(file_id)],
                    }
                    section["content"].append(updated_section)
                else:
                    section['content'][0]['value'] = [str(file_id)]

                updated_section = section

        if None is updated_section:
            raise ValueError("No pedigree section to attach image to.")

        self.collection.find_one_and_update(
            {"name": analysis_name},
            {'$set': updated_document},
        )

        return updated_section

    def get_genomic_units(self, analysis_name: str):
        """ Returns the genomic units for an analysis with variants displayed in the HGVS Nomenclature """
        genomic_units_return = {"genes": {}, "variants": []}

        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist")

        if 'genomic_units' not in analysis:
            raise ValueError(f"Analysis {analysis_name} does not have genomic units")

        for gene in analysis['genomic_units']:
            variants = []
            for variant in gene['variants']:
                hgvs_variant = variant["hgvs_variant"]
                p_dot = variant["p_dot"]
                if all(value != "" for value in [p_dot, hgvs_variant]):
                    variants.append(f"{hgvs_variant}({p_dot})")
                elif hgvs_variant != "":
                    variants.append(hgvs_variant)
            genomic_units_return["genes"].update({gene["gene"]: variants})
            genomic_units_return["variants"].extend(variants)

        return genomic_units_return

    def update_supporting_evidence(self, analysis_name: str, attachment_id: str, updated_content: dict):
        """Updates Supporting Evidence content with by analysis and the attachment id"""
        supporting_evidence_files = self.collection.find_one({"name": analysis_name})["supporting_evidence_files"]
        index_to_update = supporting_evidence_files.index(
            next(filter(lambda x: x["attachment_id"] == attachment_id, supporting_evidence_files), None)
        )

        if None is index_to_update:
            raise ValueError(f"Supporting Evidence identifier {attachment_id} does not exist for {analysis_name}")

        supporting_evidence_files[index_to_update]['name'] = updated_content['name']
        if None is updated_content['data']:
            supporting_evidence_files[index_to_update]['data'] = updated_content['data']
        supporting_evidence_files[index_to_update]['comments'] = updated_content['comments']

        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"supporting_evidence_files": supporting_evidence_files}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def remove_supporting_evidence(self, analysis_name: str, attachment_id: str):
        """ Removes a supporting evidence file from an analysis """
        supporting_evidence_files = self.collection.find_one({"name": analysis_name})["supporting_evidence_files"]
        index_to_remove = supporting_evidence_files.index(
            next(filter(lambda x: x["attachment_id"] == attachment_id, supporting_evidence_files), None)
        )
        del supporting_evidence_files[index_to_remove]
        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"supporting_evidence_files": supporting_evidence_files}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def get_pedigree_file_id(self, analysis_name: str):
        """ Returns the pedigree file id for an analysis """
        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist")

        for section in analysis['sections']:
            if section["header"] == "Pedigree":
                if len(section["content"]) == 0:
                    raise ValueError(f"Analysis {analysis_name} does not have a pedigree file")
                return section['content'][0]['value'][0]
        raise ValueError(f"Analysis {analysis_name} does not have a pedigree section")

    def remove_pedigree_file(self, analysis_name: str):
        """ Removes a pedigree file from an analysis """
        analysis = self.collection.find_one({"name": analysis_name})
        for section in analysis["sections"]:
            if section["header"] == "Pedigree":
                section["content"] = []
        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"sections": analysis["sections"]}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def attach_third_party_link(self, analysis_name: str, third_party_enum: str, link: str):
        """ Returns an analysis with a third party link attached to it """
        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist")

        if third_party_enum == "MONDAY_COM":
            third_party_enum = ThirdPartyLinkType.MONDAY_COM
        elif third_party_enum == "PHENOTIPS_COM":
            third_party_enum = ThirdPartyLinkType.PHENOTIPS_COM
        else:
            raise ValueError(f"Third party link type {third_party_enum} is not supported")

        if third_party_enum not in analysis:
            analysis[third_party_enum] = None

        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {ThirdPartyLinkType(third_party_enum): link}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

    def mark_ready(self, analysis_name: str, username: str):
        """ Marks an analysis as ready """
        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist.")
        for event in analysis['timeline']:
            if event['event'] == 'ready':
                raise ValueError(f"Analysis {analysis_name} is already marked as ready!")
        analysis['timeline'].append(Event.timestamp_ready_event(username).dict())

        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"timeline": analysis["timeline"]}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document
