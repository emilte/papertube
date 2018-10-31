import time
import paho.mqtt.client as mqtt
#import Simulated_IR_Sensor as S_IR

# initial transition
t0 = {'source':     'initial',
      'target':     'polling'}

# polling --> polling
t1 = {'trigger':    't',
        'source':   'polling',
        'target':   'polling'}


# the states:
polling = {'name':      'polling',
            'entry':    'checkSensor; start_myTimer(2)'}



DEFAULT_TRANSITIONS = [t0, t1]
DEFAULT_STATES = [polling]

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "stmpy/simulated_ir"


class Simulated_Sensor_Monitor():
    """Setup for a state machine that can monitor a connected IR sensor

    Attributes:
    name:
        the name of the object.
    transitions:
        a list of transitions for the state machine. Each transition is a dictionary.
    states:
        a list of states for the state machine. Each state is a dictionary.
    pin:
        the pin on the breadboard that the sensor is plugged into
    interval:
        number of seconds between each sensor reading

    """
    def on_message(self, client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))
        try:
            n = int(msg.payload)
            if n in [0,1]:
                self.sensor = n
        except:
            pass

    def __init__(self, name="simulated_sensor_monitor", interval=3):
        #print("Creating " + name )
        self.name = name
        self.stm = None
        self.interval = interval
        self.value = 0 # Oppdateres kun når vi sjekker sensor
        self.sensor = 0 # En flow av sensor updates
        self.buddies = []

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT)
        self.client.subscribe(TOPIC)
        self.client.loop_start()

    def checkSensor(self):
        s = "Checking sensor:"
        s += "\nvalue: " + str(self.value)
        s += "\nsensor: " + str(self.sensor)
        #print(s)
        if self.value != self.sensor:
            self.value = self.sensor
            if self.value == 0:
                self.signal_buddies("refilled")
            if self.value == 1:
                self.signal_buddies("low")

    def addBuddy(self, machine):
        #print("Adding buddy: " + machine.get_name())
        self.buddies.append(machine)

    def signal_buddies(self, msg):
        #print("Signaling buddies:")
        #print(self.buddies)
        for buddy in self.buddies:
            if buddy != None:
                buddy.getMachine().send_signal(msg)

    def getMachine(self):
        return self.stm

    def start_myTimer(self, seconds=7):
        timeout = 1000*seconds
        #print("Starting timer in {} ({} seconds)".format(self.name, timeout/1000))
        self.stm.start_timer('t', timeout)

    def setMachine(self, stm):
        #print("Setting stm: {} for {}".format(stm._id, self.name))
        self.stm = stm

    def get_name(self):
        return self.name
