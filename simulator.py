import paho.mqtt.client as mqtt
from settings import settings

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(settings.broker, settings.port)

    i = None
    while i != "EXIT":
        i: str = input("Commands: 'on' (PIR ON), number (LDR value), 'exit': ").strip().upper()
        
        try:
            inum = float(i)
            if inum >= 0 and inum <= 100:
                client.publish(settings.ldr_topic, i, retain=True)
                print("Published LDR value", i)
            else:
                print("Invalid LDR value, must be between 0~100")
        
        except ValueError:
            if i in ("ON", "OFF"):
                client.publish(settings.pir_topic, i)
                print("Published PIR", i)


    print("Bye!")
