"""FastAPI application entrypoint."""

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router as portfolio_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="ARAIA Portfolio Input API")
app.include_router(portfolio_router)
