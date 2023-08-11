import requests
import serial

class GPS:
    def __init__(self):
        self.ip = None
        self.lat = None
        self.lng = None
        self.date = None
        self.time = None
        self.ser = None

    def getConnectionWireless(self, ip):
        self.ip = ip
        try:
            self.lat = requests.get(f'http://{self.ip}/gps/lat')
            self.lng = requests.get(f'http://{self.ip}/gps/lng')
            self.date = requests.get(f'http://{self.ip}/gps/date')
            self.time = requests.get(f'http://{self.ip}/gps/time')

            if(self.lat.status_code == 200 and self.lng.status_code == 200 and self.date.status_code == 200 and self.time.status_code == 200):
                return "TrueConnected"
            else:
                return "FalseConnected"
        except:
            return "FalseNotConnected"

    def getStatusWireless(self, status):
        if(self.getConnectionWireless() == "TrueConnected"):
            match status:
                case "connection":
                    return True
                case "lat":
                    return self.lat.content.decode()
                case "lng":
                    return self.lng.content.decode()
                case "date":
                    return self.date.content.decode()
                case "time":
                    return self.time.content.decode()
        elif(self.getConnectionWireless() == "FalseConnected"):
            match status:
                case "connection":
                    return False
                case _:
                    return "Failed"
        else:
            return "Failed"
    
    def getConnectionWired(self, port):
        try:
            self.ser = serial.Serial(port = port, baudrate = 115200)
            return True
        except:
            return False
    
    def getStatusWired(self, status):
        if(self.getConnectionWired()):
            value = str(self.ser.readline(), "UTF-8")
            splitedValue = value.split()
            match status:
                case "connection":
                    return True
                case "lat":
                    return splitedValue[2]
                case "lng":
                    return splitedValue[3]
                case "date":
                    return splitedValue[0]
                case "time":
                    return splitedValue[1]
        else:
            match status:
                case "connection":
                    return False
                case _:
                    return "Failed"