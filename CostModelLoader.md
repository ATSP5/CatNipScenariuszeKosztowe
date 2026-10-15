Wczytuje produkty, BOM, ceny surowców i koszty stałe z `input/`, robi Data Scan i sprawdza, czy każda pozycja BOM wskazuje znany produkt i surowiec.

## folders
Wejście — `ProjectFolders`.

## reader
Wejście — `TableReader`.

## generator
Wejście — `DemoCostData`.

## scanner
Wejście — `DataScanner`.

## model
Wyjście bloku — `CostModel`.

## validate
Błąd, gdy BOM wskazuje nieznany produkt albo surowiec.
