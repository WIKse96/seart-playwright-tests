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
| `PAGE_LOAD_THRESHOLD_MS` | limit czasu ładowania strony w ms (lokalnie zmierzony czas `load`: 4,1–5,5 s; na runnerach GitHub Actions bywa wolniej, stąd wyższy margines) | 11000 |
| `NOTIFY_EMAIL_ENABLED` | `true`, żeby po każdym uruchomieniu testów wysłać email z podsumowaniem wyniku | `false` |
| `NOTIFY_EMAIL_FROM` | adres Gmail, z którego wysyłane jest powiadomienie | – |
| `NOTIFY_EMAIL_APP_PASSWORD` | [Gmail App Password](https://myaccount.google.com/apppasswords) konta z `NOTIFY_EMAIL_FROM` (nie zwykłe hasło) | – |
| `NOTIFY_EMAIL_TO` | adres odbiorcy powiadomienia | `NOTIFY_EMAIL_FROM` |
| `NOTIFY_NTFY_ENABLED` | `true`, żeby po testach wysłać powiadomienie push przez [ntfy.sh](https://ntfy.sh) | `false` |
| `NOTIFY_NTFY_TOPIC` | nazwa tematu ntfy — ustaw długi, losowy ciąg, bo temat działa jak "tajny URL" (kto zna nazwę, ten widzi powiadomienia) | – |
| `NOTIFY_NTFY_SERVER` | adres serwera ntfy (własny lub publiczny) | `https://ntfy.sh` |

## Powiadomienia

Po ustawieniu `NOTIFY_EMAIL_ENABLED=true` i/lub `NOTIFY_NTFY_ENABLED=true` w `.env`, po każdym
przebiegu `pytest` leci jedno zbiorcze powiadomienie z wynikiem (ile testów przeszło/nie przeszło
i które) — można włączyć jeden kanał albo oba naraz.

- **Email** wymaga wygenerowania [Gmail App Password](https://myaccount.google.com/apppasswords)
  dla konta nadawcy (konto musi mieć włączoną weryfikację dwuetapową).
- **ntfy.sh** nie wymaga konta ani instalacji — wystarczy wybrać unikalny `NOTIFY_NTFY_TOPIC`.
  Żeby dostać powiadomienie push na telefon, zainstaluj apkę [ntfy](https://ntfy.sh/) i zasubskrybuj
  ten sam temat; bez apki można sprawdzać powiadomienia w przeglądarce pod `https://ntfy.sh/<temat>`.
  Temat jest publicznie dostępny dla każdego, kto zna jego nazwę — traktuj go jak hasło.

## Uruchomienie testów

```bash
pytest --headed          # z widoczną przeglądarką
pytest                    # w trybie headless
pytest tests/test_login.py -v
```

## CI

Workflow GitHub Actions (`.github/workflows/playwright.yml`) uruchamia testy przy każdym pushu/PR.
Dane logowania należy dodać jako sekrety repozytorium: `SEART_LOGIN_EMAIL`, `SEART_LOGIN_PASSWORD`.
