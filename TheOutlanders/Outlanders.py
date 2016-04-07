"""
The code is written for MAE415. 
Idea is to have different methods written for different sensors.
Calling the methods as and when needed and truely test.
"""

#Importing dependencies
import time
import grovepi
import os
import otlndrGPSClient
import sys


#Define the class
class Outlanders:
     
     #Initializer
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

        #GPS Session
        otlndrGPSClient.gpsp = otlndrGPSClient.GpsPoller()
        

    #Code for the calibration of gyro sensor
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
        

    #Read from the airquality sensor    
     def readAirQualitySensorData(self,sensorID):
        if sensorID==1:
            self.airQualitySensorValue=grovepi.analogRead(self.airQualitySensor1)
        elif sensorID ==2:
            self.airQualitySensorValue=grovepi.analogRead(self.airQualitySensor2)
        return self.airQualitySensorValue


    #Read from the Gyro sensor
     def readGyroSensorData(self):
        self.gyroSensorValue=grovepi.analogRead(self.gyroSensor)
        return self.gyroSensorValue

    #Module to write to file
     def csvWriteRow(self,row):
          try:
               with open("outlndrsData.txt", "ab") as f:
                    f.write(row)
          except:
               print "Write Error"
          
#create the class object as mission
mission=Outlanders()

#Time function
current_milli_time = lambda: int(round(time.time() * 1000))

#Calibrate Sensor
mission.gyroCalibrate()

#Start GPS Thread
otlndrGPSClient.gpsp.start()

#Do forever
while True:
    #Clear everything before starting up
    os.system('clear')

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
        latValue = otlndrGPSClient.gpsd.fix.latitude
        lonValue = otlndrGPSClient.gpsd.fix.longitude
        gpsTime  = otlndrGPSClient.gpsd.utc,' + ', otlndrGPSClient.gpsd.fix.time
        altValue = otlndrGPSClient.gpsd.fix.altitude
        epsValue = otlndrGPSClient.gpsd.fix.eps
        epxValue = otlndrGPSClient.gpsd.fix.epx
        epvValue = otlndrGPSClient.gpsd.fix.epv
        eptValue = otlndrGPSClient.gpsd.fix.ept 
        spdValue = otlndrGPSClient.gpsd.fix.speed
        clbValue = otlndrGPSClient.gpsd.fix.climb
        trkValue = otlndrGPSClient.gpsd.fix.track
        mdeValue = otlndrGPSClient.gpsd.fix.mode


        #Read time
        timeValue=current_milli_time()

        #make the string
        dataString=str(tempVal1)+","+str(tempVal2)+","+str(gyroValue)+","+str(gyroVelValue)+","+str(timeValue)+","+str(latValue)+","+str(lonValue)+","+str(gpsTime)+","+str(altValue)+","+str(epsValue)+","+str(epxValue)+","+str(epvValue)+","+str(eptValue)+","+str(spdValue)+","+str(clbValue)+","+str(trkValue)+","+str(mdeValue)+"\n"

        #write to the csv file
        mission.csvWriteRow(dataString)
        
        #Timer for making the thread sleep
        time.sleep(30)
    
    except IOError as thisException:
        print str(thisException)

    except (KeyboardInterrupt, SystemExit): 
        otlndrGPSClient.gpsp.running = False
        otlndrGPSClient.gpsp.join()
