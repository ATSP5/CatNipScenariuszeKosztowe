Dane demonstracyjne producenta stolarki aluminiowej i PVC: produkty (`products.xlsx`), receptury (`bom.csv`), ceny surowców i energii (`resources.json`) oraz koszty stałe (`overheads.json`). Ceny produktów są dobrane tak, żeby firma miała ok. 9% marży EBITDA, a najtańsze wyroby aluminiowe — cienką marżę. Pliki powstają w `input/` tylko wtedy, gdy ich tam nie ma.

## generator
Wyjście bloku — ten generator, podawany do `CostModelLoader`.

## ensure
Tworzy brakujące pliki; zwraca `True`, gdy coś zapisał.

## RESOURCES
Surowce: identyfikator, nazwa, jednostka, cena, dostawca.

## PRODUCTS
Produkty: wolumen roczny, robocizna, docelowa marża pokrycia, BOM.

## TARGET_EBITDA_MARGIN
Docelowa marża EBITDA, z której wynikają koszty stałe.
