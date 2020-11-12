import RPi.GPIO as GPIO
import time

FAN_PIN = 17
ON_THRESHOLD = 50
OFF_THRESHOLD = 47
SLEEP_INTERVAL = 5

class Fan:
    running = False

    def on(self):
        GPIO.output(FAN_PIN, GPIO.HIGH)
        #print("ON")
        self.running = True

    def off(self):
        GPIO.output(FAN_PIN, GPIO.LOW)
        #print("OFF")
        self.running = False


def get_temp():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp_str = f.read()

    try:
        return int(temp_str) / 1000
    except (IndexError, ValueError,) as e:
        raise RuntimeError('Could not parse temperature output.')


if OFF_THRESHOLD >= ON_THRESHOLD:
    raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

fan = Fan()
fan.off()

while True:
    temp = get_temp()
    #print("temp {}, on_threshhold {}, fan_running {}".format(temp,ON_THRESHOLD,fan.running))

    if temp > ON_THRESHOLD and not fan.running:
        fan.on()

    elif fan.running and temp < OFF_THRESHOLD:
        fan.off()

    time.sleep(SLEEP_INTERVAL)
