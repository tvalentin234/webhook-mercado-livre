import streamlit as st
import pandas as pd
import psycopg2
import os

# Configuração da página
st.set_page_config(page_title="Painel Mercado Livre", layout="wide")
st.title("📦 Painel de Mensagens Mercado Livre")

# Conexão com PostgreSQL
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")
    st.stop()

# Buscar os últimos pack_ids únicos
try:
    cursor.execute("""
        SELECT pack_id, MAX(timestamp) as ultima_msg
        FROM chat_mensagens
        GROUP BY pack_id
        ORDER BY ultima_msg DESC
        LIMIT 20
    """)
    pack_ids = [row[0] for row in cursor.fetchall()]
except Exception as e:
    st.error(f"Erro ao buscar os pack_ids: {e}")
    st.stop()

# Seleção de pedido
pack_id_selecionado = st.selectbox("Selecione um pedido:", pack_ids)

# Mostrar mensagens do pack_id selecionado
if pack_id_selecionado:
    cursor.execute("""
        SELECT sender_id, receiver_id, message_text, timestamp, status
        FROM chat_mensagens
        WHERE pack_id = %s
        ORDER BY timestamp ASC
    """, (pack_id_selecionado,))
    
    mensagens = cursor.fetchall()
    
    df = pd.DataFrame(mensagens, columns=[
        "Remetente", "Destinatário", "Mensagem", "Data/Hora", "Status"
    ])
    
    st.dataframe(df, use_container_width=True)
    
    # Botão para marcar como lidas
    if st.button("Marcar todas como lidas"):
        cursor.execute("""
            UPDATE chat_mensagens
            SET status = 'lida'
            WHERE pack_id = %s
        """, (pack_id_selecionado,))
        conn.commit()
        st.success("Mensagens marcadas como lidas!")

# Fechar conexão
cursor.close()
conn.close()

