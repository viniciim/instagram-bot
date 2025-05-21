from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()

# ✅ Defina aqui seu token de verificação (o mesmo que você colocou no painel da Meta)
VERIFY_TOKEN = "vknoprecinho"


# 🚩 Endpoint para a verificação do Webhook (GET)
@app.get("/webhook")
async def verify(request: Request):
    params = dict(request.query_params)

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)
    else:
        return JSONResponse(status_code=403, content={"error": "Forbidden"})


# 🚀 Endpoint para receber eventos (POST)
@app.post("/webhook")
async def webhook_events(payload: dict):
    print("📩 Recebeu evento:")
    print(payload)

    # Aqui você pode tratar os comentários recebidos
    # Exemplo simples:
    try:
        entry = payload['entry'][0]
        changes = entry['changes'][0]
        if changes['field'] == 'comments':
            comment = changes['value']
            print("🗨️ Novo comentário:")
            print(comment)
    except Exception as e:
        print("❌ Erro ao processar:", e)

    return {"status": "Recebido com sucesso"}
