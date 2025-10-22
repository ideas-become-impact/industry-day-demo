import numpy as np
import matplotlib.pyplot as plt
import get_heartbeat
import model

def rest_button_clicked():
    '''
    add this to existing function
    '''
    train, output = get_heartbeat.get_heartbeat("COM4", 1)
    return train, output

def exercise_button_clicked():
    '''
    add this to existing function
    '''
    train, output = get_heartbeat.get_heartbeat("COM4", 2)
    return train, output

def collect_and_train():

    rest_train, rest_output = rest_button_clicked()
    exercise_train, exercise_output = exercise_button_clicked()
    train = rest_train + exercise_train
    output = rest_output + exercise_output
    X = np.array(train) # 10+10 samples, each 29 features
    y = np.array(output) # 10+10 labels

    costs, W, b = model.train(X, y)

    return costs, W, b

costs, W, b = collect_and_train()

# test prediction on a random array
X_test = np.array([472, 503, 491, 526, 459, 548, 512, 480, 499, 537, 455, 525, 467, 544, 510, 493, 482, 501, 529, 518, 460, 471, 523, 495, 509, 538, 486, 517, 504])
y_pred = model.predict(X_test, W, b)
state = 0 if y_pred[0,0] <= 0.5 else 1

print(state)


# #plot
# epochs = range(1, len(costs) + 1)
# plt.plot(epochs, costs)
# plt.xlabel("Epoch")
# plt.ylabel("Cost")
# plt.title("Cost vs. Epoch")
# plt.grid(True)
# plt.show()
