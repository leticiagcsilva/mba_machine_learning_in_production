import joblib
import numpy as np
import zmq
from minio import Minio
from minio.error import ResponseError



def make_predictions(X_test):
    # Carregar o modelo treinado do MinIO
    client = Minio('localhost:9000', access_key='minio',
                   secret_key='minio123', secure=False)
    try:
        client.fget_object('models', 'modelo.pkl', 'modelo.pkl')
    except ResponseError as err:
        print(err)

    # Carregar o modelo treinado
    model = joblib.load('modelo.pkl')

    # Fazer previsões usando o modelo carregado
    predicted_values = model.predict(X_test)

    # Retornar as previsões
    return predicted_values


# Inicialização do socket ZMQ
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

# Loop principal para receber e processar os dados de teste
while True:
    # Receber os dados de teste do nó de treinamento
    data = socket.recv_json()

    # Verificar se são dados de teste
    if 'X_test' in data:
        X_test = np.array(data['X_test'])

        # Fazer previsões usando o modelo salvo
        predicted_values = make_predictions(X_test)

        # Enviar as previsões de volta para o nó de treinamento
        socket.send_json(predicted_values.tolist())
