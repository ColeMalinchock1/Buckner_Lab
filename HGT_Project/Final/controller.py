# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from json_server import JSON_Server
import time
import math
from serial import Serial
import pyTMCL


class Controller:
    def __init__(self, gui, piMode, hxMode):

        # Reading if pi and hx711 are connected from main.py
        self.piMode = piMode
        self.hxMode = hxMode

        # Setting up the GUI
        self.main_win = QMainWindow()
        self.ui = gui
        self.ui.setupUi(self.main_win)

        # Importing libraries if modes are on
        if self.piMode:
            import RPi.GPIO as GPIO
        if self.hxMode:
            from hx711 import HX711
            
        # Setting up TMCL serial communication
        # Getting the motor address, default is 1
        MODULE_ADDRESS = 1

        # Getting the serial port
        serial_port = Serial("/dev/ttyACM0")

        # Connecting to the serial port
        bus = pyTMCL.connect(serial_port)

        # Creating the motor object that can be controlled
        self.motor = bus.get_motor(MODULE_ADDRESS)

        while True:
            try:
                # Setting axis parameters
                self.motor.set_axis_parameter(2, 20)
                self.motor.set_axis_parameter(5, 1000)
                self.motor.set_axis_parameter(6, 255)
                self.motor.set_axis_parameter(7, 110)
                self.motor.set_axis_parameter(214, 0)
                break
            except pyTMCL.reply.TrinamicException:
                print("Motor not on")

        self.motor.stop()

        # Creating check variable so it does not repeat the stop
        self.check = True

        # GPIO Pins
        self.increase_tension = 22 # Stop_R
        self.decrease_tension = 27 # Stop L
        self.slow_mode = 17 # AIN_0
        self.green_led = 25
        self.yellow_led = 24
        self.red_led = 23
        self.output_pins = [self.increase_tension , self.decrease_tension , self.slow_mode , self.green_led , self.red_led , self.yellow_led]

        if self.piMode:

            # Warnings at the startup
            GPIO.setwarnings(False)

            # Setting the GPIO mode to BCM (instead of BOARD)
            GPIO.setmode(GPIO.BCM)

            # Setting up all pins as OUT
            GPIO.setup(self.increase_tension , GPIO.OUT)
            GPIO.setup(self.decrease_tension , GPIO.OUT)
            GPIO.setup(self.slow_mode , GPIO.OUT)
            GPIO.setup(self.red_led , GPIO.OUT)
            GPIO.setup(self.green_led , GPIO.OUT)
            GPIO.setup(self.yellow_led , GPIO.OUT)
        
            # Default the output pins to low
            for i in self.output_pins:
                GPIO.output(i , GPIO.HIGH)  

        # Initializations for keypads
        self.decimal_1 = False
        self.maxPrecision_1 = False
        self.ui.setMarkTension.setHidden(True)
        self.ui.tooLargeLabelTension.setHidden(True)

        self.decimal_2 = False
        self.maxPrecision_2 = False
        self.ui.setMarkDelay.setHidden(True)
        self.ui.tooLargeLabelDelay.setHidden(True)

        self.decimal_3 = False
        self.maxPrecision_3 = False
        self.ui.setMarkSchedule1.setHidden(True)
        self.ui.tooLargeLabelSchedule1.setHidden(True)

        self.decimal_4 = False
        self.maxPrecision_4 = False
        self.ui.setMarkSchedule2.setHidden(True)
        self.ui.tooLargeLabelSchedule2.setHidden(True)

        # Initializations for hx711
        self.referenceUnit = -66090
    
        if self.hxMode:

            # Referencing pins
            self.hx = HX711(5 ,6)
            
            # ???
            self.hx.set_reading_format("MSB", "MSB")
            
            # Inputting reference unit
            self.hx.set_reference_unit(self.referenceUnit)
            
            # Zeroing the hx
            self.hx.reset()
            self.hx.tare()
            
        
        # Range of deadband and slow mode
        self.dead_band_range = 1.0
        self.slow_mode_range = 6.0

        # Schedule initialization
        self.scheduleOn = False
        
        # Arrays for tension history and scheduling
        self.timeArray = []
        self.timeArrayCounter = 0
        self.currentTensionArray = []
        self.setTensionArray = []
        self.last_time_array = time.time()

        # Time in between puts and gets to stay under the 5000 an hour limit
        self.wait_time = 4 # Seconds

        # Defaults to setTension widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.setTension)

        # Buttons for switching between windows
        self.ui.setTensionButton.clicked.connect(self.showSetTension)
        self.ui.setTimeDelayButton.clicked.connect(self.showSetTimeDelay)
        self.ui.setScheduleButton.clicked.connect(self.showSetSchedule1)
        self.ui.tensionHistoryButton.clicked.connect(self.showTensionHistory)

        # Connect up and down buttons to setweight
        self.setWeight = 0.00
        self.ui.tensionUp.clicked.connect(self.doTensionUp)
        self.ui.tensionDown.clicked.connect(self.doTensionDown)
        self.ui.setTensionLCD.display(self.setWeight)

        # Set Time Delay Variable
        self.setTimeDelay = 0.00
        self.ui.timeDelayLCD.display(self.setTimeDelay)
        self.last_time_delay = time.time()
        self.last_schedule_update = time.time()
        self.set_point_time = time.time()

        # Initializing count between each cycle for artificial weight
        self.count = 0

        # Artificial weight
        self.val = 0

        # MANUAL SET TENSION SCREEN #
        self.ui.keypad1.clicked.connect(lambda: self.manualSetTension(1))
        self.ui.keypad2.clicked.connect(lambda: self.manualSetTension(2))
        self.ui.keypad3.clicked.connect(lambda: self.manualSetTension(3))
        self.ui.keypad4.clicked.connect(lambda: self.manualSetTension(4))
        self.ui.keypad5.clicked.connect(lambda: self.manualSetTension(5))
        self.ui.keypad6.clicked.connect(lambda: self.manualSetTension(6))
        self.ui.keypad7.clicked.connect(lambda: self.manualSetTension(7))
        self.ui.keypad8.clicked.connect(lambda: self.manualSetTension(8))
        self.ui.keypad9.clicked.connect(lambda: self.manualSetTension(9))
        self.ui.keypad0.clicked.connect(lambda: self.manualSetTension(0))
        self.ui.keypadEnter.clicked.connect(lambda: self.manualSetTension(11))
        self.ui.keypadDecimal.clicked.connect(lambda: self.manualSetTension(12))
        self.ui.keypadClear_5.clicked.connect(lambda: self.manualSetTension(13))

        # MANUAL SET TIME DELAY SCREEN #
        self.ui.keypad1_2.clicked.connect(lambda: self.manualSetTimeDelay(1))
        self.ui.keypad2_2.clicked.connect(lambda: self.manualSetTimeDelay(2))
        self.ui.keypad3_2.clicked.connect(lambda: self.manualSetTimeDelay(3))
        self.ui.keypad4_2.clicked.connect(lambda: self.manualSetTimeDelay(4))
        self.ui.keypad5_2.clicked.connect(lambda: self.manualSetTimeDelay(5))
        self.ui.keypad6_2.clicked.connect(lambda: self.manualSetTimeDelay(6))
        self.ui.keypad7_2.clicked.connect(lambda: self.manualSetTimeDelay(7))
        self.ui.keypad8_2.clicked.connect(lambda: self.manualSetTimeDelay(8))
        self.ui.keypad9_2.clicked.connect(lambda: self.manualSetTimeDelay(9))
        self.ui.keypad0_2.clicked.connect(lambda: self.manualSetTimeDelay(0))
        self.ui.keypadEnter_2.clicked.connect(lambda: self.manualSetTimeDelay(11))
        self.ui.keypadDecimal_2.clicked.connect(lambda: self.manualSetTimeDelay(12))
        self.ui.keypadClear_6.clicked.connect(lambda: self.manualSetTimeDelay(13))

        # MANUAL SET SCHEDULE1 SCREEN #
        self.ui.keypad1_3.clicked.connect(lambda: self.manualSetSchedule1(1))
        self.ui.keypad2_3.clicked.connect(lambda: self.manualSetSchedule1(2))
        self.ui.keypad3_3.clicked.connect(lambda: self.manualSetSchedule1(3))
        self.ui.keypad4_3.clicked.connect(lambda: self.manualSetSchedule1(4))
        self.ui.keypad5_3.clicked.connect(lambda: self.manualSetSchedule1(5))
        self.ui.keypad6_3.clicked.connect(lambda: self.manualSetSchedule1(6))
        self.ui.keypad7_3.clicked.connect(lambda: self.manualSetSchedule1(7))
        self.ui.keypad8_3.clicked.connect(lambda: self.manualSetSchedule1(8))
        self.ui.keypad9_3.clicked.connect(lambda: self.manualSetSchedule1(9))
        self.ui.keypad0_3.clicked.connect(lambda: self.manualSetSchedule1(0))
        self.ui.keypadEnter_3.clicked.connect(lambda: self.manualSetSchedule1(11))
        self.ui.keypadDecimal_3.clicked.connect(lambda: self.manualSetSchedule1(12))
        self.ui.keypadClear_3.clicked.connect(lambda: self.manualSetSchedule1(13))

        # MANUAL SET SCHEDULE2 SCREEN #
        self.ui.keypad1_7.clicked.connect(lambda: self.manualSetSchedule2(1))
        self.ui.keypad2_7.clicked.connect(lambda: self.manualSetSchedule2(2))
        self.ui.keypad3_7.clicked.connect(lambda: self.manualSetSchedule2(3))
        self.ui.keypad4_7.clicked.connect(lambda: self.manualSetSchedule2(4))
        self.ui.keypad5_7.clicked.connect(lambda: self.manualSetSchedule2(5))
        self.ui.keypad6_7.clicked.connect(lambda: self.manualSetSchedule2(6))
        self.ui.keypad7_7.clicked.connect(lambda: self.manualSetSchedule2(7))
        self.ui.keypad8_7.clicked.connect(lambda: self.manualSetSchedule2(8))
        self.ui.keypad9_7.clicked.connect(lambda: self.manualSetSchedule2(9))
        self.ui.keypad0_7.clicked.connect(lambda: self.manualSetSchedule2(0))
        self.ui.keypadEnter_7.clicked.connect(lambda: self.manualSetSchedule2(11))
        self.ui.keypadDecimal_7.clicked.connect(lambda: self.manualSetSchedule2(12))
        self.ui.keypadClear_4.clicked.connect(lambda: self.manualSetSchedule2(13))

        # MANUAL SET SCHEDULE3 SCREEN #
        self.ui.buttonLinear.clicked.connect(lambda: self.manualSetSchedule3(1))
        self.ui.buttonSteps.clicked.connect(lambda: self.manualSetSchedule3(2))

    # Get the tension reading from the hx711 and display it on current weight LCD
    def updateWeight(self):
        if self.hxMode:
            self.current_tension = self.get_tension()
            print(self.current_tension)
        else: 
        # Artificial Tension
            self.count += 1
            self.current_tension = self.get_artificial_tension()

        # Only adding tension every 1 seconds to the tension array
        if time.time() - self.last_time_array > 1:
            self.currentTensionArray.append(self.current_tension)
            if not self.scheduleOn:
                self.setTensionArray.append(self.setWeight)
            self.last_time_array = time.time()

        if math.floor(self.current_tension) <= 0.0:
            self.ui.currentWeightLCD.display(0.00)
        else:
            self.ui.currentWeightLCD.display(self.current_tension)
        
    def updateSchedule(self):
        # If the setpoint is changing with the schedule, update the setWeight depending on how long since the start of schedule mode
        # And if it has been ~1 second since the last update
        if self.scheduleOn and time.time() - self.last_schedule_update > 1:

            # Find the time since the schedule started (seconds)
            timeSinceScheduleStart = int(time.time() - self.scheduleStartTime)

            # Changing the setpoint to the setpoint on the constructed array from setSchedule3 based on the time since started
            self.setWeight = self.setTensionArray[timeSinceScheduleStart]

            # The LCD display will change to display the set weight
            self.ui.setTensionLCD.display(self.setWeight)

            # Finding the time left on the schedule 
            timeScheduleLeft = self.setScheduleTime_Sec - timeSinceScheduleStart
            timeScheduleLeft_min = str(int((timeScheduleLeft // 60) % 60))
            timeScheduleLeft_hr = str(int(timeScheduleLeft // 3600))

            # Displaying the time left on the schedule
            self.ui.ScheduleTimeLCD.display(timeScheduleLeft_hr + ":" + timeScheduleLeft_min)

            # When the time on schedule is less than 1 second it turns off schedule mode
            if timeScheduleLeft < 1:
                self.scheduleOn = False
                self.scheduleMode = "Schedule Mode: Off"
                self.setTensionArray = []
                self.ui.labelScheduleMode.setText(self.scheduleMode)
                self.ui.graphWidget.clear()
            
            # Setting this as the last time the schedule has been updated
            self.set_schedule_update = time.time()

        # If schedule mode is off, the LCDs on the Schedule will display 0
        else:
            self.ui.ScheduleTimeLCD.display(0)
            self.ui.ScheduleSetpointLCD.display(0)

    ## Tension History Plotter Function ##
    def plot_chart(self):
        # Max size of currentTensionArray for no schedule
        max_size = 3600 # (~1 hour)
        self.ui.graphWidget.clear()
        # If tension setpoint
        if self.scheduleOn:

            self.ui.graphWidget.plot(range(int(self.setScheduleTime_Sec)) , self.setTensionArray)
            self.ui.graphWidget.plot(range(len(self.currentTensionArray)) , self.currentTensionArray , pen = (255 , 0 , 0))
        else:
            # If the length of the current tension array is greater than 3600 it deletes the first item in the list
            if len(self.currentTensionArray) > max_size:
                self.currentTensionArray.pop(0)
                self.setTensionArray.pop(0)

            self.ui.graphWidget.plot(range(len(self.currentTensionArray)) , self.setTensionArray)
            self.ui.graphWidget.plot(range(len(self.currentTensionArray)) , self.currentTensionArray , pen = (255 , 0 , 0))
            
            
        
    ## Set Tension Keypad Function ##
    def manualSetTension(self, pressed):

        # If enter button is pressed get the setWeight and display on setTensionLCD
        # If number entered is greater than 50 lb it needs to be re-entered
        if pressed == 11:
            if self.ui.manualSetTensionLCD.value() < 50:
                self.setWeight = self.ui.manualSetTensionLCD.value()
                self.ui.setTensionLCD.display(self.setWeight)
                self.ui.setMarkTension.setHidden(False)
                if self.scheduleOn:
                    self.setTensionArray = []
                    self.currentTensionArray = []
                    self.scheduleMode = "Schedule Mode: Off"  
                self.scheduleOn = False
                
            else:
                self.ui.tooLargeLabelTension.setHidden(False)
            self.ui.manualSetTensionLCD.display(0)
            self.maxPrecision_1 = False
            self.decimal_1 = False

        # If the clear button is pressed, the display goes back 0
        elif pressed == 13:
            self.ui.manualSetTensionLCD.display(0)
            self.ui.setMarkTension.setHidden(True)
            self.ui.tooLargeLabelTension.setHidden(True)

        # If the decimal number is pressed it puts a decimal down, but does not let you put more than one decimal down
        elif pressed == 12:
            if self.decimal_1 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTensionLCD.value()))+("."))
                    self.ui.manualSetTensionLCD.display(mstLCDstring)
                    self.decimal_1 = True
                    self.ui.setMarkTension.setHidden(True)
                    self.ui.tooLargeLabelTension.setHidden(True)

        # When any number is pressed it displays it on the LCD
        else:
            if (self.ui.manualSetTensionLCD.value() == 0) and (self.decimal_1 == False):
                self.ui.manualSetTensionLCD.display(pressed)
                self.ui.setMarkTension.setHidden(True)
                self.ui.tooLargeLabelTension.setHidden(True)
            else:
                if self.decimal_1 == False:
                    mstLCDstring = (str(int(self.ui.manualSetTensionLCD.value())))+(str(pressed))
                    self.ui.manualSetTensionLCD.display(float(mstLCDstring))
                    self.ui.setMarkTension.setHidden(True)
                    self.ui.tooLargeLabelTension.setHidden(True)
                else:
                    if self.maxPrecision_1 == False:
                        mstLCDstring = str(float(self.ui.manualSetTensionLCD.value()) + (0.1 * int(pressed)))
                        self.ui.manualSetTensionLCD.display(mstLCDstring)
                        self.maxPrecision_1 = True
                        self.ui.setMarkTension.setHidden(True)
                        self.ui.tooLargeLabelTension.setHidden(True)

    ## Schedule1 Keypad Function ##
    def manualSetSchedule1(self, pressed):
        if pressed == 11: # Enter
            if self.ui.manualSetSchedule1LCD.value() < 50:
                self.setScheduleWeight = self.ui.manualSetSchedule1LCD.value()
                self.ui.setMarkSchedule1.setHidden(False)
                self.ui.keypadEnter_3.setText("Next")
                self.ui.keypadEnter_3.clicked.connect(self.showSetSchedule2)
            else:
                self.ui.tooLargeLabelSchedule1.setHidden(False)
            self.maxPrecision_3 = False
            self.decimal_3 = False
            
        elif pressed == 13: # Clear
            self.ui.manualSetSchedule1LCD.display(0)
            self.ui.setMarkSchedule1.setHidden(True)
            self.ui.tooLargeLabelSchedule1.setHidden(True)
            
        elif pressed == 12: # Decimal
            if self.decimal_3 == False:
                    mstLCDstring = (str(int(self.ui.manualSetSchedule1LCD.value()))+("."))
                    self.ui.manualSetSchedule1LCD.display(mstLCDstring)
                    self.decimal_3 = True
                    self.ui.setMarkSchedule1.setHidden(True)
                    self.ui.tooLargeLabelSchedule1.setHidden(True)
                    
        else: # Any number
            if (self.ui.manualSetSchedule1LCD.value() == 0) and (self.decimal_3 == False):
                self.ui.manualSetSchedule1LCD.display(pressed)
                self.ui.setMarkSchedule1.setHidden(True)
                self.ui.tooLargeLabelSchedule1.setHidden(True)

            else:
                if self.decimal_3 == False:
                    mstLCDstring = (str(int(self.ui.manualSetSchedule1LCD.value())))+(str(pressed))
                    self.ui.manualSetSchedule1LCD.display(float(mstLCDstring))
                    self.ui.setMarkSchedule1.setHidden(True)
                    self.ui.tooLargeLabelSchedule1.setHidden(True)
                else:
                    if self.maxPrecision_3 == False:
                        mstLCDstring = str(float(self.ui.manualSetSchedule1LCD.value()) + (0.1 * int(pressed)))
                        self.ui.manualSetSchedule1LCD.display(mstLCDstring)
                        self.maxPrecision_3 = True
                        self.ui.setMarkSchedule1.setHidden(True)
                        self.ui.tooLargeLabelSchedule1.setHidden(True)

    ## Schedule2 Keypad Function ##
    def manualSetSchedule2(self, pressed):

        # Makes the button say enter again and clears the LCD for schedule1
        self.ui.keypadEnter_3.setText("Enter")
        self.ui.manualSetSchedule1LCD.display(0)

        if pressed == 11: # Enter
            if self.ui.manualSetSchedule2LCD.value() < 24 and self.ui.manualSetSchedule2LCD.value() > 0:
                self.setScheduleTime = self.ui.manualSetSchedule2LCD.value()
                self.ui.setMarkSchedule2.setHidden(False)
                self.ui.keypadEnter_7.setText("Next")
                self.ui.keypadEnter_7.clicked.connect(self.showSetSchedule3)
            else:
                self.ui.tooLargeLabelSchedule2.setHidden(False)
            self.maxPrecision_4 = False
            self.decimal_4 = False
            
        elif pressed == 13: # Clear
            self.ui.manualSetSchedule2LCD.display(0)
            self.ui.setMarkSchedule2.setHidden(True)
            self.ui.tooLargeLabelSchedule2.setHidden(True)
            
        elif pressed == 12: # Decimal
            if self.decimal_4 == False:
                    mstLCDstring = (str(int(self.ui.manualSetSchedule2LCD.value()))+("."))
                    self.ui.manualSetSchedule2LCD.display(mstLCDstring)
                    self.decimal_4 = True
                    self.ui.setMarkSchedule2.setHidden(True)
                    self.ui.tooLargeLabelSchedule2.setHidden(True)
                    
        else: # Any number
            if (self.ui.manualSetSchedule2LCD.value() == 0) and (self.decimal_4 == False):
                self.ui.manualSetSchedule2LCD.display(pressed)
                self.ui.setMarkSchedule2.setHidden(True)
                self.ui.tooLargeLabelSchedule2.setHidden(True)

            else:
                if self.decimal_4 == False:
                    mstLCDstring = (str(int(self.ui.manualSetSchedule2LCD.value())))+(str(pressed))
                    self.ui.manualSetSchedule2LCD.display(float(mstLCDstring))
                    self.ui.setMarkSchedule2.setHidden(True)
                    self.ui.tooLargeLabelSchedule2.setHidden(True)
                else:
                    if self.maxPrecision_4 == False:
                        mstLCDstring = str(float(self.ui.manualSetSchedule2LCD.value()) + (0.1 * int(pressed)))
                        self.ui.manualSetSchedule2LCD.display(mstLCDstring)
                        self.maxPrecision_4 = True
                        self.ui.setMarkSchedule2.setHidden(True)
                        self.ui.tooLargeLabelSchedule2.setHidden(True)

    ## Set Schedule Mode ##
    def manualSetSchedule3(self , pressed):

        # Returns the keypadEnter back to Enter and makes the LCD 0 again
        self.ui.keypadEnter_7.setText("Enter")
        self.ui.manualSetSchedule2LCD.display(0)

        # Converting the setScheduleTime from hours to seconds
        self.setScheduleTime_Sec = self.setScheduleTime * 3600

        # Initializing values for getting the tension
        startWeight = self.current_tension
        endWeight = self.setScheduleWeight
        self.setTensionArray = []
        self.currentTensionArray = []
        changeInWeight = endWeight - startWeight
        timeArray = range(int(self.setScheduleTime_Sec))

        # Modifiers to the step
        step_wait = 60 * 20 # Number of seconds to wait at each step (20 min)
        steps = 3 # Number of steps

        # Linear
        if pressed == 1:
            rate = changeInWeight/self.setScheduleTime_Sec
            for i in timeArray:
                self.setTensionArray.append(startWeight + rate * i)
            self.scheduleMode = "Schedule Mode: Linear"

        
        # Steps
        if pressed == 2:
            
            # Create a rate that still reaches the setpoint in the desired time with the desired steps
            rate = changeInWeight/(self.setScheduleTime_Sec - step_wait * (steps - 1))

            # Create an array with just the increasing tension
            for i in range(int(self.setScheduleTime_Sec - step_wait * (steps - 1))):
                self.setTensionArray.append(startWeight + rate * i)
                
            # Include in the array the stops where it holds tension for a given time
            for i in range(steps - 1):
                stop_spot = int(len(self.setTensionArray)/steps * (i + 1))
                stop_tension = self.setTensionArray[stop_spot]
                for j in range(step_wait):
                    self.setTensionArray.insert(stop_spot , stop_tension)
            self.scheduleMode = "Schedule Mode: Steps"

        
        # Boolean for if the setpoint is changing (ie. schedule mode) or if it is static
        self.scheduleOn = True

        # Initializing start time of schedule
        self.scheduleStartTime = time.time()

        # Changing label and setpoint
        self.ui.labelScheduleMode.setText(self.scheduleMode)
        self.ui.ScheduleSetpointLCD.display(self.setScheduleWeight)

        # Clearing the graph if it has anything on it
        self.ui.graphWidget.clear()
            
        # Changes the screen to the chart screen
        self.showTensionHistory()

    ## Set Time Delay Keypad Function##
    def manualSetTimeDelay(self, pressed):
        if pressed == 11: # Enter
            if self.ui.manualSetDelayLCD.value() < 600:
                self.setTimeDelay = self.ui.manualSetDelayLCD.value()
                self.ui.timeDelayLCD.display(self.setTimeDelay)
                self.ui.setMarkDelay.setHidden(False)
            else:
                self.ui.tooLargeLabelDelay.setHidden(False)
            self.ui.manualSetDelayLCD.display(0)
            self.maxPrecision_2 = False
            self.decimal_2 = False
            
        elif pressed == 13: # Clear
            self.ui.manualSetDelayLCD.display(0)
            self.ui.setMarkDelay.setHidden(True)
            self.ui.tooLargeLabelDelay.setHidden(True)
            
        elif pressed == 12: # Decimal
            if self.decimal_2 == False:
                    mstLCDstring = (str(int(self.ui.manualSetDelayLCD.value()))+("."))
                    #print (mstLCDstring)
                    self.ui.manualSetDelayLCD.display(mstLCDstring)
                    self.decimal_2 = True
                    self.ui.setMarkDelay.setHidden(True)
                    self.ui.tooLargeLabelDelay.setHidden(True)
                    
        else: # Any number
            if (self.ui.manualSetDelayLCD.value() == 0) and (self.decimal_2 == False):
                #print("value is 0 and decimal is false")
                self.ui.manualSetDelayLCD.display(pressed)
                #print("manual set time displayed")
                self.ui.setMarkDelay.setHidden(True)
                self.ui.tooLargeLabelDelay.setHidden(True)
                #print("setmarks hidden")
            else:
                if self.decimal_2 == False:
                    mstLCDstring = (str(int(self.ui.manualSetDelayLCD.value())))+(str(pressed))
                    #print (mstLCDstring)
                    self.ui.manualSetDelayLCD.display(float(mstLCDstring))
                    self.ui.setMarkDelay.setHidden(True)
                    self.ui.tooLargeLabelDelay.setHidden(True)
                else:
                    if self.maxPrecision_2 == False:
                        mstLCDstring = str(float(self.ui.manualSetDelayLCD.value()) + (0.1 * int(pressed)))
                        #print (mstLCDstring)
                        self.ui.manualSetDelayLCD.display(mstLCDstring)
                        self.maxPrecision_2 = True
                        self.ui.setMarkDelay.setHidden(True)
                        self.ui.tooLargeLabelDelay.setHidden(True)
        

    def doTensionUp(self):
        # Increasing tension by 1
        self.setWeight += 1.0
        self.ui.setTensionLCD.display(self.setWeight)
        

    def doTensionDown(self):
        # Decreasing tension by 1
        self.setWeight -= 1.0
        self.ui.setTensionLCD.display(self.setWeight)


		
    def show(self):
        self.main_win.show()

    def showSetTension(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setTension)

    def showSetTimeDelay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setTimeDelay)

    def showSetSchedule1(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setSchedule1)

    def showSetSchedule2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setSchedule2)

    def showSetSchedule3(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setSchedule3)

    def showTensionHistory(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.tensionHistory)




    def get_tension(self):
        # Getting tension from hx711
        val = self.hx.get_weight(5)

        return val
    
    def get_artificial_tension(self):
        # Getting artificial tension (absolute sin wave with a peak of 15)
        if self.count % 20 == 0:
            self.val = 15 * abs(math.sin(math.radians(self.count / 15)))

        return self.val

    # Controls is able to compare the current tension to the set point to see if it's within the dead band and within the slow mode range
    def controls(self):
        
        import RPi.GPIO as GPIO

        # Getting the most current tension
        self.current_tension = self.get_tension()

        # If the time is greater than or equal to the set pause period, it will continue the controls
        if time.time() - self.last_time_delay > self.setTimeDelay:
            
            # Finding the difference between the set point and current tension
            diff = self.setWeight - self.current_tension

            # Coefficient of speed
            k = 3

            # Setting the speed of the motor based on the distance to the setpoint
            velocity = abs(diff * k)

            # If the difference is negative and outside the dead band range, the tension is decreased
            if (diff + self.dead_band_range) < 0:
                self.motor.rotate_right(velocity)
                self.check = True
                GPIO.output(self.red_led, GPIO.HIGH)
                GPIO.output(self.green_led, GPIO.LOW)
                speed = str(velocity)
                turning_direction = "Decreasing Tension"

            # If the difference is positive and outside the dead band range, the tension is increased
            elif (diff - self.dead_band_range) > 0:
                self.motor.rotate_left(velocity)
                self.check = True
                GPIO.output(self.green_led, GPIO.HIGH)
                GPIO.output(self.red_led, GPIO.LOW)
                speed = str(velocity)
                turning_direction = "Increasing Tension"
            
            else:
                if self.check:
                    holding_current = 5 * self.current_tension
                    if holding_current > 255:
                        holding_current = 255
                    self.motor.set_axis_parameter(7, 5 * self.current_tension)
                    # self.motor.move_relative(-1234)
                    self.motor.stop()
                    self.check = False
                    print("Set point reached")
                speed = ""
                turning_direction = "Stopped"
                GPIO.output(self.green_led, GPIO.LOW)
                GPIO.output(self.red_led, GPIO.LOW)
                
                
        
        # If it is less than the delay, no adjustments are to be made
        else:
            turning_direction = "Stopped"
            speed = ""
            GPIO.output(self.green_led, GPIO.LOW)
            GPIO.output(self.red_led, GPIO.LOW)
            
        print(speed)
        print(turning_direction)
    
    def save_data(self):
        JSON_Server.save_json(self.current_tension, self.setWeight)
        JSON_Server.push_to_git()
