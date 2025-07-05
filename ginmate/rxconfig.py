import reflex as rx
import os

# 環境変数から設定を取得、デフォルトは開発環境
ENV = os.getenv("ENV", "dev")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3001"))
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
API_URL = os.getenv("API_URL", "http://localhost:8000")

config = rx.Config(
    app_name="ginmate",
    db_url="sqlite:///ginmate.db",
    env=rx.Env.PROD if ENV == "prod" else rx.Env.DEV,
    frontend_port=FRONTEND_PORT,
    backend_port=BACKEND_PORT,
    api_url=API_URL,
) 