from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import vendors, scenarios, params, generate, validate

app = FastAPI(title="Config Generator MVP", version="0.1.0", description="Generador de configuraciones para routers Mikrotik, Cisco y Juniper")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router, prefix="/api")
app.include_router(scenarios.router, prefix="/api")
app.include_router(params.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(validate.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Config Generator MVP"}

@app.get("/health")
def health_check():
    return {"status": "Ok"}