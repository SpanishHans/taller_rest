from fastapi import FastAPI
import os

from modules.db_engine import init_db
from modules.router_usuarios import router_users
from modules.router_libros import router_libros
from modules.router_reviews import router_reviews

VERSION = os.getenv("VERSION", "1.0.0")

app = FastAPI(
    title="Servicio de Autenticación",
    description="API para gestión de usuarios y autenticación",
    version=VERSION
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, bienvenido a taller rest!"}

# Register your API routes
app.include_router(router_users)
app.include_router(router_libros)
app.include_router(router_reviews)