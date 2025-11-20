import numpy as np
import matplotlib.pyplot as plt
import heartbeat.get_heartbeat
import heartbeat.model


def rest_button_clicked(ser, training_dict):
    """
    add this to existing function
    """
    training_dict = heartbeat.get_heartbeat.get_heartbeat(ser, training_dict, 1)
    return training_dict


def exercise_button_clicked(ser, training_dict):
    """
    add this to existing function
    """
    training_dict = heartbeat.get_heartbeat.get_heartbeat(ser, training_dict, 2)
    return training_dict


def collect_and_train(ser, stand_dataset, exercise_dataset):
    rest_dict = rest_button_clicked(ser, stand_dataset)
    exercise_dict = exercise_button_clicked(ser, exercise_dataset)
    rest_train = rest_dict["train"]
    rest_output = rest_dict["output"]
    exercise_train = exercise_dict["train"]
    exercise_output = exercise_dict["output"]

    train = sum(rest_train, []) + sum(exercise_train, [])
    output = rest_output + exercise_output
    print(train)
    print(output)

    X = np.array(train)  # 10+10 samples, each 29 features
    y = np.array(output)  # 10+10 labels

    costs, W, b = heartbeat.model.train(X, y)

    return costs, W, b


# costs, W, b = collect_and_train()
# print(W)
# print(b)

# # test prediction on a random array
# X_test = np.array(get_heartbeat.get_latest_heartbeat('COM4'))
# y_pred = model.predict(X_test, W, b)
# state = 0 if y_pred[0,0] <= 0.5 else 1

# print(state)


# #plot
# epochs = range(1, len(costs) + 1)
# plt.plot(epochs, costs)
# plt.xlabel("Epoch")
# plt.ylabel("Cost")
# plt.title("Cost vs. Epoch")
# plt.grid(True)
# plt.show()
