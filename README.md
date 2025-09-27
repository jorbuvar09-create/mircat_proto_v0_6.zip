# MIRCAT Prototype v0.1 — Microtramos de Turbulencia

Prototipo rápido en **Python + Streamlit** para explorar microtramos, calcular métricas básicas (volatilidad local, correlación dinámica, proxy de liquidez) y **exportar un informe Word** con tablas y PNG.

## Instrucciones de ejecución (local)
1) Crea y activa un entorno (opcional pero recomendado).
2) Instala dependencias:
```bash
pip install -r requirements.txt
```
3) Ejecuta el dashboard:
```bash
streamlit run app.py
```
4) Interactúa con los controles (ventana de microtramo, umbrales, etc.).
5) Exporta el **informe Word** desde el botón "Exportar informe".
   El archivo se guarda en `exports/` junto con los gráficos PNG.

## Estructura
```
mircat_proto_v0_1/
├─ app.py                # Dashboard Streamlit
├─ requirements.txt
├─ README.md
├─ data/
│  └─ sample_prices.csv  # Datos simulados
├─ modules/
│  ├─ data_engine.py     # Carga/simulación de datos
│  ├─ core.py            # Lógica de microtramos y métricas
│  ├─ volatility.py      # Volatilidad local
│  ├─ liquidity.py       # Proxy de liquidez
│  └─ propagation.py     # Correlación dinámica / contagio
└─ export/
   └─ report.py          # Exportador Word + guardado de PNG
```

## Notas
- Este es un prototipo: la arquitectura está pensada para crecer modularmente.
- Los datos reales (intradiarios, spreads, etc.) se integrarán después con conectores.
- El informe Word es reproducible y guarda gráficos y tablas con trazabilidad básica.
