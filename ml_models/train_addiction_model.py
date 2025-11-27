# ml_models/train_addiction_model.py
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

DATA_PATH = os.getenv("ADDICTION_DATA_PATH", "data/processed/addiction_dataset.csv")
MODEL_OUT = os.getenv("ADDICTION_MODEL_OUT", "ml_models/addiction_model.pkl")

def load_dummy_addiction_dataset(path=DATA_PATH):
    # If you don't have data, create a small synthetic dataset:
    import numpy as np
    import pandas as pd
    np.random.seed(0)
    rows = []
    for i in range(500):
        duration = np.random.randint(20, 600)  # seconds
        is_compilation = np.random.binomial(1, 0.2)
        view_count = np.random.randint(0, 100000)
        repeat_watch = np.random.randint(0,5)
        # synthetic addiction target: higher for short+compilation+repeat
        target = min(100, int(0.4*is_compilation*100 + 0.2*(1 if duration<60 else 0)*100 + 10*repeat_watch + np.random.randn()*5))
        rows.append({"duration_sec":duration, "is_compilation":is_compilation, "view_count":view_count, "repeat_watch":repeat_watch, "addiction_index":target})
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df

def train():
    if not os.path.exists(DATA_PATH):
        df = load_dummy_addiction_dataset()
    else:
        df = pd.read_csv(DATA_PATH)

    X = df[["duration_sec","is_compilation","view_count","repeat_watch"]]
    y = df["addiction_index"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print("MSE:", mean_squared_error(y_test, preds))
    print("R2:", r2_score(y_test, preds))
    joblib.dump(model, MODEL_OUT)
    print(f"Saved addiction model to {MODEL_OUT}")
    return model

if __name__ == "__main__":
    train()
