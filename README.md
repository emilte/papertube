# papertube
Alert system for app idea (Toiletpaper Tube). This project was made as a practise for state machine behaviour and mqtt communication.

In a course at NTNU, groups of students we were supposed to brainstorm a startup idea. My group came up with The Toiletpaper Tube.

Idea:
- Have a container for toiletpaper rolls in the bathroom.
- Connect an IR sensor to keep track of amount of paper left. This sensor sends a continuous stream of data to a sensor monitor.
- The sensor monitor checks the sensor state regularly. If the state has changed, it will notify another machine (Notification Controller)
- The notification controller will notify mqtt subscribers (like an app) that the bathroom is running low on toiletpaper.

We also wanted to have a GPS tracker, so that an app could notify only when the owner enters a grocery store. This project does not implement this though.

How:
1. Clone or download project
2. Run: pip install pipenv (python 3) in a terminal 
3. Run pipenv shell
4. Run the file: Launch_System
5. Connect as an MQTT client on http://www.hivemq.com/demos/websocket-client/ and subscribe to stmpy/alerts
6. Run the file: Simulated_IR_Sensor
