"""
Enumerations for the rosalution project.
"""
from enum import Enum


class SectionRowType(str, Enum):
    """The types of data stored within a field in an Analysis' sections."""

    TEXT = 'text'
    IMAGE = 'image'
    DOCUMENT = 'document'
    LINK = 'link'


class GenomicUnitType(str, Enum):
    """Enumeration of the different types of genomic units that can be analyzed"""

    GENE = "gene"
    TRANSCRIPT = "transcript"
    VARIANT = "variant"
    HGVS_VARIANT = "hgvs_variant"
    INVALID = "invalid"


class AnnotationSourceType(str, Enum):
    """Enumeration of the different types of annotation sources in the configuration"""

    HTTP = "http"
    CSV = "csv"
    NONE = "none"


class EventType(str, Enum):
    """Enumeration of the different events for an analyses"""

    CREATE = 'create'
    READY = 'ready'
    OPENED = 'opened'
    APPROVE = 'approve'
    HOLD = 'hold'
    DECLINE = 'decline'


class StatusType(str, Enum):
    """Enumeration of the different statuses for an analyses"""

    PREPARATION = "Preparation"
    READY = "Ready"
    ACTIVE = "Active"
    APPROVED = "Approved"
    ON_HOLD = "On-Hold"
    DECLINED = "Declined"

    @classmethod
    def from_event(cls, event):
        """Takes an event from an analysis time and returns the status"""
        event_text = "Preparation"

        if event == EventType.READY:
            event_text = "Ready"
        elif event == EventType.OPENED:
            event_text = "Active"
        elif event == EventType.APPROVE:
            event_text = "Approved"
        elif event == EventType.HOLD:
            event_text = "On-Hold"
        elif event == EventType.DECLINE:
            event_text = "Declined"

        return cls(event_text)


class ThirdPartyLinkType(str, Enum):
    """Enumeration of the different types of third party links"""

    MONDAY_COM = "monday_com"
    PHENOTIPS_COM = "phenotips_com"
