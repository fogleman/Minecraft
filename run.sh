#!/bin/bash
# Script para executar o jogo Minecraft em Python

cd "$(dirname "$0")"

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Executa o jogo
python3 main.py


