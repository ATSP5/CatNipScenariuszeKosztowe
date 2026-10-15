from dataclasses import dataclass, field
from typing import List

from ProductResult import ProductResult
from Scenario import Scenario


@dataclass
class ScenarioResult:
    """Wynik firmy w jednym scenariuszu: przychód, marża pokrycia, EBITDA, próg rentowności i produkty."""

    scenario: Scenario
    revenue: float
    variable_cost: float
    fixed_costs: float
    products: List[ProductResult] = field(default_factory=list)

    @property
    def contribution(self) -> float:
        return self.revenue - self.variable_cost

    @property
    def ebitda(self) -> float:
        return self.contribution - self.fixed_costs

    @property
    def ebitda_margin(self) -> float:
        return 100 * self.ebitda / self.revenue if self.revenue else 0.0

    @property
    def break_even_revenue(self) -> float:
        ratio = self.contribution / self.revenue if self.revenue else 0.0
        return self.fixed_costs / ratio if ratio > 0 else float("inf")

    def at_risk(self) -> List[ProductResult]:
        return sorted([p for p in self.products if p.status != "OK"], key=lambda p: p.margin_pct)
