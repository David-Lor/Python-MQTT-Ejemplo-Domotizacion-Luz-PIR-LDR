# Ejemplo Python IoT MQTT - Control luz con PIR + LDR

Ejemplo de domotización de luz con control automático de encendido y apagado, controlado según movimiento y cantidad de luz presente en la habitación (sensores PIR y lumínico/LDR), comunicándose mediante MQTT, y controlado mediante un servicio Python.

Cuando el PIR detecta movimiento, Y la luminosidad de la habitación está por debajo de cierto nivel, la luz se enciende automáticamente. Cuando el PIR deja de detectar movimiento, se apaga automáticamente.

## Requirements

- Python >= 3.6
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- [dotenv-settings-handler](https://pypi.org/project/dotenv-settings-handler/)

## Topics

Definición de topics MQTT en este contexto:

- `habitacion/luz/cmd`: Comandos para controlar la luz: `ON`, `OFF`
- `habitacion/luz/stat`: Estado actual de la luz: `ON`, `OFF` (retained) (no utilizado)
- `habitacion/pir/stat`: Estado sensor de movimiento: `ON` cuando detecta movimiento, `OFF` cuando deja de detectarlo (lo mejor sería que sólo enviase ON y el tiempo de espera a decidir "no hay movimiento" fuese por código)
- `habitacion/ldr/stat`: Cantidad de luz detectada: porcentaje entre 0~100 enviado periódicamente (retained) (se da por hecho que el fotodiodo/LDR devuelve valores lineales)

## Settings

Se definen en archivo `.env`. Se cargan como variables de entorno utilizando [Dotenv Settings Handler](https://github.com/David-Lor/Python-DotEnv-Settings-Handler), cargándose en código a través de la clase `MySettings` instanciada.

`LC_LDR_THRESHOLD` define el porcentaje de luz máximo que hará que la luz de encienda automáticamente cuando el PIR detecte movimiento.

## light_controller.py

- Servicio de control de luz.
- Se suscribe a topics de stat de PIR (movimiento) y LDR (luz).
- Envía acciones ON/OFF al topic de la luz para encender/apagar la luz.
- Cuando el PIR envía ON Y el nivel de luz es MENOR que el umbral, ENCIENDE la luz.
- Cuando el PIR envía OFF, APAGA la luz (realmente, esta funcionalidad debería estar definida también por el servicio, con un temporizador, y el PIR enviar únicamente mensajes cada vez que detecta movimiento).

## simulator.py

- Simulador de dispositivos sensores (movimiento y luz).
- El usuario debe introducir:
  - `on` para enviar ON por el PIR (hay movimiento)
  - `off` para enviar OFF por el PIR (no hay movimiento)
  - Número (int/float) para enviar luminosidad LDR (entre 0 y 100)
