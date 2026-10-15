from dataclasses import dataclass


@dataclass
class ProductResult:
    """Jeden produkt w scenariuszu: cena, koszt jednostkowy, marża pokrycia przed i po zmianie."""

    product_id: str
    name: str
    price: float
    unit_cost: float
    base_unit_cost: float
    volume: float
    base_margin_pct: float
    margin_pct: float
    contribution: float
    required_price_increase_pct: float

    AT_RISK_MARGIN_PCT = 5.0

    @property
    def status(self) -> str:
        if self.margin_pct < 0:
            return "strata"
        if self.margin_pct < self.AT_RISK_MARGIN_PCT:
            return "zagrożony"
        return "OK"
