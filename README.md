# Indicador Avanzado para TradingView

Este proyecto genera un indicador avanzado que muestra zonas institucionales, ballenas, delta de volumen y señales de entrada/salida, alimentado por datos externos.

##  Requisitos

- Python 3.8+
- `pip install -r requirements.txt`

##  Estructura

- `app/procesador_trading.py`: Genera archivo `indicador_data.json`
- `app/api_tradingview.py`: Servidor Flask para exponer el JSON
- `indicador_data.json`: Archivo de salida consumido por TradingView
- `run.sh`: Script para lanzar todo fácilmente

##  Uso

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
./run.sh

## Despliegue en Render

1. Crea un repo en GitHub.
2. Sube este proyecto.
3. Ve a [Render](https://render.com), crea un nuevo Web Service y conéctalo a tu repo.
4. Render usará `render.yaml` automáticamente.
