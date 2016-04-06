"""
The code is written for MAE415. 
Idea is to have different methods written for different sensors.
Calling the methods as and when needed and truely test.
"""

#Importing dependencies
import time
import csv
import grovepi
from gps import *
import os


#Define the class
class Outlanders:
     
     def __init__(self):
        """
        Define the sensors on the machine and the variables
        """
        #Sensor1: Air quality
        self.airQualitySensor1=0
        grovepi.pinMode(self.airQualitySensor1,"INPUT")

        #Sensor2: Air quality 2
        self.airQualitySensor2=1
        grovepi.pinMode(self.airQualitySensor2,"INPUT")
        
        #Sensor3: Gyro sensor
        self.gyroSensor=3
        grovepi.pinMode(self.gyroSensor,"INPUT")
        
     def gyroCalibrate(self):
        print "calibrating..."
        sum = 0
        errors = 0
        for x in range(0, 100):
            try:
                # Get sensor value
                v = grovepi.analogRead(self.gyroSensor)
                sum += v
                time.sleep(.05)
            except IOError:
                print "Error"
                errors += 1

        if errors == 100:
            print "unable to calibrate"
        
        self.reference_value = sum / (100 - errors)

        print "finished calibrating"
        print "reference_value =", self.reference_value
        
     def readAirQualitySensorData(self,sensorID):
        if sensorID==1:
            self.airQualitySensorValue=grovepi.analogRead(self.airQualitySensor1)
        elif sensorID ==2:
            self.airQualitySensorValue=grovepi.analogRead(self.airQualitySensor2)
        return self.airQualitySensorValue

     def readGyroSensorData(self):
          self.gyroSensorValue=grovepi.analogRead(self.gyroSensor)
          return self.gyroSensorValue
        

#create the class object as mission
mission=Outlanders()

#Calibrate Sensor
mission.gyroCalibrate()

#Do forever
while True:
    #Task1: Read sensor values
    try:
        #clear the system variables
        os.system('clear')
    
        #read the grovePi air quality sensor1
        tempVal1=mission.readAirQualitySensorData(1)
        
        #read grovepi air quality senor2
        tempVal2=mission.readAirQualitySensorData(2)
        
        #read from the gyro sensor
        gyroValue=mission.readGyroSensorData()
        gyroVelValue=((float)(gyroValue - mission.reference_value) * 4930.0) / 1023.0 / 0.67
        
        #read gps

        #make the string
        dataString=str(tempVal1)+","+str(tempVal2)+","+str(gyroValue)+","+str(gyroVelValue)

        #write to the csv file
        print dataString
        
        time.sleep(5)
    except IOError as thisException:
        print str(thisException)
    
    #Task2: write the sensor values
