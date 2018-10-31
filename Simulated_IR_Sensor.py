from random import randint
from time import sleep
import paho.mqtt.client as mqtt

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "stmpy/simulated_ir"
client = mqtt.Client()
client.connect(BROKER, PORT)
client.loop_start()

# Container is full: 0
# Container is low: 1

def on_enter():
    global TOPIC
    print("Enter either 1 or 0 to simulate an IR sensor")
    while True:
        x = input("{} <-- ".format(TOPIC))
        client.publish(TOPIC, x)

def alternating(n=50, time=10):
    global TOPIC
    for i in range(n):
        value = i % 2
        print("{} --> {}".format(value, TOPIC))
        client.publish(TOPIC, value)
        sleep(time)

def random(time=10):
    global TOPIC
    while True:
        value = randint(0,1)
        print("{} --> {}".format(value, TOPIC))
        client.publish(TOPIC, value)
        sleep(time)

#alternating(n=200, time=10)
on_enter()
