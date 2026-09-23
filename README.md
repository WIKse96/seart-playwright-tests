# seart.pl – testy Playwright + pytest

Automatyczne testy sklepu [seart.pl](https://www.seart.pl):

- `tests/test_page_load.py` – mierzy czas ładowania strony produktu i sprawdza, czy mieści się w zadanym limicie.
- `tests/test_add_to_cart.py` – dodaje produkt "Komoda drewniana Rustyk 3/9" do koszyka i weryfikuje aktualizację koszyka.
- `tests/test_login.py` – loguje się na konto testowe.

## Instalacja

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Konfiguracja

Skopiuj `.env.example` do `.env` i uzupełnij dane (plik `.env` jest ignorowany przez git):

```bash
cp .env.example .env
```

| Zmienna | Opis | Domyślnie |
|---|---|---|
| `SEART_LOGIN_EMAIL` | login do konta testowego | – (wymagane) |
| `SEART_LOGIN_PASSWORD` | hasło do konta testowego | – (wymagane) |
| `SEART_PRODUCT_URL` | URL testowanego produktu | komoda Rustyk 3/9 |
| `PAGE_LOAD_THRESHOLD_MS` | limit czasu ładowania strony w ms | 8000 |

## Uruchomienie testów

```bash
pytest --headed          # z widoczną przeglądarką
pytest                    # w trybie headless
pytest tests/test_login.py -v
```

## CI

Workflow GitHub Actions (`.github/workflows/playwright.yml`) uruchamia testy przy każdym pushu/PR.
Dane logowania należy dodać jako sekrety repozytorium: `SEART_LOGIN_EMAIL`, `SEART_LOGIN_PASSWORD`.
