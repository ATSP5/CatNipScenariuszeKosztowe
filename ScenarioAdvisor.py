from typing import List

from PlnFormat import PlnFormat
from ScenarioEngine import ScenarioEngine
from ScenarioResult import ScenarioResult


class ScenarioAdvisor:
    """Zamienia wynik scenariusza w odpowiedź: co się stanie z EBITDA, które produkty są zagrożone i co z tym zrobić."""

    def __init__(self, formatter: PlnFormat):
        self.formatter = formatter

    def advisor(self) -> "ScenarioAdvisor":
        return self

    def findings(self, engine: ScenarioEngine, base: ScenarioResult, result: ScenarioResult, resource_id: str) -> List[str]:
        f = self.formatter
        scenario = result.scenario
        change = result.ebitda - base.ebitda
        lines = ["%s: EBITDA %s → %s (%s, %s). Marża EBITDA %s → %s." % (
            scenario.name, f.short_zl(base.ebitda), f.short_zl(result.ebitda), f.short_zl(change),
            f.signed_pct(100 * change / base.ebitda) if base.ebitda else "—",
            f.pct(base.ebitda_margin), f.pct(result.ebitda_margin))]
        at_risk = result.at_risk()
        if at_risk:
            lines.append("Produkty zagrożone (marża pokrycia < %s): %s." % (f.pct(at_risk[0].AT_RISK_MARGIN_PCT, 0), ", ".join(
                "%s — %s" % (p.name, f.pct(p.margin_pct)) for p in at_risk)))
        else:
            lines.append("Żaden produkt nie schodzi poniżej 5% marży pokrycia.")
        needed = [p for p in result.products if p.required_price_increase_pct >= 0.05]
        if needed and scenario.pass_through_pct < 100:
            weighted = sum(p.required_price_increase_pct * p.price * p.volume for p in needed) / sum(p.price * p.volume for p in result.products)
            top = sorted(needed, key=lambda p: -p.required_price_increase_pct)[:3]
            lines.append("Żeby utrzymać marże w złotych, ceny trzeba podnieść średnio o %s — najbardziej: %s." % (
                f.pct(weighted), ", ".join("%s %s" % (p.name, f.signed_pct(p.required_price_increase_pct)) for p in top)))
        limit = engine.shock_to_zero_ebitda(resource_id, scenario.pass_through_pct, scenario.volume_change_pct)
        name = engine.resource_names[resource_id]
        if limit == float("inf"):
            lines.append("Przy tych założeniach wzrost ceny surowca „%s” nie sprowadzi EBITDA do zera." % name)
        else:
            lines.append("EBITDA spadnie do zera dopiero przy wzroście ceny surowca „%s” o %s." % (name, f.pct(limit, 0)))
        if result.break_even_revenue != float("inf"):
            lines.append("Próg rentowności: %s przychodu (zapas bezpieczeństwa %s)." % (
                f.short_zl(result.break_even_revenue), f.pct(100 * (1 - result.break_even_revenue / result.revenue))))
        return lines
