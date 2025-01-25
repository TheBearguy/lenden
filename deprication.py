# This is an example file
# IF needed -> we can build such models for specific product categories
# to overall boost the accuracy of the suggested current valuation.
# Atleast we're doing it "on paper";

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# Historical data simulation (replace this with real data)
data = {
    "uniqueness": np.random.uniform(0, 1, 1000),
    "preciousness": np.random.uniform(0, 1, 1000),
    "market_trend": np.random.uniform(0.5, 1.5, 1000),
    "age": np.random.uniform(0, 10, 1000),
    "depreciation_rate": np.random.uniform(0, 0.2, 1000),  # Target variable
}

df = pd.DataFrame(data)

# Train/test split
X = df[["uniqueness", "preciousness", "market_trend", "age"]]
y = df["depreciation_rate"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a regression model
depreciation_model = RandomForestRegressor(n_estimators=100, random_state=42)
depreciation_model.fit(X_train, y_train)

# Evaluate the model
y_pred = depreciation_model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

class ProductValuation:
    def __init__(self, uniqueness, preciousness, market_trend, age):
        self.uniqueness = uniqueness
        self.preciousness = preciousness
        self.market_trend = market_trend
        self.age = age

    def predict_depreciation(self):
        input_data = np.array([[self.uniqueness, self.preciousness, self.market_trend, self.age]])
        predicted_depreciation = depreciation_model.predict(input_data)[0]
        return predicted_depreciation

    def calculate_value(self):
        depreciation_rate = self.predict_depreciation()
        base_value = 1000  # Assume a base value
        adjusted_value = base_value * (1 - depreciation_rate)
        adjusted_value *= self.uniqueness * self.preciousness * self.market_trend
        return adjusted_value
