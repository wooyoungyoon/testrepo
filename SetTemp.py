#!/usr/bin/python3.7
from __future__ import division
import sys, os
sys.path.append('/home/pi/Desktop/TempScripts/')
import logging
#from logging.handlers import RotatingFileHandler
#from logging import handlers
import RPi.GPIO as GPIO # Import the GPIO library.
#import Adafruit_GPIO as platform
import Adafruit_GPIO.SPI as SPI
#import Adafruit_GPIO
import PCA9685 as PCA9685
import time             # Import time library
#import datetime
import MAX6675 as MAX6675


GPIO.setmode(GPIO.BCM)  
#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
CLK = 11     # BOARD: 23 (11)
CS  = 8     # BOARD: 24 (8)
DO  = 9     # BOARD: 21(9)
SPI_PORT   = 0
SPI_DEVICE = 0
sensor = MAX6675.MAX6675(CLK,CS,DO,spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

pwm = PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
time.sleep(1)

print("starting")

try:
  
        while True:
            temp = sensor.readTempC()          
           
            if temp< 83:
                dc = 3686 # 90% duty cycle (of 4096)   
                req_dc = 90
                time.sleep(1)
                
            elif temp >=83 and temp<84.75:
                dc = 2662 # 90% duty cycle (of 4096)   
                req_dc = 65
                time.sleep(1)
                
            elif temp >=84.75 and temp<85.5:
                dc = 819 # 10% duty cycle
                req_dc = 20
                time.sleep(1)

            else:
                dc = 0    # stop PWM
                req_dc = 0
                time.sleep(1)
            
            pwm.set_pwm(0, 0, dc)
            pwm.set_pwm(4, 0, dc)
            pwm.set_pwm(8, 0, dc)

                
            time.sleep(1)

            now = time.time()
            struck_now = time.localtime(now)
            print(time.strftime("%Y-%m-%d %H:%M:%S", struck_now), ("Duty: %s, Temp:%s" %(req_dc,temp)))

            time.sleep(1)

            
except KeyboardInterrupt:
        print("Ctl C pressed - ending program")
        dc = 0    # stop PWM
        req_dc = 0        
        pwm.stop()
        GPIO.cleanup()

    ##    f=open("temp1.log","w")
          
     
