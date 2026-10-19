"""Session state for a running scenario."""
from dataclasses import asdict, dataclass, field


@dataclass
class ScenarioState:
    """Where the user is in a scenario. Stored on the chat session."""

    status: str = "idle"  # idle | active | completed
    condition: str | None = None
    location: str | None = None
    role: str = "common"
    for_self: bool = False
    age_band: str | None = None
    protocol: str = "adult"
    incident_id: str | None = None
    index: int = 0
    steps: list[dict] = field(default_factory=list)
    lat: float | None = None
    lon: float | None = None

    @classmethod
    def from_dict(cls, d: dict | None) -> "ScenarioState":
        return cls(**{k: v for k, v in (d or {}).items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def active(self) -> bool:
        return self.status == "active" and bool(self.steps)

    def current(self) -> dict | None:
        return self.steps[self.index] if self.active and 0 <= self.index < len(self.steps) else None

    def advance(self) -> dict | None:
        """Move to the next step. Returns it, or None (and marks the scenario completed) at the end."""
        if self.index + 1 >= len(self.steps):
            self.status = "completed"
            return None
        self.index += 1
        return self.current()
