# ORTUS kalendāra automātiskais sinhronizēšanas rīks _OKS_

## Problēmas apraksts
Rīgas Tehniskās universitātes studiju portālā ORTUS studentiem ir iespējams aplūkot sev aktuālo nodarbību grafiku, kas tiek atjaunināts, kad notiek izmaiņas grafikā.

Lietotājiem, kuri vēlas pievienot un izmantot savu nodarbību grafiku ārpus ORTUS vides, ORTUS piedāvā lejupielādēt iCalendar formāta datni, kas satur nodarbību grafika informāciju, kuru tālāk ir iespējams pievienot citās kalendāra programmatūrās, piemēram, Google Calendar, Thunderbird vai Apple Calendar, apvienojot savus esošos kalendārus ar studiju nodarbību grafiku vienotā kalendārā, taču ar šādu risinājumu nodarbību grafiks netiek automātiski atjaunināts, tādēļ var rasties gadījums, kad svarīga informācija starp nodarbību grafikiem atšķiras, lietotājam nezinot.

Pastāv esoši risinājumi savstarpējai kalendāru datu sinhronizācijai, piemēram, izmantojot CalDAV protokolu, taču, lai to izmantotu, tam ir jābūt uzstādītam uz paša kalendāru servera ORTUSā, kas lietotājam nav iespējams.
## Projekta uzdevums
Izstrādāt programmatūru, kas automatizēti iegūst studenta nodarbību grafiku (iCalendar datni) no ORTUS un pievieno vai atjaunina esošo Google kalendāru ar jauniegūtajiem nodarbību grafika datiem periodiski, lietotāja noteiktā laika intervālā, izmantojot publiski pieejamo Google Calendar API.
## [Darbības demonstrācija](https://youtu.be/Nyxfd7P56tA)

