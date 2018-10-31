from stmpy import Machine, Driver

driver = Driver()

# State machine to handle sensor data and notifying connected clients
import Notification_Controller as not_ctrl
notif_controller = not_ctrl.Notification_Controller(name = "notif_controller")
machine1 = Machine(
    name        = notif_controller.get_name(),
    transitions = not_ctrl.DEFAULT_TRANSITIONS,
    obj         = notif_controller,
    states      = not_ctrl.DEFAULT_STATES
)
notif_controller.setMachine(machine1)
driver.add_machine(machine1)

# State machine tweaked to monitor the simulated sensor (for testing)
import Simulated_Sensor_Monitor as sim_sens_mon
sim_sensor_monitor = sim_sens_mon.Simulated_Sensor_Monitor(name = "sim_sensor_monitor")
machine3 = Machine(
    name        = sim_sensor_monitor.get_name(),
    transitions = sim_sens_mon.DEFAULT_TRANSITIONS,
    obj         = sim_sensor_monitor,
    states      = sim_sens_mon.DEFAULT_STATES
)
sim_sensor_monitor.setMachine(machine3)
sim_sensor_monitor.addBuddy(notif_controller)
driver.add_machine(machine3)

driver.start()
