# DatabaseFaker

# Wymagane oprogramowanie

## Python
  Wymagana wersja Pythona to 3.6+
## Biblioteki oracle
  Wymagany jest plik oci.dll, znajdujący się przykładowo w Oracle Instant Client. Ścieżka do folderu z tym plikiem musi znajdować się w zmiennej środowiskowej "Path".
  
  **Ważne** - 32/64-bitowe wersje Pythona i biblioteki oci.dll muszą się zgadzać.

## Biblioteki Pythona
  Wszystkie wymagane biblioteki Python znajdują się w pliku requirements.txt. Można je zainstalować komendą:
  
  `pip install -r requirements.txt`
  
# Uruchomienie samego skryptu

Wymagane jest ustawienie zmiennych środowiskowych DB_USERNAME oraz DB_PASSWORD w celu połączenia się z bazą danych.

Możliwa jest zmiana ziarna bezpośrednio w kodzie, w celu zmiany wygenerowanych losowo danych.
