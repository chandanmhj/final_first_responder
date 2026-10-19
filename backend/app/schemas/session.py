"""Request and response models for profile and sessions."""
from pydantic import BaseModel, Field


class ProfileUpdate(BaseModel):
    """Fields a user may change on their own profile."""

    full_name: str | None = Field(default=None, max_length=120)
    role: str | None = Field(default=None, pattern="^(common|responder)$")
    cert_number: str | None = Field(default=None, max_length=60)
    attested: bool | None = None


class SessionRename(BaseModel):
    title: str = Field(min_length=1, max_length=120)
