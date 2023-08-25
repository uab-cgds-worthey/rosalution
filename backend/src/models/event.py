"""
Creates Events that occur within the application to track important events that affect an analysis' status.
"""
from datetime import datetime, timezone
from pydantic import BaseModel

from ..enums import EventType


class Event(BaseModel):
    """Events that occur for an analysis"""

    event: EventType
    timestamp: datetime
    username: str

    @staticmethod
    def timestamp_create_event(username):
        """Creates a timestamp of the create event done by username"""
        return Event.timestamp_event(username, EventType.CREATE)

    @staticmethod
    def timestamp_ready_event(username):
        """Creates a timestamp of the ready event done by username"""
        return Event.timestamp_event(username, EventType.READY)

    @staticmethod
    def timestamp_event(username, event):
        """Creates a timestamp of the 'event' done by username"""
        return Event(**{
            "event": event,
            "timestamp": datetime.now(timezone.utc),
            "username": username,
        })
