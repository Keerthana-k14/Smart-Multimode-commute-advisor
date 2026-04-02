import pandas as pd
import pickle
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ml.features import load_and_engineer, FEATURES
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

CSV_PATH = os.path.join(os.path.dirname(__file__),
                        '..', 'data', 'raw', 'Banglore_traffic_Dataset.csv')

print("Loading dataset...")
df = load_and_engineer(CSV_PATH)
print(f"Dataset loaded: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")

os.makedirs(os.path.join(os.path.dirname(__file__), 'models'), exist_ok=True)

for mode in ['car', 'metro', 'bus']:
    col = f'{mode}_travel_time'
    df_clean = df.dropna(subset=FEATURES + [col])
    X = df_clean[FEATURES]
    y = df_clean[col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    preds  = model.predict(X_test)
    mae    = mean_absolute_error(y_test, preds)
    rmse   = np.sqrt(mean_squared_error(y_test, preds))
    print(f"{mode:6s} → MAE: {mae:.2f} min  |  RMSE: {rmse:.2f} min")

    model_path = os.path.join(os.path.dirname(__file__), 'models', f'rf_{mode}.pkl')
    pickle.dump(model, open(model_path, 'wb'))
    print(f"  Saved → {model_path}")

print("\nAll 3 models trained and saved!")