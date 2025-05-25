from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'vknoprecinho')

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verificado com sucesso!")
        return PlainTextResponse(content=challenge)
    else:
        print("❌ Verificação falhou.")
        return JSONResponse(content={"error": "Verificação falhou"}, status_code=403)

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("📥 Dados recebidos no webhook:")
    print(data)

    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                field = change.get("field")
                if field == "feed":
                    value = change.get("value", {})
                    if value.get("item") == "comment":
                        comment_text = value.get("message")
                        commenter_id = value.get("from", {}).get("id")
                        post_id = value.get("post_id")

                        print(f"💬 Novo comentário no post {post_id}")
                        print(f"👤 ID do usuário: {commenter_id}")
                        print(f"✍️ Comentário: {comment_text}")

    except Exception as e:
        print(f"❌ Erro ao processar webhook: {e}")

    return JSONResponse(content={"status": "recebido"}, status_code=200)

@app.get("/")
def root():
    return {"status": "🔥 Webhook rodando no Render com sucesso!"}
