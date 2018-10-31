from stmpy import Driver
import time
import paho.mqtt.client as mqtt

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "stmpy/alerts"


# initial transition
t0 = {'source':     'initial',
      'target':     'idle'}

#default:
# idle --> notification
c1 = {'trigger':    'low',
        'source':   'idle',
        'target':   'notification'}
# notification --> idle
c2 = {'trigger':    'refilled',
        'source':   'notification',
        'target':   'idle'}

DEFAULT_TRANSITIONS = [t0, c1, c2]

# transitions for spam_filter:
# idle --> spam_filter
c3 = {'trigger':    'low',
        'source':   'idle',
        'target':   'spam_filter'}
# spam_filter --> idle
c4 = {'trigger':    'refilled',
        'source':   'spam_filter',
        'target':   'idle'}
# spam_filter --> notification
c5 = {'trigger':    't',
        'source':   'spam_filter',
        'target':   'notification'}
# notification --> idle
c6 = {'trigger':    'refilled',
        'source':   'notification',
        'target':   'idle'}

FILTER_TRANSITIONS = [t0, c3, c4, c5, c6]


# the states:
idle = {'name':     'idle',
        'entry':    'set_led("off")'}

spam_filter = {'name':      'spam_filter',
                'entry':    'start_myTimer',
                'exit':     'stop_timer'}

notification = {'name':     'notification',
                'entry':    'set_led("on"); alert_subscribers'}

DEFAULT_STATES = [idle, notification]
FILTER_STATES = [idle, spam_filter, notification]

class Notification_Controller():

    def __init__(self, name="notification_controller"):
        #print("Creating " + name )
        self.name = name
        self.led = "off"
        self.stm = None

        self.client = mqtt.Client()
        self.client.connect(BROKER, PORT)
        self.client.loop_start()

    def set_led(self, state):
        print("LED: " + state)
        self.led = state

    def get_led(self):
        return self.led

    def alert_subscribers(self):
        # NOT FINISHED
        # Publish to topic
        # project/sensor_id/"something"
        # print("Alerting users")
        self.client.publish(TOPIC, "Paper tube almost empty!")

    def get_name(self):
        return self.name

    def setMachine(self, stm):
        #print("Setting stm: {} for {}".format(stm._id, self.name))
        self.stm = stm

    def getMachine(self):
        return self.stm

    # Functions for machine with spam_filter
    def start_myTimer(self, minutes):
        #print("Starting timer in {} ({} minutes)".format(self.name, 1000*60*minutes))
        self.stm.start_timer('t', 1000*60*minutes)

    def stop_timer(self):
        return
        #print("Stopping timer in " + self.name)
        #self.stm.stop_timer('t')
