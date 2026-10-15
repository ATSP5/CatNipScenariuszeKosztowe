Silnik scenariuszy „co jeśli”: przelicza wynik firmy dla dowolnej zmiany cen surowców, cen sprzedaży i wolumenu. Koszt jednostkowy = Σ (zużycie z BOM × cena surowca × (1 + szok)) + robocizna; cena rośnie o `pass_through_pct` % wzrostu kosztu, wolumen o `volume_change_pct`, koszty stałe zostają.

## model
Wejście — `CostModel`.

## engine
Wyjście bloku — ten silnik, podawany do strony raportu.

## run
Wynik (`ScenarioResult`) dla dowolnego `Scenario`.

## base
Scenariusz bazowy.

## shock
Scenariusz zmiany ceny jednego surowca.

## ladder
Drabina scenariuszy BASE → +10% → +15% → +25%.

## sensitivity
Zmiana EBITDA przy +10% ceny każdego surowca — który boli najbardziej.

## shock_to_zero_ebitda
O ile % może zdrożeć surowiec, zanim EBITDA spadnie do zera.

## cost_structure
Roczny koszt każdego surowca, robocizny i kosztów stałych.
