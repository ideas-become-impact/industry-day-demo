import serial
import time

def initialize_data_holding_dict() -> dict:
    data_holding_dict = {
        "train": [],
        "output": [],
        "start": 0.0,
        "state": {
            "list_full": False,
            "filled": False
        }
    }

    return data_holding_dict

def get_heartbeat(ser: serial.Serial, data_holding_dict: dict, button_clicked: int):

    # train: list[list[int]] = []
    # output = []
    time.sleep(1) 

    # create a new train set (array) every 3 seconds
    if not data_holding_dict["train"]:
        data_holding_dict["start"] = time.time()
        data_holding_dict["train"].append([])

    interval = 3

    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip() # Read a line, decode, and remove whitespace
            hb_parts = line.split(",") # ["512", "530", ...]
            print(hb_parts[-1]) # "512"
            data_holding_dict["train"][-1].append(int(hb_parts[-1]))
            if (len(data_holding_dict["train"][-1]) == 29):
                data_holding_dict["state"]["list_full"] = True
            time.sleep(0.1)
        

            if data_holding_dict["state"]["list_full"]:
                data_holding_dict["train"].append([])
        # while count <= 11:
        #     if ser.in_waiting > 0:
        #         line = ser.readline().decode('utf-8').strip() # Read a line, decode, and remove whitespace
        #         hb_parts = line.split(",") # ["512", "530", ...]
        #         print(hb_parts[-1]) # "512"
        #         train[-1].append(int(hb_parts[-1]))  
        #     time.sleep(0.1) # Small delay to prevent busy-waiting

            if time.time() - data_holding_dict["start"] >= interval:
                data_holding_dict["train"].append([])
                data_holding_dict["start"] = time.time()

    except KeyboardInterrupt:
        print("Program terminated by user.")
    # finally:
    #     ser.close() # Close the serial port when done
    #     print("Serial port closed.")

    # if (len(data_holding_dict["train"]) == 10 and len(data_holding_dict["train"][0]) == 29):
        # data_holding_dict["train"] = data_holding_dict["train"][1:-2]
        # for i in range(len(data_holding_dict["train"])): # cut lengths until 29
        #     data_holding_dict["train"][i] = data_holding_dict["train"][i][:29]
    if len(data_holding_dict["train"]) == 10:
        data_holding_dict["state"]["filled"] = True
        for i in range(len(data_holding_dict["train"])):
            if (i + 1 > len(data_holding_dict["train"])):
                data_holding_dict["train"][i] = []
            else:
                data_holding_dict["train"][i] = data_holding_dict["train"][i+1]

    # ideally make button_clicked an int/bool, depends on what's easier to get from frontend
    if button_clicked == 1: #resting clicked
        data_holding_dict["output"].extend([0] * 10)
    if button_clicked == 2: #exercising clicked
        data_holding_dict["output"].extend([1] * 10)

    return data_holding_dict

def get_latest_heartbeat(ser: serial.Serial, span: int = 29, *times):
    "Get the latest 29 heartbeat data from serial port for testing purpose, return array of ints"
    if (len(times) > 0):
        time.sleep(times[0])
    heartbeat_data = []
    try:
        while len(heartbeat_data) < span:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                hb_parts = line.split(",")
                heartbeat_data.append(int(hb_parts[-1]))
                if (len(times) > 1):
                    time.sleep(times[1])
        return heartbeat_data
    except KeyboardInterrupt:
        print("Program terminated by user.")
    
    return heartbeat_data

# def get_last_sec_heartbeat(ser: serial.Serial):
#     "Get the heartbeat data from last second, return array of reading and time elapsed"
#     heartbeat_data = []
#     try:
#         while len(heartbeat_data) < 20: # 20 most recent reading
#             if ser.in_waiting > 0:
#                 line = ser.readline().decode('utf-8').strip()
#                 hb_parts = line.split(",")
#                 heartbeat_data.append(int(hb_parts[-1]))
#             time.sleep(0.05)
#         return heartbeat_data
#     except KeyboardInterrupt:
#         print("Program terminated by user.")
    
#     return heartbeat_data