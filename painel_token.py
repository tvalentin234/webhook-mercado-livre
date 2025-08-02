import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Gerar Token Mercado Livre", layout="centered")
st.title(":lock: Gerador e Renovador de Token - Mercado Livre")

def export_tokens_to_file(data, filename="tokens_mercado_livre.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        st.success(f"Tokens exportados com sucesso para {filename}")
    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")

tabs = st.tabs(["Gerar Access Token", "Renovar Token"])

with tabs[0]:
    st.subheader("Obter novo Access Token")
    with st.form("token_form"):
        client_id = st.text_input("Client ID", value="")
        client_secret = st.text_input("Client Secret", value="", type="password")
        redirect_uri = st.text_input("Redirect URI", value="https://localhost")
        code = st.text_input("Código de autorização (code=... da URL)")
        submitted = st.form_submit_button("Gerar Access Token")

    if submitted:
        if not all([client_id, client_secret, code, redirect_uri]):
            st.error("Todos os campos são obrigatórios.")
        else:
            url = "https://api.mercadolibre.com/oauth/token"
            payload = {
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            with st.spinner("Solicitando token ao Mercado Livre..."):
                response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                st.success("Access Token gerado com sucesso!")
                st.code(json.dumps(result, indent=2), language='json')

                st.text_input("Access Token", value=result['access_token'], key="at")
                st.text_input("Refresh Token", value=result['refresh_token'], key="rt")

                if st.button("Exportar tokens para arquivo JSON"):
                    export_tokens_to_file(result)
            else:
                st.error(f"Erro: {response.status_code}")
                try:
                    st.code(response.json())
                except:
                    st.text(response.text)

with tabs[1]:
    st.subheader("Renovar Access Token com Refresh Token")
    with st.form("refresh_form"):
        client_id = st.text_input("Client ID (refresh)", value="", key="rcid")
        client_secret = st.text_input("Client Secret (refresh)", value="", key="rcsec", type="password")
        refresh_token = st.text_input("Refresh Token", value="", key="rftok")
        refresh_submit = st.form_submit_button("Renovar Token")

    if refresh_submit:
        if not all([client_id, client_secret, refresh_token]):
            st.error("Todos os campos são obrigatórios para renovação.")
        else:
            url = "https://api.mercadolibre.com/oauth/token"
            payload = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            with st.spinner("Renovando token..."):
                response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                st.success("Novo Access Token gerado!")
                st.code(json.dumps(result, indent=2), language='json')

                st.text_input("Access Token", value=result['access_token'], key="at2")
                st.text_input("Novo Refresh Token", value=result['refresh_token'], key="rt2")

                if st.button("Exportar novo token para JSON"):
                    export_tokens_to_file(result, filename="tokens_renovados.json")
            else:
                st.error(f"Erro: {response.status_code}")
                try:
                    st.code(response.json())
                except:
                    st.text(response.text)

