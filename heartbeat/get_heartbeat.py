import serial
import time

def get_heartbeat(COM_port):
    ser = serial.Serial(COM_port, 115200, timeout=1) 

    time.sleep(2) 

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip() # Read a line, decode, and remove whitespace
                hb_parts = line.split(",")
                print(hb_parts[-1])
                

            time.sleep(0.1) # Small delay to prevent busy-waiting
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        ser.close() # Close the serial port when done
        print("Serial port closed.")