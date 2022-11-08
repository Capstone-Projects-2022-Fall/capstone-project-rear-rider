# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)

class Lidar():
    def __init__(self) -> None:
        pass

    @staticmethod
    def getTFminiData():
        while True:
            #time.sleep(0.1)
            count = ser.in_waiting  # Count the number of bytes in the input buffer
            if count > 8:
                recv = ser.read(9)   # Read up to 9 bytes
                ser.reset_input_buffer() # Clear the buffer
                # type(recv[0]),  'int' in python3 
                
                if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                    distance = recv[2] + recv[3] * 256
                    strength = recv[4] + recv[5] * 256
                    # print("Distatnce: %3.2fm Signal Strength: %d"%((distance * 0.01), strength))
                    ser.reset_input_buffer()
                    return distance, strength

if __name__ == '__main__':
    lidar = Lidar()
    try:
        if ser.is_open == False:
            ser.open()
        print('%d %d'%lidar.getTFminiData())
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
