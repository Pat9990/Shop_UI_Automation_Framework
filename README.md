# SauceDemo Test Automation

Projekt automatyzuje testy funkcjonalne strony [SauceDemo](https://www.saucedemo.com/) przy użyciu **Selenium WebDriver**, **pytest** i **Page Object Model (POM)**.

---

## Spis treści

- [Technologie](#technologie)
- [Instalacja](#instalacja)
- [Uruchamianie testów](#uruchamianie-testów)
- [Raporty](#raporty)
- [Struktura projektu](#struktura-projektu)
- [Konwencje](#konwencje)
- [Przykładowe testy](#przykładowe-testy)

---

## Technologie

- Python 3.11+
- Selenium 4.x
- pytest 8.x
- webdriver-manager 4.x
- Firefox / Chrome
- pytest-html (raporty w HTML)

---

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone <repo-url>
cd <project-folder>
```
2. Stwórz wirtualne środowisko:
```bash
python -m venv .venv
```
3.Aktywuj wirtualne środowisko:
Windows
```bash
.venv\Scripts\activate
```
4. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

## Uruchamianie testów
```bash
pytest -v
```
- Testy korzystają z Firefoxa domyślnie.
- Wszystkie testy automatycznie otwierają przeglądarkę, wykonują akcje i zamykają ją po teście

## Raporty
Możesz generować raporty w HTML za pomocą pytest-html:
```bash
pytest --html=reports/report.html --self-contained-html
```
Raport zostanie zapisany w folderze reports/ (trzeba go utworzyć, jeśli nie istnieje).
Zawiera szczegóły testów, wyniki itp.

## Struktura projektu
```
project/
│
├── core/                 # Konfiguracja i ustawienia globalne
│   └── config.py         # URL-e, dane testowe, stałe
│
├── pages/                # Page Object Models
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── tests/                # Testy automatyczne
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── conftest.py           # Pytest fixtures
├── requirements.txt      # Lista zależności
├── reports/              # Raporty HTML z testów
└── README.md             # Dokumentacja
```
## Konwencje
- Page Object Model – każda strona ma swoją klasę w pages/.
- Lokatory prywatne zaczynają się od __, metody pomocnicze od _.
- Publiczne metody opisują akcje użytkownika (np. login, add_to_cart, checkout_overview).
- checkout_overview).

Dane konfiguracyjne (URL-e, login, hasła) znajdują się w core/config.py.

## Przykładowe testy
- Logowanie poprawne i błędne (test_login.py)
- Sortowanie produktów według nazwy i ceny (test_inventory.py)
- Dodawanie/usuwanie produktów w koszyku (test_cart.py)
- Checkout i weryfikacja sumy cen (test_checkout.py)