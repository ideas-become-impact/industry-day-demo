import numpy as np
import matplotlib.pyplot as plt
import demo.get_heartbeat as get_heartbeat
import demo.model as model

rest_train, exercise_train, rest_output, exercise_output = [], [], [], []
W, b = None, None

def rest_button_clicked():
    '''
    add this to existing function
    '''
    train, output = get_heartbeat.get_heartbeat("COM6", 1)
    return train, output

def exercise_button_clicked():
    '''
    add this to existing function
    '''
    train, output = get_heartbeat.get_heartbeat("COM6", 2)
    return train, output

def collect_and_train():
    global rest_train, exercise_train, rest_output, exercise_output
    train = rest_train + exercise_train
    output = rest_output + exercise_output
    X = np.array(train) # 10+10 samples, each 29 features
    y = np.array(output) # 10+10 labels

    costs, W, b = model.train(X, y)

    return costs, W, b


while True:
    command = input("\nEnter command (stand / exercise / train / predict / quit): ").strip().lower()

    if command == "stand":
        rest_train, rest_output = rest_button_clicked()
        print("Collected standing data.")

    elif command == "exercise":
        exercise_train, exercise_output = exercise_button_clicked()
        print("Collected exercising data.")

    elif command == "train":
        _, W, b = collect_and_train()
        print("Training complete!")

    elif command == "predict":
        if W is None or b is None:
            print("⚠️ Please train the model first.")
            continue
        X_test = np.array(get_heartbeat.get_latest_heartbeat("COM6")).reshape(1, -1)
        y_pred = model.predict(X_test, W, b)
        state = 0 if y_pred[0,0] <= 0.5 else 1
        if state == 0:
            print("You are standing.")
        else:
            print("You are exercising.")

    elif command == "quit":
        print("Exiting program.")
        break

    else:
        print("Unknown command. Try again.")
