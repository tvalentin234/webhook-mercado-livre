#!/bin/bash

# Caminho base do projeto
cd "$(dirname "$0")"

# Variável do banco
export DATABASE_URL="postgresql://thyago:senha123@localhost:5432/ml_chat"

# Iniciar painel Streamlit
echo "Iniciando painel em http://localhost:8501 ..."
streamlit run painel.py
