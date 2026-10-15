import time
from typing import Dict, List, Sequence, Tuple

import numpy as np

from CostModel import CostModel
from PipelineStep import PipelineStep
from ProductResult import ProductResult
from Scenario import Scenario
from ScenarioResult import ScenarioResult


class ScenarioEngine:
    """Przelicza wynik firmy dla dowolnej zmiany cen surowców, cen sprzedaży i wolumenu.

    Koszt jednostkowy = Σ (zużycie z BOM × cena surowca × (1 + szok)) + robocizna. Cena rośnie o
    pass_through_pct % wzrostu kosztu jednostkowego, wolumen o volume_change_pct, koszty stałe zostają.
    """

    LADDER = (0.0, 10.0, 15.0, 25.0)

    def __init__(self, model: CostModel):
        started = time.perf_counter()
        self.model = model
        products = model.products.set_index("product_id")
        self.product_ids = list(products.index)
        self.names = products.name.to_dict()
        self.resource_ids = list(model.resources.resource_id)
        self.resource_names = dict(zip(model.resources.resource_id, model.resources.name))
        self.usage = (model.bom.pivot_table(index="product_id", columns="resource_id", values="qty_per_unit", aggfunc="sum")
                      .reindex(index=self.product_ids, columns=self.resource_ids).fillna(0.0).to_numpy())
        self.prices = model.resources.set_index("resource_id").price.reindex(self.resource_ids).to_numpy(dtype=float)
        self.sell_price = products.sell_price.to_numpy(dtype=float)
        self.volume = products.annual_volume.to_numpy(dtype=float)
        self.labour = products.labour_cost.to_numpy(dtype=float)
        self.fixed_costs = float(model.overheads.annual_pln.sum())
        self.base_unit_cost = self.usage @ self.prices + self.labour
        model.scan.pipeline.append(PipelineStep("Build cost model", "%d produktów × %d surowców, koszty stałe %d pozycji" % (
            len(self.product_ids), len(self.resource_ids), len(model.overheads)), time.perf_counter() - started))

    def engine(self) -> "ScenarioEngine":
        return self

    def resource_options(self) -> List[Tuple[str, str]]:
        return [(rid, self.resource_names[rid]) for rid in self.resource_ids]

    def base(self) -> ScenarioResult:
        return self.run(Scenario("BASE"))

    def run(self, scenario: Scenario) -> ScenarioResult:
        factors = np.array([1 + scenario.shocks.get(rid, 0.0) / 100 for rid in self.resource_ids])
        unit_cost = self.usage @ (self.prices * factors) + self.labour
        price = self.sell_price + scenario.pass_through_pct / 100 * (unit_cost - self.base_unit_cost)
        volume = self.volume * (1 + scenario.volume_change_pct / 100)
        base_margin = 100 * (1 - self.base_unit_cost / self.sell_price)
        margin = 100 * (1 - unit_cost / price)
        required = 100 * np.maximum(unit_cost - self.base_unit_cost, 0) / self.sell_price
        products = [ProductResult(pid, self.names[pid], float(price[i]), float(unit_cost[i]), float(self.base_unit_cost[i]),
                                  float(volume[i]), float(base_margin[i]), float(margin[i]),
                                  float((price[i] - unit_cost[i]) * volume[i]), float(required[i]))
                    for i, pid in enumerate(self.product_ids)]
        return ScenarioResult(scenario, float(price @ volume), float(unit_cost @ volume), self.fixed_costs, products)

    def shock(self, resource_id: str, shock_pct: float, pass_through_pct: float = 0.0, volume_change_pct: float = 0.0) -> ScenarioResult:
        name = "BASE" if not shock_pct else "%s %+g%%" % (self.resource_names[resource_id], shock_pct)
        return self.run(Scenario(name, {resource_id: shock_pct}, pass_through_pct, volume_change_pct))

    def ladder(self, resource_id: str, pass_through_pct: float = 0.0, volume_change_pct: float = 0.0,
               shocks: Sequence[float] = LADDER) -> List[ScenarioResult]:
        return [self.shock(resource_id, s, pass_through_pct, volume_change_pct) for s in shocks]

    def sensitivity(self, shock_pct: float = 10.0) -> Dict[str, float]:
        """Zmiana EBITDA [zł] przy wzroście ceny każdego surowca o shock_pct, od najgroźniejszego."""
        base = self.base().ebitda
        impact = {self.resource_names[rid]: self.shock(rid, shock_pct).ebitda - base for rid in self.resource_ids}
        return dict(sorted(impact.items(), key=lambda item: item[1]))

    def shock_to_zero_ebitda(self, resource_id: str, pass_through_pct: float = 0.0, volume_change_pct: float = 0.0) -> float:
        """O ile % może zdrożeć surowiec, zanim EBITDA spadnie do zera (EBITDA jest liniowa względem szoku)."""
        at_zero = self.shock(resource_id, 0.0, pass_through_pct, volume_change_pct).ebitda
        at_hundred = self.shock(resource_id, 100.0, pass_through_pct, volume_change_pct).ebitda
        slope = (at_hundred - at_zero) / 100
        if slope >= 0:
            return float("inf")
        return max(0.0, -at_zero / slope)

    def cost_structure(self) -> Dict[str, float]:
        """Roczny koszt każdego surowca, robocizny i kosztów stałych w scenariuszu bazowym."""
        spend = (self.usage * self.prices).T @ self.volume
        structure = {self.resource_names[rid]: float(spend[i]) for i, rid in enumerate(self.resource_ids)}
        structure["Robocizna"] = float(self.labour @ self.volume)
        structure["Koszty stałe"] = self.fixed_costs
        return dict(sorted(structure.items(), key=lambda item: -item[1]))
