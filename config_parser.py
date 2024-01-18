from dataclasses import dataclass
import tomllib


# Datu klase, kas satur lietotājvārdu un paroli
@dataclass(init=True, eq=True)
class ORTUSCredentials:
    username: str
    password: str


# Nolasa konfigurācijas failā config.toml esošo ORTUS lietotājvārdu un paroli un atgriež tos datu klasē
def parse_config() -> ORTUSCredentials | None:
    with open("config.toml", "rb") as f:
        try:
            config = tomllib.load(f)

            username = config["ortus-identity"]["username"]
            password = config["ortus-identity"]["password"]

            return ORTUSCredentials(username, password)
        except tomllib.TOMLDecodeError as err:
            print(f"Kļūda konfigurācijas faila dekodēšanā: {err}")
            f.close()
