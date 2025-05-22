from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'vknoprecinho')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'EAAYgKxphH8ABOZBl2TLbnbCwgM8ZARvioRZBFpMhmVpmQPbSucwtJRW9PjambVZANRi7k6qT9no61gGY3vo2Ga8AWGF108g12G6gslyZCHxLJDlz6CI5yGpkKgdGq0BiG0eGYX3uRMWtRcZAuW12ltm4QdVKTiLTq5zYXtx9ZAGOWgZBJJOoGkTD8vDt5rg58vjqdAhUJtaFFeNlqAZDZD')


@app.get("/webhook")
async def verify(request: Request):
    """
    Verificação do webhook (GET)
    """
    params = dict(request.query_params)
    mode = params.get('hub.mode')
    token = params.get('hub.verify_token')
    challenge = params.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print('WEBHOOK VERIFICADO ✅')
        return int(challenge)
    else:
        print('FALHA NA VERIFICAÇÃO ❌')
        return {"error": "Verificação falhou"}


@app.post("/webhook")
async def webhook_listener(payload: dict):
    """
    Recebe os eventos do Instagram (POST)
    """
    print("🔔 Evento recebido:")
    print(payload)

    # Aqui você pode tratar o evento, por exemplo pegar comentário:
    try:
        entry = payload['entry'][0]
        changes = entry.get('changes', [])

        for change in changes:
            if change['field'] == 'comments':
                comment = change['value']['text']
                username = change['value']['from']['username']
                print(f"🗨️ Novo comentário de {username}: {comment}")

    except Exception as e:
        print(f"Erro ao tratar o webhook: {e}")

    return {"status": "received"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
