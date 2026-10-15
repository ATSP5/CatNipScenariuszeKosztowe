Folder projektu — ten, w którym leży plik `.catnip` — oraz jego podfoldery `input/` (dane) i `output/` (wyniki). Działa identycznie lokalnie i w Dockerze (`/app`), bo szuka pliku `.catnip`, a nie ścieżki z dysku C:. Ten sam blok jest we wszystkich trzech projektach demonstracyjnych.

## input_name
Nazwa folderu z danymi wejściowymi, domyślnie `input`.

## output_name
Nazwa folderu na wyniki, domyślnie `output`.

## folders
Wyjście bloku — ta instancja, podawana do loadera danych (i zapisu CSV).

## find_root
Pierwszy z folderów: bieżący katalog roboczy, folder modułu — ten, w którym jest plik `.catnip`.

## input_path
Pełna ścieżka pliku w `input/`.

## output_path
Pełna ścieżka pliku w `output/`.
