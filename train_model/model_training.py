import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

def train_depreciation_model():
    data = {
        "uniqueness": np.random.uniform(0, 1, 1000),
        "preciousness": np.random.uniform(0, 1, 1000),
        "market_trend": np.random.uniform(0.5, 1.5, 1000),
        "age": np.random.uniform(0, 10, 1000),
        "depreciation_rate": np.random.uniform(0.05, 0.15, 1000),
    }

    df = pd.DataFrame(data)
    X = df[["uniqueness", "preciousness", "market_trend", "age"]]
    y = df["depreciation_rate"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Trained depreciation model with MSE: {mse}")

    joblib.dump(model, "depreciation_model.pkl")

# Uncomment the line below to train and save the model
# train_depreciation_model()