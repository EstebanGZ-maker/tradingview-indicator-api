# === Python Script: procesador_trading.py ===
# Objetivo: Extraer, transformar y exportar datos del mercado desde CoinGlass y Bybit
# para su consumo en TradingView vía JSON

import json
import requests
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# === Cargar variables de entorno ===
load_dotenv()

USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0")
API_KEY_COINGLASS = os.getenv("API_KEY_COINGLASS", "")

# === Configuración de headers de API ===
HEADERS = {
    "User-Agent": USER_AGENT
    # "Authorization": f"Bearer {API_KEY_COINGLASS}"  #
}

# === Utilidad de reintento ===
def safe_get(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[Intento {attempt+1}] Error al acceder a {url}: {e}")
            time.sleep(delay)
    return {}

# === CoinGlass: Liquidation Map ===
def extract_liquidation_zones():
    url = "https://www.coinglass.com/pro/futures/LiquidationMap"
    data = safe_get(url)
    zones = []
    for item in data.get("data", [])[:5]:
        zones.append({
            "price": item.get("price", 0),
            "type": "short" if item.get("side") == "SELL" else "long",
            "label": "Zona de Cortos" if item.get("side") == "SELL" else "Zona de Compras"
        })
    return zones

# === Delta de volumen ===
def calculate_volume_delta():
    url = "https://www.coinglass.com/es/hyperliquid"
    data = safe_get(url)
    delta_value = float(data.get("delta", 0))
    return {
        "value_usd": round(delta_value, 2),
        "trend": "bullish" if delta_value > 0 else "bearish",
        "dominance": "buyers" if delta_value > 0 else "sellers"
    }

# === Whale Activity ===
def detect_whale_activity():
    # Simulación mientras no haya endpoint específico
    return [
        {"price": 65300, "label": "Whale Buy"},
        {"price": 64800, "label": "Whale Sell"}
    ]

# === Generación de señales ===
def generate_signals(liquidity, delta, whales):
    signals = []
    if delta['trend'] == "bullish" and any(z['type'] == 'long' for z in liquidity):
        signals.append({"price": liquidity[0]['price'], "type": "buy", "reason": "zone+delta+whale"})
    return signals

# === Construcción del payload ===
def generate_payload():
    liquidity = extract_liquidation_zones()
    delta = calculate_volume_delta()
    whales = detect_whale_activity()
    signals = generate_signals(liquidity, delta, whales)
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "liquidity_zones": liquidity,
        "whale_zones": whales,
        "volume_delta": delta,
        "market_state": "neutral",
        "signals": signals
    }

# === Exportación del JSON ===
def export_to_json(payload, filename="indicador_data.json"):
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)

if __name__ == "__main__":
    data = generate_payload()
    export_to_json(data)
    print("JSON generado exitosamente: indicador_data.json")
