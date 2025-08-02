#!/bin/bash

# Caminho base do projeto
cd "$(dirname "$0")"

# Variáveis de ambiente
export DATABASE_URL="postgresql://thyago:senha123@localhost:5432/ml_chat"
export ML_ACCESS_TOKEN="SEU_TOKEN_DO_MERCADO_LIVRE_AQUI"

# Iniciar servidor Flask
echo "Iniciando webhook Flask em http://localhost:5000 ..."
flask run --port=5000

