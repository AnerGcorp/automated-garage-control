import serial
import serial.tools.list_ports
import time

device = "/dev/ttyUSB0"

ports = serial.tools.list_ports.comports()
portList = []
for port in ports:
    portList.append(str(port.device))
    print(str(port.device))


def read_RFID(device):
    print("Connecting device...")
    dev = serial.Serial(device, 9600)

    try:
        print("Trying to connect ARDUINO")
    except:
        print("Failed to connect on ", device)
        exit()
    while True:
        try:
            data = dev.readline().decode("UTF")
            data = data[:-2]
            # data = str(data)
            # data = data[2:]
            # data = data[:-5]
            print(data == "177-231-117-29")
            time.sleep(0.3)
            dev.flushInput()
        except:
            print("Processing...")
            break


read_RFID(device)

# def cmd(serial):
#     serial.flushInput()
#     serial.flushOutput()
#     while True:
#         time.sleep(5)
#         try:
#             data = dev.readline()
#             print(data)

#         except:
#             print("Processing...")
#     return data

# cmd(serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=9600))
