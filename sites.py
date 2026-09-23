import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    id: str
    label: str
    product_url: str
    login_url: str
    product_name: str
    confirmation_template: str
    email_field_name: str
    password_field_name: str
    login_button_name: str
    cookie_reject_label: str
    account_page_title: str
    email_env: str
    password_env: str

    @property
    def confirmation_text(self) -> str:
        return self.confirmation_template.format(name=self.product_name)

    @property
    def credentials(self) -> dict:
        return {
            "email": os.environ[self.email_env],
            "password": os.environ[self.password_env],
        }


SITES = [
    Site(
        id="seart_pl",
        label="seart.pl",
        product_url=os.environ.get(
            "SEART_PL_PRODUCT_URL",
            "https://www.seart.pl/drewniana-komoda-sosnowa-rustyk-3-9.html",
        ),
        login_url="https://www.seart.pl/customer/account/login/",
        product_name="Komoda drewniana Rustyk 3/9",
        confirmation_template="{name} został dodany do Twojego koszyka.",
        email_field_name="Adres e-mail",
        password_field_name="Hasło",
        login_button_name="Logowanie",
        cookie_reject_label="Odrzuć",
        account_page_title="Moje konto",
        email_env="SEART_LOGIN_EMAIL",
        password_env="SEART_LOGIN_PASSWORD",
    ),
    Site(
        id="rustykalneuchwyty_pl",
        label="rustykalneuchwyty.pl",
        product_url=os.environ.get(
            "RUSTYKALNEUCHWYTY_PRODUCT_URL",
            "https://rustykalneuchwyty.pl/zawias-meblowy-country.html",
        ),
        login_url="https://rustykalneuchwyty.pl/customer/account/login/",
        product_name="Zawias meblowy COUNTRY",
        confirmation_template="{name} został dodany do Twojego koszyka.",
        email_field_name="Adres e-mail",
        password_field_name="Hasło",
        login_button_name="Logowanie",
        cookie_reject_label="Odrzuć",
        account_page_title="Moje konto",
        email_env="RUSTYKALNEUCHWYTY_LOGIN_EMAIL",
        password_env="RUSTYKALNEUCHWYTY_LOGIN_PASSWORD",
    ),
    Site(
        id="seart_cz",
        label="seart.cz",
        product_url=os.environ.get(
            "SEART_CZ_PRODUCT_URL",
            "https://www.seart.cz/nabytkova-knopka-rustyk-30-mm-s-dekorativni-destickou.html",
        ),
        login_url="https://www.seart.cz/customer/account/login/",
        product_name="Nábytková knopka Rustyk 30 mm s dekorativní destičkou",
        confirmation_template="{name} byl úspěšně přidán do košíku.",
        email_field_name="Emailová adresa",
        password_field_name="Heslo",
        login_button_name="Přihlášení",
        cookie_reject_label="Odmítnout",
        account_page_title="Můj účet",
        email_env="SEART_CZ_LOGIN_EMAIL",
        password_env="SEART_CZ_LOGIN_PASSWORD",
    ),
]
