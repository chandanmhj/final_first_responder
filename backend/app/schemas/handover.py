"""Models for incident events."""
from pydantic import BaseModel, Field


class EventIn(BaseModel):
    """An event the user records by hand (for example 'called 108' or a note)."""

    event_type: str = Field(pattern="^(called_108|ambulance_arrived|cpr_started|aed_used|tourniquet_applied|helmet_removed|patient_moved|note)$")
    text: str | None = Field(default=None, max_length=500)
    occurred_at: str | None = None
