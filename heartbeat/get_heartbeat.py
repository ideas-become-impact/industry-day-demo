import serial
import time

def get_heartbeat(COM_port, button_clicked):
    train = []
    output = []

    ser = serial.Serial(COM_port, 115200, timeout=1) 
    time.sleep(1) 

    # create a new train set (array) every 3 seconds
    start = time.time()
    count = 0
    interval = 3
    train.append([])

    try:
        while count <= 11:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip() # Read a line, decode, and remove whitespace
                hb_parts = line.split(",")
                print(hb_parts[-1])
                train[-1].append(int(hb_parts[-1]))   
            time.sleep(0.1) # Small delay to prevent busy-waiting

            if time.time() - start >= interval * (count + 1):
                train.append([])
                count += 1

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        ser.close() # Close the serial port when done
        print("Serial port closed.")

    train = train[1:-2]
    for i in range(len(train)):
        train[i] = train[i][:29] 

    # ideally make button_clicked an int/bool, depends on what's easier to get from frontend
    if button_clicked == 1: #resting clicked
        output.extend([0] * 10)
    if button_clicked == 2: #exercising clicked
        output.extend([0] * 10)

    return train, output

