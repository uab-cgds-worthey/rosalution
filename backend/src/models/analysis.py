"""
Manages Analyses for rosalution. An analysis within rosalution comprises of
of identifiers, case notes, and the genomic units being analyzed.
"""
# pylint: disable=too-few-public-methods
from datetime import date
import json
import re
from typing import List, Optional
from pydantic import BaseModel, computed_field, model_validator

from .event import Event

from ..enums import EventType, StatusType, GenomicUnitType


class GenomicUnit(BaseModel):
    """The basic units within an analysis"""

    gene: Optional[str] = None
    transcripts: List = []
    variants: List = []


class Section(BaseModel, frozen=True):
    """The sections of case notes associated with an analysis"""

    header: str
    attachment_field: Optional[str] = None
    content: List = []

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        """Allows FastAPI to valid and unpack the JSON of data into the model"""
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class BaseAnalysis(BaseModel):
    """The share parts of an analysis and it's summary"""

    name: str
    description: Optional[str] = None
    nominated_by: str
    timeline: List[Event] = []
    third_party_links: Optional[List] = []

    @computed_field
    @property
    def created_date(self) -> date:
        """The created date derived from the create event in the timeline"""
        if len(self.timeline) == 0:
            return None

        return next((event.timestamp.date() for event in self.timeline if event.event == EventType.CREATE), None)

    @computed_field
    @property
    def last_modified_date(self) -> date:
        """The last modified date derived from the last event in the timeline"""
        if len(self.timeline) == 0:
            return None

        last_event = sorted(self.timeline, key=lambda event: event.timestamp, reverse=True)[0]
        return last_event.timestamp.date()

    @computed_field
    @property
    def latest_status(self) -> StatusType:
        """The status as calculated from the events on the timeline"""
        if len(self.timeline) == 0:
            return None

        last_event = sorted(self.timeline, key=lambda event: event.timestamp, reverse=True)[0]
        return StatusType.from_event(last_event.event)


class AnalysisSummary(BaseAnalysis):
    """Models the summary of an analysis"""

    genomic_units: List[GenomicUnit] = []


class Analysis(BaseAnalysis):
    """Models a detailed analysis"""

    genomic_units: List[GenomicUnit] = []
    sections: List[Section] = []
    discussions: List = []
    attachments: List = []
    manifest: List = []

    def units_to_annotate(self):
        """Returns the types of genomic units within the analysis"""
        units = []
        for unit in self.genomic_units:
            if hasattr(unit, "gene"):
                units.append({"unit": unit.gene, "type": GenomicUnitType.GENE})
            for transcript in unit.transcripts:
                units.append({
                    "unit": transcript["transcript"],
                    "type": GenomicUnitType.TRANSCRIPT,
                })
            for variant in unit.variants:
                if "hgvs_variant" in variant and variant["hgvs_variant"]:
                    transcript = variant["hgvs_variant"].split(':')[0]
                    transcript_without_version = re.sub(r'\..*', '', transcript)
                    units.append({
                        "unit": variant["hgvs_variant"],
                        "type": GenomicUnitType.HGVS_VARIANT,
                        "genomic_build": variant["build"],
                        "transcript": transcript_without_version,
                    })

        return units

    def find_section_field_by_attachment_id(self, attachment_id):
        """
        Returns a tuple of the Section and field of section that the attachment is in, otherwise returns (None, None)
        """

        def attribute_type_in_field(attribute_key, field_value):
            return attribute_key if attribute_key in field_value else ''

        for section in self.sections:
            for field in section.content:
                for value in field['value']:
                    for key in ['file_id', 'attachment_id']:
                        if attribute_type_in_field(key, value) and value[key] == attachment_id:
                            return (section, field)
        return (None, None)

    def find_discussion_post(self, discussion_post_id):
        """
        Finds a specific discussion post in an analysis by the discussion post id otherwise returns none
        if no discussion with that post is in the analysis.
        """
        for discussion in self.discussions:
            if discussion['post_id'] == discussion_post_id:
                return discussion

        return None

    def find_discussion_reply(self, discussion_post_id, discussion_reply_id):
        """
        Finds a specific discussion reply to a discussion post in an analysis by the discussion post id 
        otherwise returns none if no reply with that reply is in the analysis.
        """

        discussion_post = self.find_discussion_post(discussion_post_id)

        for reply in discussion_post['thread']:
            if reply['reply_id'] == discussion_reply_id:
                return reply

        return None

    def find_authored_discussion_post(self, discussion_post_id, client_id):
        """
        Finds a discussion post from a user that authored the post in an analysis otherwise returns none if the post
        was found, but the user did not author the post
        """
        discussion_post = self.find_discussion_post(discussion_post_id)

        if discussion_post is None:
            raise ValueError(f"Post '{discussion_post_id}' does not exist.")

        if discussion_post['author_id'] == client_id:
            return discussion_post

        return None

    def find_authored_discussion_reply(self, discussion_post_id, discussion_reply_id, client_id):
        """
        Finds a discussion reply from a user that authored the reply to a post in an analysis otherwise returns none 
        if the reply was found, but the user did not author the reply
        """

        discussion_reply = self.find_discussion_reply(discussion_post_id, discussion_reply_id)

        if discussion_reply is None:
            raise ValueError(f"Post '{discussion_reply_id}' does not exist.")

        if discussion_reply['author_id'] == client_id:
            return discussion_reply

        return None

    def is_file_attached(self, attachment_id):
        """
        Returns true if any of the attachments in the analysis contains the attachment id.
        """
        return any(attachment['attachment_id'] == attachment_id for attachment in self.attachments)
