# line_follower.py
# by: Carl Strömberg

# Import the EV3-robot library
import ev3dev.ev3 as ev3
from time import sleep


class LineFollower:
    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

    # Main method
    def run(self):

        # sensors
        cs = ev3.ColorSensor();      assert cs.connected  # measures light intensity
        us = ev3.UltrasonicSensor(); assert us.connected

        cs.mode = 'COL-REFLECT'  # measure light intensity

        # motors
        lm = ev3.LargeMotor('outB');  assert lm.connected  # left motor
        rm = ev3.LargeMotor('outC');  assert rm.connected  # right motor

        speed = 360/4  # deg/sec, [-1000, 1000]
        dt = 500       # milliseconds
        stop_action = "coast"

        # PID tuning
        Kp = 1  # proportional gain
        Ki = 0  # integral gain
        Kd = 0  # derivative gain

        integral = 0
        previous_error = 0

        # initial measurment
        target_value = cs.value()

        # Start the main loop
        while not self.shut_down:

            # Calculate steering using PID algorithm
            print("CS " + str(cs.value()))
            print("US " + str(us.value()))

            if cs.value() == 0:
                  rm.run_forever(speed_sp = 0)
                  lm.run_forever(speed_sp = 0)
                  self.shut_down = True
                  """elif target_value < (cs.value() - 4):
                        lm.run_forever(speed_sp = 30)
                        rm.run_forever(speed_sp = -30)
                  elif target_value < (cs.value() - 2):
                        lm.run_forever(speed_sp = -60)
                        rm.run_forever(speed_sp = -80)"""
            elif us.value() < 200:
                  lm.run_forever(speed_sp = 32)
                  rm.run_forever(speed_sp = -32)
                  sleep(4)
                  if us.value() < 200:
                        lm.run_forever(speed_sp = 32)
                        rm.run_forever(speed_sp = -32)
                        sleep(8)
            elif us.value() > 400:
                  lm.run_forever(speed_sp = -600)
                  rm.run_forever(speed_sp = -600)
            else:
                  lm.run_forever(speed_sp = -100)
                  rm.run_forever(speed_sp = -100)

# Main function
if __name__ == "__main__":
    robot = LineFollower()
    robot.run()
