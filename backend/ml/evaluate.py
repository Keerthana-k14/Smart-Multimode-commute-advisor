import pandas as pd
import numpy as np
import pickle
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ml.features import load_and_engineer, FEATURES
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

def evaluate_models():
    from config import RAW_CSV, MODELS_DIR

    print("Loading dataset...")
    df = load_and_engineer(RAW_CSV)

    results = {}
    for mode in ['car', 'metro', 'bus']:
        col = f'{mode}_travel_time'
        df_clean = df.dropna(subset=FEATURES + [col])
        X = df_clean[FEATURES]
        y = df_clean[col]

        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model_path = os.path.join(MODELS_DIR, f'rf_{mode}.pkl')
        model = pickle.load(open(model_path, 'rb'))
        preds = model.predict(X_test)

        mae  = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2   = model.score(X_test, y_test)

        results[mode] = {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "R2": round(r2, 4)}
        print(f"{mode:6s} → MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.4f}")

    return results

if __name__ == "__main__":
    evaluate_models()