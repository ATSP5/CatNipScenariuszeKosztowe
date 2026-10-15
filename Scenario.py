from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Scenario:
    """Założenia scenariusza: zmiany cen surowców (%), jaką część wzrostu kosztu przerzucamy na ceny, zmiana wolumenu."""

    name: str
    shocks: Dict[str, float] = field(default_factory=dict)
    pass_through_pct: float = 0.0
    volume_change_pct: float = 0.0
