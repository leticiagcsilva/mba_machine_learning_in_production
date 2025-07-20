import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
import pandas as pd
import zmq

# Carregar os dados de treinamento do arquivo CSV
train_data = pd.read_csv('data.csv')

# Separar os recursos (X_train) e o alvo (y_train)
X_train = train_data.drop('target', axis=1)
y_train = train_data['target']

# Definindo os hiperparâmetros a serem testados
param_grid = {
    'class_weight': ['balanced', None],
    'C': np.logspace(-4, 0, 4),
    'penalty': ['l1', 'l2']
}

LogReg = LogisticRegression(random_state=2)

grid_search = GridSearchCV(LogReg, param_grid, cv=10)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
print("Melhores parâmetros:", best_params)

# Função para fazer previsões usando os melhores parâmetros encontrados

def make_predictions(X_train, y_train, X_test, best_params):
    best_model = LogisticRegression(**best_params, random_state=2)
    best_model.fit(X_train, y_train)
    predicted_values = best_model.predict(X_test)
    return predicted_values


# Inicialização do socket ZMQ
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

# Loop principal para receber e processar os dados
while True:
    # Receber os dados do mestre
    data = socket.recv_json()

    # Verificar se são dados de treinamento
    if 'X_train' in data and 'y_train' in data:
        X_train = np.array(data['X_train'])
        y_train = np.array(data['y_train'])

        # Executar a otimização de hiperparâmetros
        best_params = optimize_hyperparameters(X_train, y_train)

        # Enviar os melhores parâmetros de volta para o mestre
        socket.send_json(best_params)

    # Verificar se são dados de teste
    elif 'X_test' in data:
        X_test = np.array(data['X_test'])

        # Receber os melhores parâmetros do mestre
        best_params = socket.recv_json()

        # Fazer previsões usando os melhores parâmetros
        predicted_values = make_predictions(
            X_train, y_train, X_test, best_params)

        # Enviar as previsões de volta para o mestre
        socket.send_json(predicted_values.tolist())
