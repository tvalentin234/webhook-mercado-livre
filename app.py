from flask import Flask, request, jsonify
import requests
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ML_ACCESS_TOKEN")
DB_URL = os.getenv("DATABASE_URL")

@app.route('/')
def home():
    return "Webhook ML rodando"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "Payload vazio"}), 400

    if 'resource' in data and data['topic'] == 'messages':
        resource_url = f"https://api.mercadolibre.com{data['resource']}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

        try:
            response = requests.get(resource_url, headers=headers)
            response.raise_for_status()
            mensagens = response.json().get("messages", [])
            for msg in mensagens:
                salvar_mensagem(msg)
            return jsonify({"status": "mensagens processadas"}), 200

        except requests.exceptions.RequestException as e:
            return jsonify({"erro na requisicao": str(e)}), 500
    else:
        return jsonify({"status": "evento ignorado"}), 200

def salvar_mensagem(msg):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_mensagens (id, pack_id, sender_id, receiver_id, message_text, timestamp, status)
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
        """, (
            msg.get("pack_id"),
            msg.get("sender", {}).get("user_id"),
            msg.get("receiver", {}).get("user_id"),
            msg.get("text"),
            msg.get("date_created", datetime.now().isoformat()),
            'nao_lida'
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao salvar mensagem:", e)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

