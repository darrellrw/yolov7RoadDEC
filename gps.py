import requests
import serial
import time

class Wireless:
    def __init__(self, ip):
        self.ip = ip

    def getStatusWireless(self, status = "connection"):
        try:
            lat = requests.get(f'http://{self.ip}/gps/lat')
            lng = requests.get(f'http://{self.ip}/gps/lng')
            date = requests.get(f'http://{self.ip}/gps/date')
            time = requests.get(f'http://{self.ip}/gps/time')

            status_dict = {
                "connection": True,
                "lat"       : lat.content.decode(),
                "lng"       : lng.content.decode(),
                "date"      : date.content.decode(),
                "time"      : time.content.decode(),
            }
            default_status = False
            return status_dict.get(status, default_status)
        except:
            return False

class Wired:
    def __init__(self, port = "/dev/ttyUSB0", baud = "9600"):
        self.ser = serial.Serial(port = port, baudrate = baud, timeout = 1)

    def getStatusWired(self, status = "connection"):
        try:
            if(self.ser):
                value = str(self.ser.readline().decode("UTF-8").strip())
                splitedValue = value.split()
                if (status == "connection"):
                    return True
                elif (status == "lat"):
                    return splitedValue[2]
                elif (status == "lng"):
                    return splitedValue[3]
                elif (status == "date"):
                    return splitedValue[0]
                elif (status == "time"):
                    return splitedValue[1]
                else:
                    return False
            else:
                return False
        except:
            return False

#Test
# ggps = GPS("COM3", "9600")
# print(ggps.getStatusWired("connection"))
# print(ggps.getStatusWired("lat"))