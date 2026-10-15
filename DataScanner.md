**Data Scan** — rozpoznaje dane bez ręcznego opisu: typ każdej kolumny (`int`, `decimal`, `DateTime`, `string`, `bool`), braki, liczbę unikalnych wartości, klucz każdej tabeli (kolumna `*_id` bez braków i powtórzeń) oraz powiązania między plikami (kolumna `*_id`, której wartości w całości występują w kluczu innej tabeli). To ten sam mechanizm we wszystkich trzech analizach.

## scanner
Wyjście bloku — ten skaner, podawany do loadera danych.

## SAMPLE
Ile wartości próbki ogląda się przy rozpoznawaniu typu i przykładu.

## scan
Przyjmuje `{nazwa pliku: (format, DataFrame)}` i zwraca `DataScan` z profilami tabel i pierwszym krokiem pipeline'u.

## profile_column
Profil jednej kolumny (`ColumnProfile`).

## type_of
Rozpoznany typ kolumny; tekst w formacie `RRRR-MM-DD…` to `DateTime`.

## is_id_name
Czy nazwa kolumny wygląda na identyfikator (`id` albo `…_id`).

## mark_keys
Oznacza klucz każdej tabeli.

## link_references
Wiąże kolumny `…_id` z kluczami innych tabel, gdy wszystkie wartości się w nich znajdują.
