import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from modules.data_engine import load_prices
from modules.core import micro_windows, compute_features, classify_microtramo
from export.report import export_word

st.set_page_config(page_title="MIRCAT v0.1", layout="wide")
st.title("MIRCAT v0.1 — Microtramos de Turbulencia")

# Sidebar: parámetros
st.sidebar.header("Parámetros")
win = st.sidebar.slider("Ventana microtramo (minutos)", min_value=10, max_value=120, value=30, step=5)
step = st.sidebar.slider("Paso entre ventanas (minutos)", min_value=5, max_value=120, value=15, step=5)
thr_burst = st.sidebar.slider("Umbral Burst (|Z|)", 0.5, 3.0, 1.5, 0.1)
thr_liq = st.sidebar.slider("Umbral Liquidez (rango/price)", 0.001, 0.05, 0.01, 0.001)
thr_prop = st.sidebar.slider("Umbral Propagación (|ρ|)", 0.0, 0.9, 0.2, 0.05)

# Datos
data_file = Path("data")/"sample_prices.csv"
df = load_prices(str(data_file))

# Cálculo de features
feat = compute_features(df, win=win)

# Clasificación por microventanas (mostrar tabla breve)
idxs = micro_windows(df, win=win, step=step)
rows = []
for (a,b) in idxs[:50]:  # limitar listado para vista rápida
    frow = feat.iloc[b-1]  # usar último punto de la ventana
    cls = classify_microtramo(frow, thr_burst, thr_liq, thr_prop)
    rows.append({"inicio": a, "fin": b, "burst": round(frow.get("burst", np.nan), 3),
                 "liq": round(frow.get("liq_proxy", np.nan), 4),
                 "prop|ρ|": round(abs(frow.get("prop_corr", np.nan)), 3),
                 "clase": cls})
table = pd.DataFrame(rows)
st.subheader("Clasificación de microtramos (muestra)")
st.dataframe(table)

# Gráficos simples
st.subheader("Gráficos")
st.line_chart(df.set_index("t")["price"], height=200)
st.line_chart(feat[["vol_local"]].fillna(0), height=200)
st.line_chart(feat[["burst"]].fillna(0), height=200)
st.line_chart(feat[["liq_proxy"]].fillna(0), height=200)
st.line_chart(feat[["prop_corr"]].fillna(0), height=200)
# Nuevas métricas
if "E_scale8" in feat.columns:
    st.line_chart(feat[["E_scale8"]].fillna(0), height=200)
if "liq_roll" in feat.columns:
    st.line_chart(feat[["liq_roll"]].fillna(0), height=200)


# Exportación
st.subheader("Exportar informe")
if st.button("Exportar informe Word (con PNG)"):
    summary = {
        "Precio inicial": round(df["price"].iloc[0], 2),
        "Precio final": round(df["price"].iloc[-1], 2),
        "Ventana": win,
        "Paso": step,
        "Umbral burst": thr_burst,
        "Umbral liq": thr_liq,
        "Umbral prop": thr_prop,
        "Wavelets": "on",
        "Liquidez_Roll": "on"
    }
    out_doc = export_word(df, feat, summary, "exports")
    st.success(f"Informe generado: {out_doc}")
    st.write("Archivo guardado en carpeta `exports/`.")


st.markdown("---")
st.subheader("Heatmap wavelet (escalas vs tiempo)")
from modules.wavelets import wavelet_scalogram
power, widths = wavelet_scalogram(df["ret"], widths=(2,4,8,16,32,64))
import matplotlib.pyplot as plt
import numpy as np
import io
fig = plt.figure()
plt.imshow(power, aspect='auto')
plt.title('Heatmap Wavelet')
plt.xlabel('Tiempo')
plt.ylabel('Escala')
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
plt.close(fig)
st.image(buf.getvalue())

st.markdown("---")
st.subheader("Clasificador rápido (RandomForest)")
from modules.model import make_labels, train_rf
labels = make_labels(feat, thr_burst=thr_burst, thr_liq=thr_liq, thr_prop=thr_prop)
feat_ml = feat.copy()
feat_ml["label"] = labels
if st.button("Entrenar y evaluar clasificador"):
    model, acc, imp_df = train_rf(feat_ml.select_dtypes(include=[float,int]).fillna(0).assign(label=labels), label_col="label")
    if model is None:
        st.warning("Datos insuficientes para entrenar.")
    else:
        st.success(f"Accuracy hold-out: {acc:.3f}")
        st.dataframe(imp_df.head(15))
