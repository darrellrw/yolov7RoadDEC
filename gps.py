import requests
import serial
import time

def getStatusWireless(status = "connection", ip = ""):
    try:
        lat = requests.get(f'http://{ip}/gps/lat')
        lng = requests.get(f'http://{ip}/gps/lng')
        date = requests.get(f'http://{ip}/gps/date')
        time = requests.get(f'http://{ip}/gps/time')

        status_dict = {
            "connection": True,
            "lat"       : lat.content.decode(),
            "lng"       : lng.content.decode(),
            "date"      : date.content.decode(),
            "time"      : time.content.decode(),
        }
        default_status = False
        return status_dict.get(status, default_status)

        # Tidak dapat dipakai di Python3 < 3.10
        # if(lat.status_code == 200 and lng.status_code == 200 and date.status_code == 200 and time.status_code == 200):
        #     match status:
        #         case "connection":
        #             return True
        #         case "lat":
        #             return lat.content.decode()
        #         case "lng":
        #             return lng.content.decode()
        #         case "date":
        #             return date.content.decode()
        #         case "time":
        #             return time.content.decode()
        # else:
        #     match status:
        #             case "connection":
        #                 return False
    except:
        return False

def getStatusWired(status = "connection", port = ""):
    try:
        ser = serial.Serial(port = port, baudrate = 115200, timeout = 1)
        time.sleep(3)
        if(ser):
            value = str(ser.readline().decode("UTF-8").strip())
            splitedValue = value.split()
            if (status == "connection"):
                return True
            elif (status == "lat"):
                ser.write(b"lat")
                return splitedValue[2]
            elif (status == "lng"):
                ser.write(b"lng")
                return splitedValue[3]
            elif (status == "date"):
                ser.write(b"date")
                return splitedValue[0]
            elif (status == "time"):
                ser.write(b"time")
                return splitedValue[1]
            else:
                return False
        else:
            match status:
                case "connection":
                    return False

        # Backup Code
        # ser = serial.Serial(port = port, baudrate = 115200, timeout = 100)
        # if (status == "connection"):
        #     return True
        # elif (status == "lat"):
        #     ser.write(b"lat")
        #     return str(ser.readline().decode("UTF-8"))
        # elif (status == "lng"):
        #     ser.write(b"lng")
        #     return str(ser.readline().decode("UTF-8"))
        # elif (status == "date"):
        #     ser.write(b"date")
        #     return str(ser.readline().decode("UTF-8"))
        # elif (status == "time"):
        #     ser.write(b"time")
        #     return str(ser.readline().decode("UTF-8"))
        # else:
        #     return False

        # Tidak dapat dipakai di Python3 < 3.10
        # if(ser):
        #     match status:
        #         case "connection":
        #             return True
        #         case "lat":
        #             ser.write(b"lat")
        #             return str(ser.readline().decode("UTF-8"))
        #         case "lng":
        #             ser.write(b"lng")
        #             return str(ser.readline().decode("UTF-8"))
        #         case "date":
        #             ser.write(b"date")
        #             return str(ser.readline().decode("UTF-8"))
        #         case "time":
        #             ser.write(b"time")
        #             return str(ser.readline().decode("UTF-8"))
        # else:
        #     match status:
        #         case "connection":
        #             return False
        # ser.close()
    except:
        return False

#Test
print(getStatusWired("date", "COM12"))