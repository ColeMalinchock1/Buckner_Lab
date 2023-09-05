#! /usr/bin/python3

import time
import sys
import RPi.GPIO as GPIO
import curses

# Initializations
EMULATE_HX711=False
set_point = 8.0
dead_band_range = 1.0
slow_mode_range = 5.0
increase_tension = 22
decrease_tension = 27
slow_mode = 17
output_pins = [increase_tension , decrease_tension , slow_mode]
referenceUnit = -66090
stdscr = curses.initscr()

def main(hx):
    global set_point , dead_band_range
    GPIO.setup(increase_tension , GPIO.OUT)
    GPIO.setup(decrease_tension , GPIO.OUT)
    GPIO.setup(slow_mode , GPIO.OUT)

    # Default the output_pins to low
    for i in output_pins:
        GPIO.output(i , GPIO.LOW)

    while True:
        current_tension = get_tension(hx)
        turning_direction , speed = controller(current_tension)

        stdscr.refresh()
        stdscr.addstr(1 , 5 , 'Set Point: %s           ' % str(set_point))
        stdscr.addstr(2 , 5 , 'Current Tension: %.2f           ' % current_tension)
        stdscr.addstr(3 , 5 , 'Turning Condition: %s           ' % turning_direction)
        stdscr.addstr(4 , 5 , 'Speed: %s           ' % speed)

def get_tension(hx):
    try:
        
        val = hx.get_weight(5)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        return val

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
    

def setup():

    if not EMULATE_HX711:
        from hx711 import HX711
    else:
        from emulated_hx711 import HX711

    hx = HX711(5, 6)

    hx.set_reading_format("MSB", "MSB")

    hx.set_reference_unit(referenceUnit)

    hx.reset()

    hx.tare()
    
    return hx

def cleanAndExit():

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    sys.exit()

# Controller is able to compare the current tension to the set point to see if it's within the dead band and within the slow mode range
def controller(current_tension):
    global set_point , dead_band_range

    # If the current tension is below the dead band the tension is increased
    if set_point - dead_band_range > current_tension:

        # If the current tension is below the slow mode range the speed is fast
        if set_point - slow_mode_range > current_tension:
            GPIO.output(slow_mode , GPIO.LOW)
            speed = "Fast"
        else:
            GPIO.output(slow_mode , GPIO.HIGH)
            speed = "Slow"
        GPIO.output(increase_tension , GPIO.HIGH)
        GPIO.output(decrease_tension , GPIO.LOW)
        turning_direction = "Increasing Tension"
    
    # If the current tension is above the dead band the tension is decreased
    elif set_point + dead_band_range < current_tension:

        # If the current tension is above the slow mode range the speed is fast
        if set_point + slow_mode_range < current_tension:
            GPIO.output(slow_mode , GPIO.LOW)
            speed = "Fast"
        else:
            GPIO.output(slow_mode , GPIO.HIGH)
            speed = "Slow"
        GPIO.output(decrease_tension , GPIO.HIGH)
        GPIO.output(increase_tension , GPIO.LOW)
        turning_direction = "Decreasing Tension"
    
    else:
        speed = ""
        turning_direction = "Stopped"
        for i in output_pins:
            GPIO.output(i , GPIO.LOW)
    
    return turning_direction , speed



if __name__ == '__main__':
    hx = setup()
    main(hx)
