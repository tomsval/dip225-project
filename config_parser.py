import os
from dataclasses import dataclass
import tomllib


# Datu klase, kas satur lietotājvārdu un paroli
@dataclass(init=True, eq=True)
class Credentials:
    identifier: str
    password: str


# Nolasa konfigurācijas failā config.toml esošo ORTUS lietotājvārdu un paroli un atgriež tos datu klasē
def get_ortus_credentials() -> Credentials:
    if not os.path.exists("config.toml"):
        raise FileNotFoundError(
            "Konfigurācijas fails 'config.toml' nav atrasts pamata mapē."
        )

    with open("config.toml", "rb") as f:
        try:
            config = tomllib.load(f)

            username = config["ortus-identity"]["username"]
            password = config["ortus-identity"]["password"]

            return Credentials(username, password)
        except tomllib.TOMLDecodeError as err:
            print(f"Kļūda konfigurācijas faila dekodēšanā: {err}")
            f.close()