## Uzstādīšana
### SVARĪGI VĒRTĒTĀJAM
Google Calendar API ierobežojumu dēļ jebkurš lietotājs ar Google kontu nevar lietot vai izmēģināt programmatūru, ja nav pats izveidojis Google Cloud projektu uz sava Google konta un sakonfigurējis OAuth piekrišanas atļaujas un ieguvis savu OAuth klienta kredenciāļu JSON failu, kas ir nepieciešams, lai varētu lietot Google Calendar API bez Cloud projekta publicēšanas, kas nav iespējams šī projekta darba ietvaros. Vairāk informācijas skatīt [šeit](https://developers.google.com/calendar/api/quickstart/python#set_up_your_environment).

Repozitorijā ir iekļauts fails `credentials.json`, kas ir nepieciešams OAuth autentifikācijas veikšanai. Gadījumā, ja izvēlaties izveidot un uzstādīt pats savu Google Cloud projektu, tad šo datni nepieciešams aizstāt ar savam projektam raksturīgo datni. Vairāk informācijas skatīt [šeit](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application).

Ja vēlaties izmēģināt OKS uz sava datora bez Google Cloud projekta uzstādīšanas, lūdzu atsūtiet savu Gmail e-pasta adresi, kuru izmantosiet pārbaudes veikšanai uz manu RTU e-pasta adresi, lai varu pievienot Jūsu Google kontu kā testa lietotāju. 

### Vides uzstādīšana
Lai varētu palaist programmatūru, nepieciešams instalēt OKS nepieciešamās bibliotēkas Python vidē. To var ērti izdarīt ar komandu

```bash
pip install --upgrade selenium ics webdriver-manager requests google-api-python-client google-auth-httplib2 google-auth-oauthlib 
```
Programmatūras lietošanai arī ir nepieciešams lejupielādēt un instalēt Google Chrome interneta pārluku, kas tiek izmantots automatizētai iCalendar datnes iegūšanai no ORTUSa. Pārlūku var lejupielādēt [šeit](https://www.google.com/chrome/).

## Lietošana
### Konfigurācija
Lai OKS varētu iegūt konkrētajam lietotājam raksturīgo nodarbību grafiku no ORTUSa, datnē `config.toml` zem `ortus-identity` lauka nepieciešams norādīt savu ORTUSa lietotājvārdu un paroli.

```toml
[ortus-identity]
username = "LIETOTĀJVĀRDS"
password = "PAROLE"
````
### Programmatūras palaišana
Pēc lietotājvārda un paroles ierakstīšanas konfigurācijas datnē OKS var palaist, var izmantot komandu
```bash
python oks.py
````
### Programmatūras darbība
Kad programmatūra tiek palaista, tā sākumā atver robotizētu Google Chrome logu, kas automatizēti ielogojas ORTUSā, izmantojot `config.toml` datnē norādīto lietotājvārdu un paroli. Tad notiek navigācija uz ORTUS sadaļu _Studentiem - Grafiki_. Kad lapa ir ielādējusies, programmatūra lejupielādē iCalendar datni un to saglabā tajā pašā mapē ar nosaukumu `grafiks.ics`, un aizver Google Chrome logu.

Pēc iCalendar datnes iegūšanas programmatūra, izmantojot `credentials.json` datni, veic autentifikāciju ar Google, izmantojot OAuth2 protokolu. Kad autentifikācija ir pabeigta, programmatūra nolasa `grafiks.ics` datni, pārveido datus no iCalendar formāta uz Google Calendar API nepieciešamā formāta datiem (līdzīgi JSON). Visbeidzot, lietotājam tiek pievienots jauns kalendārs, kura nosaukums ir pašreizējais laiks, un katrs kalendāra notikums (nodarbība) tiek pievienots jaunizveidotajam kalendāram. 

Pēc notikumu pievienošanas programmatūra beidz darbību ar paziņojumu "Pabeigts!".
## Izmantotās bibliotēkas
#### `selenium`
_Selenium_ ir vispārējs tīmekļa pārlūkprogrammatūras automatizācijas rīks. Šajā projektā tas tika izmantots, lai automatizētu procesu ielogoties ORTUSā, dotos uz nodarbību grafiku saturošo ORTUSa sadaļu un lai iegūtu katram ORTUS lietotājam unikālu hipersaiti, kas satur kalendāra datni.
#### `webdriver-manager`
_Webdriver Manager_ ir utilītbibliotēka, kas ļauj ērti instalēt _Selenium_ nepieciešamos _webdraiverus_, kurus izmanto tīmekļa pārlūkprogrammatūras kontrolēšanai. Šajā projektā tā tika izmantota, lai lietotājam atvieglotu programmatūras uzstādīšanas procesu (nav nepieciešams manuāli lejupielādēt _webdraiveri_ savai, konkrētajai Google Chrome versijai).
#### `requests`
_Requests_ ir bibliotēka, kas ļauj ērti veikt HTTP/1.1 pieprasījums. Ar šo bibliotēku tiek veikts pieprasījums uz `telpas2.rtu.lv` un veikta nepieciešamo nodarbību grafika kalendāra datnes lejupielāde. 
#### `ics`
_Ics_ ir iCalendar formāta datņu rediģēšanai un izveidošanai paredzēta bibliotēka. Šajā projektā tā tika izmantota, lai viegli no datnes `grafiks.ics` izgūtu nepieciešamo kalendāra notikumu apraksta, sākuma laika, beigu laika un vietas datus pārveidošanai uz Google Calendar API nepieciešamo formātu, kas nav saderīgs ar iCalendar formātu.
#### `google-auth-httplib2`, `google-auth-oauthlib` un `google-api-python-client`
Šīs trīs bibliotēkas nepieciešamas, lai savienotos un autentificētos ar Google Calendar API, un sūtītu pieprasījumus lietotājam izveidot jaunu kalendāru un tajā pievienot nodarbību grafika notikumus. 
### Iebūvētās bibliotēkas
#### `os`
Pārbaudei, vai kāda konkrēta datne ir jau izveidota.  

#### `tomllib`
Konfigurācijas datnes informācijas parsēšanai uz izmantojamām Python datu struktūrām.

#### `dataclasses`
`dataclass` tipa datu struktūras izveidei.

#### `datetime`
Kalendāra datnē esošas datumu un laika informācijas apstrādei pareizā formātā, kā arī pašreizējā sistēmas laika ieguvei.

## Programmatūras metožu apraksts
### `oks.py`
1. `main() -> None`: Galvenā metode.

### `config_parser.py`
1. `get_ortus_credentials() -> Credentials(identifier: str, password: str)`: Nolasa `config.toml` konfigurācijas datni un iegūst tur norādīto lietotājvārdu un paroli, atgriežot `Credentials` datu klasi, kas satur lietotājvārdu un paroli.
### `calendar_scraper.py`
1. `CalendarScraper.__init__(self) -> None`: Inicializācijas metode, kurā iegūst lietotāja ORTUSa lietotājvārdu un paroli, inicializē _Selenium_ un palaiž _webdraiveri_. 
2. `CalendarScraper.run(self)`: Izsauc metodes, kas veic darbības ORTUSa vietnē.
3. `CalendarScraper.login(self, username: str, password: str) -> None`: Automatizēti ielogojas ORTUSā ar sniegtajiem lietotāja kredenciāļiem.
4. `CalendarScraper.navigate_schedule_page(self) -> None`: Automatizēti dodas no ORTUSa sākumlapas uz _Grafiki_ apakšlapas.
5. `CalendarScraper.download_schedule_file(self) -> None`: Iegūst katram lietotājam unikālu grafika hipersaiti un veic nodarbību grafika iCalendar datnes lejupielādi.

### `calendar_sync.py`
1. `CalendarSync.__init__(self) -> None`: Inicializācijas metode, kas izsauc Google Calendar API piekļuves uzstādīšanas metodi `CalendarSync.build_api_service`.
2. `CalendarSync.build_api_service(self, credentials_path: str) -> None`: Izmantojot argumentā `credentials_path` norādīto `credentials.json` datnes atrašanās vietu, veic nepieciešamās darbības Google Calendar API autentifikācijas veikšanai un lietošanas uzstādīšanai.
3. `CalendarSync.ics_to_google_calendar_format(self) -> list`: No diska nolasa `grafiks.ics` datni un pārveido no iCalendar formāta uz Google Calendar API nepieciešamo kalendāra formātu. Atgriež sarakstu ar kalendāra notikumu datu struktūrām (_dictionary_ tipa).
4. `CalendarSync.sync_calendar(self) -> None`: Izveido jaunu tukšu kalendāru lietotāja Google Calendar sistēmā, kura nosaukums ir pašreizējais laiks, un pievieno tam katru pārveidoto nodarbību grafika notikumu.

## Licence
ORTUS kalendāra automātiskakatram ORTUS lietotājam unikālu hipersaiti, kas satur kalendāra datni.is sinhronizēšanas rīks ir licencēts zem [GNU Vispārējās publiskās licences 3. versijas](LICENSE).
