from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'vknoprecinho')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'EAAYgKxphH8ABOZBl2TLbnbCwgM8ZARvioRZBFpMhmVpmQPbSucwtJRW9PjambVZANRi7k6qT9no61gGY3vo2Ga8AWGF108g12G6gslyZCHxLJDlz6CI5yGpkKgdGq0BiG0eGYX3uRMWtRcZAuW12ltm4QdVKTiLTq5zYXtx9ZAGOWgZBJJOoGkTD8vDt5rg58vjqdAhUJtaFFeNlqAZDZD')


@app.post("/webhook")
async def webhook_listener(request: Request):
    data = await request.json()
    print("🛎️ Evento recebido:")
    print(data)

    try:
        entry = data.get('entry', [])[0]
        change = entry.get('changes', [])[0]
        value = change.get('value', {})
        
        if change.get('field') == 'comments':
            user_id = value['from']['id']
            username = value['from']['username']
            comment_text = value.get('text', '')

            print(f"💬 Novo comentário de {username} (ID: {user_id}): {comment_text}")

            # Envia a mensagem no Direct
            send_message(user_id, "🚀 Opa! Aqui está o link do produto que você comentou!")

    except Exception as e:
        print("❌ Erro ao processar webhook:", e)

    return {"status": "received"}


# 🔥 Função para enviar Direct
def send_message(user_id, message_text):
    url = f'https://graph.facebook.com/v19.0/{user_id}/messages'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    payload = {
        "messaging_product": "instagram",
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": message_text
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ Mensagem enviada com sucesso!")
    else:
        print("❌ Erro ao enviar mensagem:", response.text)
