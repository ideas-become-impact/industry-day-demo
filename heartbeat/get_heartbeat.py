import serial
import time

ser = serial.Serial('COM9', 115200, timeout=1) 

time.sleep(2) 

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip() # Read a line, decode, and remove whitespace
            print(f"{line}")
        time.sleep(0.1) # Small delay to prevent busy-waiting
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    ser.close() # Close the serial port when done
    print("Serial port closed.")