#!/bin/bash

# Caminho base do projeto
cd "$(dirname "$0")"

# Variáveis de ambiente
export DATABASE_URL="postgresql://thyago:senha123@localhost:5432/ml_chat"
export ML_ACCESS_TOKEN="SEU_TOKEN_DO_MERCADO_LIVRE_AQUI"

# Verificar se gnome-terminal existe
if ! command -v gnome-terminal &> /dev/null
then
    echo "Erro: gnome-terminal não encontrado. Instale ou use os scripts individuais."
    exit 1
fi

# Iniciar Flask em uma aba
gnome-terminal -- bash -c "echo 'Webhook Flask em http://localhost:5000'; export DATABASE_URL='$DATABASE_URL'; export ML_ACCESS_TOKEN='$ML_ACCESS_TOKEN'; flask run --port=5000; exec bash"

# Iniciar Streamlit em outra aba
gnome-terminal -- bash -c "echo 'Painel em http://localhost:8501'; export DATABASE_URL='$DATABASE_URL'; streamlit run painel.py; exec bash"

