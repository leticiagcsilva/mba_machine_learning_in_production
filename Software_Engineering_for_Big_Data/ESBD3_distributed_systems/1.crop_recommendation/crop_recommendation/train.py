import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from minio import Minio

# Load and preprocess the training data
train_data = pd.read_csv('data.csv')
X_train = train_data.drop('target', axis=1)
y_train = train_data['target']

# Define the parameter grid for grid search
param_grid = {
    'class_weight': ['balanced', None],
    'C': np.logspace(-4, 0, 4),
    'penalty': ['l1', 'l2']
}

# Create the logistic regression model
log_reg = LogisticRegression(random_state=2)

# Perform grid search to find the best parameters
grid_search = GridSearchCV(log_reg, param_grid, cv=10)
grid_search.fit(X_train, y_train)

# Get the best parameters from the grid search
best_params = grid_search.best_params_
print("Melhores parâmetros:", best_params)

# Save the best model using joblib
model_path = 'modelo.pkl'
joblib.dump(grid_search.best_estimator_, model_path)

# Configure the MinIO access information
minio_url = 'localhost:9000'
access_key = 'minio'
secret_key = 'minio123'
bucket_name = 'models'

# Initialize the MinIO client
client = Minio(minio_url, access_key=access_key,
               secret_key=secret_key, secure=False)

# Upload the pickled object to MinIO
try:
    client.fput_object(bucket_name, model_path, model_path)
    print("Arquivo enviado com sucesso para o bucket!")
except:
    print("Ocorreu um erro ao enviar o arquivo para o bucket:")
