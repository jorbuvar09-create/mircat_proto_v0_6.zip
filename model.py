import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance

def make_labels(feat: pd.DataFrame,
                thr_burst: float = 1.5,
                thr_liq: float = 0.01,
                thr_prop: float = 0.2) -> pd.Series:
    # Regla: generar etiquetas en base a umbrales (proxy de verdad)
    def classify_row(r):
        b = r.get("burst", 0.0)

        l = r.get("liq_proxy", 0.0)

        p = abs(r.get("prop_corr", 0.0))

        if (b >= thr_burst) and (l >= thr_liq) and (p >= thr_prop):

            return 2  # pre-ruptura

        if (b >= thr_burst) or (l >= thr_liq) or (p >= thr_prop):

            return 1  # benigno

        return 0      # normal

    return feat.apply(classify_row, axis=1)

def train_rf(feat: pd.DataFrame, label_col: str = "label"):

    df = feat.copy().dropna()

    y = df[label_col]

    X = df.drop(columns=[label_col])

    if X.shape[0] < 50:

        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

    rf = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=123, n_jobs=-1)

    rf.fit(X_train, y_train)

    acc = rf.score(X_test, y_test)

    # Importancia por permutación (más estable interpretativamente)

    imp = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=123)

    imp_df = pd.DataFrame({"feature": X_test.columns, "importance": imp.importances_mean})

    imp_df = imp_df.sort_values("importance", ascending=False).reset_index(drop=True)

    return rf, acc, imp_df
