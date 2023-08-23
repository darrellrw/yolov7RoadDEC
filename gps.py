import requests
import serial

def getStatusWireless(status = "connection", ip = ""):
    try:
        lat = requests.get(f'http://{ip}/gps/lat')
        lng = requests.get(f'http://{ip}/gps/lng')
        date = requests.get(f'http://{ip}/gps/date')
        time = requests.get(f'http://{ip}/gps/time')

        if(lat.status_code == 200 and lng.status_code == 200 and date.status_code == 200 and time.status_code == 200):
            match status:
                case "connection":
                    return True
                case "lat":
                    return lat.content.decode()
                case "lng":
                    return lng.content.decode()
                case "date":
                    return date.content.decode()
                case "time":
                    return time.content.decode()
        else:
            match status:
                    case "connection":
                        return False
    except:
        return False

def getStatusWired(status = "connection", port = ""):
    try:
        ser = serial.Serial(port = port, baudrate = 115200, timeout = 100)
        if(ser):
            value = str(ser.readline().decode("UTF-8").strip())
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
                case "all":
                    return value
        else:
            match status:
                case "connection":
                    return False
        ser.close()
    except:
        return False