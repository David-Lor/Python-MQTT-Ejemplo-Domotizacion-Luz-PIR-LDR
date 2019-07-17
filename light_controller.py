import paho.mqtt.client as mqtt
from settings import settings

ldr_value = 100  # Last LDR value received
light_stat = False  # Light Stat (as sent from here)


def turn_light(stat):
    """Switch ON/OFF the light"""
    global light_stat
    if stat:
        payload = "ON"
        light_stat = True
    else:
        payload = "OFF"
        light_stat = False
    client.publish(settings.light_cmd_topic, payload)
    print("Switched Light", payload)


def on_connect(*args):
    """Callback to execute when MQTT connects"""
    print("MQTT Connected!")
    client.subscribe(settings.ldr_topic)
    client.subscribe(settings.pir_topic)


def on_message(*args):
    """Callback to execute when MQTT receives new message"""
    global ldr_value
    msg: mqtt.MQTTMessage = next(a for a in args if isinstance(a, mqtt.MQTTMessage))
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Rx @ {topic}: {payload}")
    if topic == settings.ldr_topic:
        ldr_value = float(payload)
    elif topic == settings.pir_topic:
        if payload == "ON" and not light_stat and ldr_value <= settings.ldr_threshold:
            turn_light(True)
        elif payload == "OFF" and light_stat:
            turn_light(False)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == "__main__":
    client.connect(settings.broker, settings.port)
    
    try:
        client.loop_forever()
    except (KeyboardInterrupt, InterruptedError):
        pass
    
    print("Bye!")
