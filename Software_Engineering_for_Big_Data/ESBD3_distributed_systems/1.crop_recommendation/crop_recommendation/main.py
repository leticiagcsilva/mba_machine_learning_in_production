import json
import numpy as np
import pandas as pd
import zmq
from minio import Minio
from minio.error import ResponseError

# Dados de treinamento e teste
train_data = pd.read_csv('data.csv')
X_train = train_data.drop('target', axis=1)
y_train = train_data['target']
X_test = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])


context = zmq.Context()

train_socket = context.socket(zmq.PUSH)
train_socket.connect("tcp://localhost:5555")
train_socket.send_json(
    {'X_train': X_train.values.tolist(), 'y_train': y_train.tolist()})
best_params = train_socket.recv_json()
print("Melhores parâmetros recebidos:", best_params)


predict_socket = context.socket(zmq.PUSH)
predict_socket.connect("tcp://localhost:5556")
predict_socket.send_json({'X_test': X_test.tolist()})
predicted_values = predict_socket.recv_json()
print("Previsões recebidas:", predicted_values)

# Salvar as previsões no MinIO
minio_client = Minio('localhost:9000', access_key='minio123',
                     secret_key='minio', secure=False)
try:
    minio_client.put_object('entregavel',
                             'predictions.json',
                               json.dumps(predicted_values))
    print("Previsões salvas no MinIO.")
except ResponseError as err:
    print(err)
