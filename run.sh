#!/bin/bash
source venv/bin/activate
cd app
python procesador_trading.py
python api_tradingview.py
