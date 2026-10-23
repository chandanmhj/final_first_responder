"""Request and response models for profile and sessions."""
from pydantic import BaseModel, Field


class ProfileUpdate(BaseModel):
    """Fields a user may change on their own profile."""

    full_name: str | None = Field(default=None, max_length=120)
    role: str | None = Field(default=None, pattern="^(common|responder)$")
    cert_number: str | None = Field(default=None, max_length=60)
    attested: bool | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    sex: str | None = Field(default=None, max_length=30)
    blood_group: str | None = Field(default=None, max_length=10)
    allergies: str | None = Field(default=None, max_length=300)
    conditions: str | None = Field(default=None, max_length=300)
    medications: str | None = Field(default=None, max_length=300)
    emergency_contact: str | None = Field(default=None, max_length=120)


class SessionPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    pinned: bool | None = None