# Testy Playwright + pytest – seart.pl / rustykalneuchwyty.pl / seart.cz

Automatyczne testy trzech sklepów grupy Seart, zdefiniowanych w [sites.py](sites.py):

- **seart.pl** – Komoda drewniana Rustyk 3/9
- **rustykalneuchwyty.pl** – Zawias meblowy COUNTRY
- **seart.cz** – Nábytková knopka Rustyk 30 mm s dekorativní destičkou

Każdy z trzech testów jest sparametryzowany i uruchamia się osobno dla każdego sklepu (`test_xxx[seart_pl]`, `test_xxx[rustykalneuchwyty_pl]`, `test_xxx[seart_cz]`):

- `tests/test_page_load.py` – mierzy czas ładowania strony produktu i sprawdza, czy mieści się w zadanym limicie.
- `tests/test_add_to_cart.py` – dodaje produkt do koszyka i weryfikuje komunikat potwierdzający.
- `tests/test_login.py` – loguje się na konto testowe.

Dodatkowo każdy test (`conftest.py: fail_on_http_error`) automatycznie sprawdza, czy główny
dokument strony nie zwrócił błędu HTTP 4xx/5xx podczas wykonywanej akcji.

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
| `SEART_LOGIN_EMAIL` / `SEART_LOGIN_PASSWORD` | login do konta testowego na seart.pl | – (wymagane) |
| `SEART_PL_PRODUCT_URL` | URL testowanego produktu na seart.pl | komoda Rustyk 3/9 |
| `SEART_PL_LOAD_THRESHOLD_MS` | limit czasu ładowania seart.pl w ms | 7600 |
| `RUSTYKALNEUCHWYTY_LOGIN_EMAIL` / `RUSTYKALNEUCHWYTY_LOGIN_PASSWORD` | login do konta testowego na rustykalneuchwyty.pl | – (wymagane) |
| `RUSTYKALNEUCHWYTY_PRODUCT_URL` | URL testowanego produktu na rustykalneuchwyty.pl | zawias COUNTRY |
| `RUSTYKALNEUCHWYTY_LOAD_THRESHOLD_MS` | limit czasu ładowania rustykalneuchwyty.pl w ms | 5000 |
| `SEART_CZ_LOGIN_EMAIL` / `SEART_CZ_LOGIN_PASSWORD` | login do konta testowego na seart.cz | – (wymagane) |
| `SEART_CZ_PRODUCT_URL` | URL testowanego produktu na seart.cz | knopka Rustyk 30 mm |
| `SEART_CZ_LOAD_THRESHOLD_MS` | limit czasu ładowania seart.cz w ms | 4800 |

Progi czasu ładowania: zmierzony lokalnie max z 5 przebiegów + ~50% marginesu (na wolniejsze
przebiegi na runnerach GitHub Actions) — seart.pl 5079 ms → 7600 ms, rustykalneuchwyty.pl
3306 ms → 5000 ms, seart.cz 3183 ms → 4800 ms.
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

Uruchomienie lokalne (z aktywnym `.venv` i uzupełnionym `.env`) **nie zużywa minut GitHub Actions** —
limit dotyczy wyłącznie przebiegów wykonywanych na serwerach GitHuba (cron, push, `workflow_dispatch`).
Z `NOTIFY_NTFY_ENABLED=true` w `.env` lokalny `pytest` wysyła to samo powiadomienie co CI.

## CI

Workflow GitHub Actions (`.github/workflows/playwright.yml`) uruchamia testy przy każdym pushu/PR
oraz na żądanie (`workflow_dispatch`) — patrz sekcja niżej o zewnętrznym harmonogramie. Dane
logowania należy dodać jako sekrety repozytorium: `SEART_LOGIN_EMAIL`, `SEART_LOGIN_PASSWORD`,
`RUSTYKALNEUCHWYTY_LOGIN_EMAIL`, `RUSTYKALNEUCHWYTY_LOGIN_PASSWORD`, `SEART_CZ_LOGIN_EMAIL`,
`SEART_CZ_LOGIN_PASSWORD`.

**Dlaczego nie `schedule:`?** GitHub Actions ma wbudowany harmonogram cron, ale w praktyce jest on
zawodny na repo z małym ruchem — GitHub sam nie gwarantuje wykonania co do minuty. W testach na
tym repo (`cron: "0 */2 * * *"`, potem `"17 */2 * * *"`) GitHub pomijał 3 z 4 zaplanowanych
uruchomień z rzędu, mimo poprawnej konfiguracji. To udokumentowane ograniczenie GitHuba, nie błąd
w tym kodzie. Dlatego harmonogram jest realizowany **z zewnątrz** (patrz niżej).

### Zewnętrzny harmonogram (cron-job.org → workflow_dispatch)

Zamiast wbudowanego `schedule:`, darmowy zewnętrzny serwis cron (np. [cron-job.org](https://cron-job.org))
co 2 godziny woła GitHub REST API, żeby odpalić workflow ręcznie (`workflow_dispatch`) — to
wykonanie faktycznie jest natychmiastowe (bez kolejkowania jak przy `schedule:`).

Konfiguracja (jednorazowa, po stronie użytkownika):

1. Utwórz **fine-grained Personal Access Token**: https://github.com/settings/personal-access-tokens/new
   - Repository access → Only select repositories → `seart-playwright-tests`
   - Permissions → Actions → **Read and write**
   - Expiration: dowolne (np. 1 rok)
2. Załóż darmowe konto na https://cron-job.org
3. Utwórz nowy cronjob:
   - **URL:** `https://api.github.com/repos/WIKse96/seart-playwright-tests/actions/workflows/playwright.yml/dispatches`
   - **Method:** `POST`
   - **Headers:**
     - `Authorization: Bearer <TWÓJ_PAT>`
     - `Accept: application/vnd.github+json`
     - `Content-Type: application/json`
   - **Body:** `{"ref":"master"}`
   - **Schedule:** co 2 godziny
4. Token wklej bezpośrednio w formularzu cron-job.org — nie udostępniaj go nigdzie indziej.

### Dead man's switch (healthchecks.io)

Ostatni krok workflow pinguje `HEALTHCHECKS_PING_URL` (sekret repozytorium) przy każdym
uruchomieniu, niezależnie od wyniku testów. To osobny, zewnętrzny sygnał "monitoring żyje" —
jeśli zewnętrzny cron-job.org przestanie wołać GitHub (np. wygasł token, konto zablokowane),
ntfy/email z wynikami testów też przestaną przychodzić, ale nic Cię o tym nie ostrzeże.
healthchecks.io wykrywa brak pingu i wysyła osobny alert mailem. Skoro wyzwalanie jest teraz przez
`workflow_dispatch` (natychmiastowe, bez kolejkowania GitHuba), grace period na healthchecks.io
można bezpiecznie zmniejszyć z powrotem do ok. 30–45 minut.

Przy testach 3 sklepów pojedynczy przebieg trwa ~100–120 s (2 min rozliczeniowe). Przy 12
uruchomieniach/dobę (co 2h) to ~360 runów/miesiąc × 2 min ≈ 720 min/miesiąc — bezpieczny zapas
wobec darmowego limitu 2000 min/miesiąc dla prywatnego repo.
