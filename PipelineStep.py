from dataclasses import dataclass


@dataclass
class PipelineStep:
    """Jeden krok przetwarzania: co zrobiono, na czym i ile to trwało."""

    name: str
    detail: str
    seconds: float
