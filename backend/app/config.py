from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str = ""
    # In production, set this to your Vercel URL, e.g. https://your-app.vercel.app
    frontend_url: str = "*"

    class Config:
        env_file = ".env"

settings = Settings()
