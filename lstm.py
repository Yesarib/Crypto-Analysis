import datetime


import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional
from tensorflow.keras.optimizers import Adam
from binance_api import get_binance_api


data = get_binance_api()

max_price = float(max([item["close"] for item in data]))
max_volume = float(max([item["volume"] for item in data]))

data_normalized = [(float(item["close"]) / max_price, float(item["volume"]) / max_volume) for item in data]

X = []
y = []
for i in range(len(data_normalized) - 10):
    X.append([data_normalized[i+j] for j in range(10)])
    y.append(data_normalized[i+10][0])

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(LSTM(64, activation='relu', input_shape=(8, 2), return_sequences=True))
model.add(LSTM(64, activation='relu', return_sequences=True))
model.add(LSTM(64, activation='relu', return_sequences=True))
model.add(Bidirectional(LSTM(64, activation='relu', return_sequences=False)))
model.add(Dense(1))

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

model.fit(X_train, y_train, epochs= 100, verbose=1)

loss = model.evaluate(X_test, y_test)

print(f"Loss: {loss}")

last_10_data = np.array([data_normalized[-10:]])
prediction = model.predict(last_10_data, batch_size=1)

predicted_price = prediction[0][0] * max_price

timestamp = int(data[-1]["timestamp"]) // 1000
predicted_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

print("Predicted Price: ", predicted_price)
print("Predicted Date:", predicted_date)