### kamerki

ssh
```bash
ssh mebaya@192.168.8.80

```

run
```bash
docker compose up -d --build
```

### wymagania:
* instalacja `docker compose` na rbpi: https://docs.docker.com/engine/install/raspberry-pi-os/
* zdefiniowanie dostępu do kamer poprzez opcje [tutaj](https://github.com/mebaya/frigate/blob/6c2e83b3a48aeb78f303a7b8a9584d96e8c9e7bb/config/config.yml#L12)
* MQTT: mosquitto server (lokalnie) trzeba stworzyć topic i dodać użytkownika o takiej konfiguracji jak w `config.yml` Lub wykorzystać to co jest w: https://github.com/mebaya/frigate/tree/dev/mqtt_build trzeba podmienić konfig i ew. zmienić ip i wtedy wszystko powinno działać. Napisałem skrypt który instaluje mosquitto-client i przerzuca configi: https://github.com/mebaya/frigate/blob/dev/mqtt.setup.sh
* postgres (zdalnie)
* minio (zdalnie) trzeba skonfigurować zgodnie z  https://github.com/mebaya/frigate/blob/dev/frigate/mebaya/settings.py
* podgląd zdarzeń: https://github.com/mebaya/SolidSecurityView

### struktura
* config: [`config.yml`](https://github.com/mebaya/frigate/blob/dev/config/config.yml`)
* zapis zdarzeń do SQL: https://github.com/mebaya/frigate/blob/6c2e83b3a48aeb78f303a7b8a9584d96e8c9e7bb/frigate/events/maintainer.py#L289
* zapis plików do MinioDB: https://github.com/mebaya/frigate/blob/6c2e83b3a48aeb78f303a7b8a9584d96e8c9e7bb/frigate/record/maintainer.py#L401
* katalog z dodatkowym kodem który stworzyłem aby wysyłać zdalnie eventy i przesyłać nagrania (postgres i miniodb) https://github.com/mebaya/frigate/tree/dev/frigate/mebaya konfiguracja jest tutaj: https://github.com/mebaya/frigate/blob/dev/frigate/mebaya/settings.py

### debugowanie
- nie widać kamer - kolejność interfaców sieciowych ma znaczenie ten przez który idą kamerki musi być pierwszy w konfiguracji
- 
