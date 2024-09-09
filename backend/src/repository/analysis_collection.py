"""
Collection with retrieves, creates, and modify analyses.
"""
from typing import List
from uuid import uuid4

from pymongo import ReturnDocument

from ..core.annotation_unit import AnnotationUnit

from ..models.analysis import Section
from ..models.event import Event
from ..enums import EventType

# pylint: disable=too-many-public-methods
# Disabling too few public metods due to utilizing Pydantic/FastAPI BaseSettings class


class AnalysisCollection:
    """Repository to access analyses for projects"""

    def __init__(self, analysis_collection):
        """Initializes with the 'PyMongo' Collection object for the analyses collection"""
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
            "third_party_links": 1,
        })

        summaries = []
        for analysis in query_result:
            genomic_unit_summaries = []
            for unit in analysis['genomic_units']:
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
            analysis['genomic_units'] = genomic_unit_summaries
            summaries.append(analysis)

        return summaries

    def summary_by_name(self, name: str):
        """Returns the summary of an analysis by name"""

        query_result = self.collection.find_one({"name": name}, {
            "name": 1,
            "description": 1,
            "genomic_units": 1,
            "nominated_by": 1,
            "timeline": 1,
            "third_party_links": 1,
        })

        if query_result:
            genomic_unit_summaries = []
            for unit in query_result['genomic_units']:
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
            query_result['genomic_units'] = genomic_unit_summaries

        return query_result

    def find_by_name(self, name: str):
        """Returns analysis by searching for name"""
        return self.collection.find_one({"name": name})

    def find_file_by_name(self, analysis_name: str, file_name: str):
        """ Returns an attached file metadata attached to an analysis if it exists by name """
        analysis = self.collection.find_one({"name": analysis_name})

        if not analysis:
            return None

        if 'supporting_evidence_files' not in analysis:
            return None

        for file in analysis['supporting_evidence_files']:
            if file['name'] == file_name:
                return file

        return None

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

    def add_dataset_to_manifest(self, analysis_name: str, annotation_unit: AnnotationUnit):
        """Adds this dataset and its version to this Analysis."""

        dataset = {
            annotation_unit.get_dataset_name(): {
                annotation_unit.get_dataset_source(),
                annotation_unit.get_version()
            }
        }
   
        updated_document = self.collection.find_one_and_update({"name": analysis_name},
                                                               {"$push": {"manifest": dataset}},
                                                               return_document=ReturnDocument.AFTER)

        return updated_document['manifest']
    
    def get_manifest_dataset_config(self, analysis_name: str, dataset_name: str):
        dataset_attribute = f"manifest.{dataset_name}"
        result = self.collection.find_one({
            "name": analysis_name,
            dataset_attribute : {'$exists': True }
        })

        if not result:
            return None
        
        return {
            "data_set": dataset_name,
            "data_source": result[dataset_name]['data_source'],
            "version": result[dataset_name]['version']
        }
    
    def get_dataset_manifest(self, analysis_name):
        analysis = self.find_by_name(analysis_name)
        if analysis is None:
            return

        return analysis['manifest']

    def create_analysis(self, analysis_data: dict):
        """Creates a new analysis if the name does not already exist"""
        if self.collection.find_one({"name": analysis_data["name"]}) is not None:
            raise ValueError(f"Analysis with name {analysis_data['name']} already exists")

        # returns an instance of InsertOneResult.
        return self.collection.insert_one(analysis_data)

    def attach_third_party_link(self, analysis_name: str, third_party_enum: str, link: str):
        """ Returns an analysis with a third party link attached to it """
        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist")

        if 'third_party_links' not in analysis:
            analysis['third_party_links'] = []

        # Check if the third_party_enum already exists in the list
        existing_link = next((item for item in analysis['third_party_links'] if item['type'] == third_party_enum), None)

        if existing_link:
            # Update the existing link
            updated_document = self.collection.find_one_and_update(
                {"name": analysis_name, "third_party_links.type": third_party_enum},
                {"$set": {"third_party_links.$.link": link}},
                return_document=ReturnDocument.AFTER,
            )
        else:
            # Add a new link to the list
            updated_document = self.collection.find_one_and_update(
                {"name": analysis_name},
                {"$push": {"third_party_links": {"type": third_party_enum, "link": link}}},
                return_document=ReturnDocument.AFTER,
            )

        # Remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)

        return updated_document

    def update_event(self, analysis_name: str, username: str, event_type: EventType):
        """ Updates analysis status """
        analysis = self.collection.find_one({"name": analysis_name})
        if not analysis:
            raise ValueError(f"Analysis with name {analysis_name} does not exist.")
        analysis['timeline'].append(Event.timestamp_event(username, event_type).model_dump())

        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"timeline": analysis["timeline"]}},
            return_document=ReturnDocument.AFTER,
        )
        # remove the _id field from the returned document since it is not JSON serializable
        updated_document.pop("_id", None)
        return updated_document

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
        self.collection.update_one({"name": name}, {"$set": query_results_to_update})

    def update_analysis_sections(self, analysis_name: str, updated_sections: List[Section]):
        """Updates each of the sections and fields within the sections if they exist in the database"""
        for section in updated_sections:
            for field in section.content:
                field_name, field_value = field["fieldName"], field["value"]
                if "Nominator" == field_name:
                    self.update_analysis_nominator(analysis_name, '; '.join(field_value))
                self.update_analysis_section(analysis_name, section.header, field_name, {"value": field_value})

    def attach_section_supporting_evidence_file(
        self, analysis_name: str, section_name: str, field_name: str, field_value_file: object
    ):
        """
        Attaches a file to a field within an analysis section and returns only the updated field within that section
        """
        updated_document = self.collection.find_one({"name": analysis_name})
        if "_id" in updated_document:
            updated_document.pop("_id", None)
        updated_section = None
        for section in updated_document['sections']:
            if section_name == section['header']:
                updated_section = section
        if None is updated_section:
            raise ValueError(
                f"'{section_name}' does not exist within '{analysis_name}'. Unable to attach report to '{section_name}'\
                section."
            )

        for field in updated_section['content']:
            if field['field'] == field_name:
                field['value'] = [field_value_file]

        self.collection.update_one({"name": analysis_name}, {'$set': updated_document})

    def attach_section_supporting_evidence_link(
        self, analysis_name: str, section_name: str, field_name: str, field_value_link: object
    ):
        """
        Attaches a link to a section field within an analysis and returns only the updated field for that section
        """
        updated_document = self.collection.find_one({"name": analysis_name})

        if "_id" in updated_document:
            updated_document.pop("_id", None)

        updated_section = None
        for section in updated_document['sections']:
            if section_name == section['header']:
                updated_section = section

        if None is updated_section:
            raise ValueError(
                f"'{section_name}' does not exist within '{analysis_name}'. Unable to attach report to '{section_name}'\
                section."
            )

        new_uuid = str(uuid4())
        field_value_link['attachment_id'] = new_uuid

        updated_field = None
        for field in updated_section['content']:
            if field['field'] == field_name:
                field['value'] = [field_value_link]
                updated_field = field

        self.collection.find_one_and_update(
            {"name": analysis_name},
            {'$set': updated_document},
            return_document=ReturnDocument.AFTER,
        )

        return_updated_field = {"header": section_name, "field": field_name, "updated_row": updated_field}

        return return_updated_field

    def add_section_image(self, analysis_name: str, section_name: str, field_name: str, file_id: str):
        """
        Adds an image to a section within an analysis specified by the the name of the section (the header) and
        """
        updated_document = self.collection.find_one({"name": analysis_name})
        if "_id" in updated_document:
            updated_document.pop("_id", None)

        updated_section = None
        for section in updated_document['sections']:
            if section_name == section['header']:
                updated_section = section

        if None is updated_section:
            raise ValueError(
                f"'{section_name}' does not exist within '{analysis_name}'. Unable to attach image to '{field_name}' \
                field in section '{section_name}"
            )

        for content_row in updated_section['content']:
            if content_row["field"] and content_row["field"] == field_name:
                content_row["value"].append({'file_id': str(file_id)})

        return self.collection.find_one_and_update({"name": analysis_name}, {'$set': updated_document},
                                                   return_document=ReturnDocument.AFTER)

    def update_section_image(
        self, analysis_name: str, section_name: str, field_name: str, file_id: str, file_id_old: str
    ):
        """ Accepts a new and old file id then updates the section image """
        updated_document = self.collection.find_one({"name": analysis_name})

        if "_id" in updated_document:
            updated_document.pop("_id", None)

        updated_section = None
        for section in updated_document['sections']:
            if section_name == section['header']:
                updated_section = section

        if None is updated_section:
            raise ValueError(
                f"'{section_name}' does not exist within '{analysis_name}'. \
                Unable to attach image to '{field_name}' field in section '{section_name}"
            )

        for content_row in updated_section['content']:
            if content_row['field'] and content_row['field'] == field_name:
                for i in range(len(content_row['value'])):
                    if content_row['value'][i]['file_id'] == file_id_old:
                        content_row['value'].pop(i)
                        content_row["value"].append({'file_id': str(file_id)})
                        break

        updated_analysis_json = self.collection.find_one_and_update({'name': analysis_name}, {'$set': updated_document},
                                                                    return_document=ReturnDocument.AFTER)

        return updated_analysis_json['sections']

    def remove_section_attachment(self, analysis_name: str, section_name: str, field_name: str, attachment_id: str):
        """ Accepts a file id and removes the reference from corresponding analysis section, returns all of the sections
         with an analysis """
        updated_document = self.collection.find_one({"name": analysis_name})

        updated_section = None
        for section in updated_document['sections']:
            if section_name == section['header']:
                updated_section = section
        if None is updated_section:
            raise ValueError(
                f"'{section_name}' does not exist within '{analysis_name}'. Unable to attach image to '{field_name}' \
                field in section '{section_name}"
            )

        def attribute_type_in_field(attribute_key, field_value):
            return attribute_key if attribute_key in field_value else ''

        for content_row in updated_section['content']:
            if content_row['field'] and content_row['field'] == field_name:
                for i in range(len(content_row['value'])):
                    content_value = content_row['value'][i]
                    for key in ['file_id', 'attachment_id']:
                        if attribute_type_in_field(key, content_value) and content_value[key] == attachment_id:
                            content_row['value'].pop(i)
                            break

        updated_analysis_json = self.collection.find_one_and_update({'name': analysis_name}, {'$set': updated_document},
                                                                    return_document=ReturnDocument.AFTER)
        return updated_analysis_json['sections']

    def add_discussion_post(self, analysis_name: str, discussion_post: object):
        """ Appends a new discussion post to an analysis """

        updated_document = self.collection.find_one_and_update({"name": analysis_name},
                                                               {"$push": {"discussions": discussion_post}},
                                                               return_document=ReturnDocument.AFTER)

        updated_document.pop("_id", None)

        return updated_document['discussions']

    def updated_discussion_post(self, discussion_post_id: str, discussion_content: str, analysis_name: str):
        """ Edits a discussion post from an analysis to update the discussion post's content """

        updated_document = self.collection.find_one_and_update({"name": analysis_name}, {
            "$set": {"discussions.$[item].content": discussion_content}
        },
                                                               array_filters=[{"item.post_id": discussion_post_id}],
                                                               return_document=ReturnDocument.AFTER)

        updated_document.pop("_id", None)

        return updated_document['discussions']

    def delete_discussion_post(self, discussion_post_id: str, analysis_name: str):
        """ Removes a discussion post from an analysis """

        updated_document = self.collection.find_one_and_update({"name": analysis_name}, {
            "$pull": {"discussions": {"post_id": discussion_post_id}}
        },
                                                               return_document=ReturnDocument.AFTER)

        updated_document.pop("_id", None)

        return updated_document['discussions']

    def attach_supporting_evidence_file(self, analysis_name: str, file_id: str, filename: str, comments: str):
        """Attaches supporting evidence documents and comments for an analysis"""
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
        return updated_document

    def attach_supporting_evidence_link(self, analysis_name: str, link_name: str, link: str, comments: str):
        """Attaches supporting evidence URL and comments to an analysis"""
        new_uuid = str(uuid4())
        new_evidence = {
            "name": link_name, "data": link, "attachment_id": new_uuid, "type": "link", "comments": comments
        }
        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$push": {"supporting_evidence_files": new_evidence}},
            return_document=ReturnDocument.AFTER,
        )

        return updated_document

    def update_supporting_evidence(self, analysis_name: str, attachment_id: str, updated_content: dict):
        """Updates Supporting Evidence content with by analysis and the attachment id"""
        supporting_evidence_files = self.collection.find_one({"name": analysis_name})["supporting_evidence_files"]
        index_to_update = supporting_evidence_files.index(
            next(filter(lambda x: x["attachment_id"] == attachment_id, supporting_evidence_files), None)
        )

        if None is index_to_update:
            raise ValueError(f"Supporting Evidence identifier {attachment_id} does not exist for {analysis_name}")

        supporting_evidence_files[index_to_update]['name'] = updated_content['name']
        if updated_content['data'] not in [None, '']:
            supporting_evidence_files[index_to_update]['data'] = updated_content['data']
        supporting_evidence_files[index_to_update]['comments'] = updated_content['comments']

        updated_document = self.collection.find_one_and_update(
            {"name": analysis_name},
            {"$set": {"supporting_evidence_files": supporting_evidence_files}},
            return_document=ReturnDocument.AFTER,
        )

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

        return updated_document
