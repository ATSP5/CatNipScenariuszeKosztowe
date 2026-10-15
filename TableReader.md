Czyta tabelę z pliku CSV, JSON (lista rekordów) albo Excel do `pandas.DataFrame` — loader nie musi wiedzieć, w jakim formacie firma trzyma dane.

## reader
Wyjście bloku — ten czytnik, podawany do loadera danych.

## format_of
Nazwa formatu pliku (`CSV`, `JSON`, `Excel`) po rozszerzeniu.

## read
Wczytuje plik. `dtypes` pozwala podać typy kolumn dużego CSV (np. `category` dla identyfikatorów), co przy milionie wierszy oszczędza pamięć.
