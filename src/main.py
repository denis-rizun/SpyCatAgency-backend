from fastapi import FastAPI

from src.api.exception_handlers import ExceptionHandler
from src.api.middlewares.cors import ConfiguredCORSMiddleware
from src.api.routes.health import router as health_router
from src.api.routes.v1.cats import router as cats_router
from src.api.routes.v1.missions import router as mission_router

app = FastAPI(title="Spy Cat Agency API", version="1.0.0")
app.add_middleware(ConfiguredCORSMiddleware)

app.include_router(health_router)
app.include_router(cats_router, prefix="/api/v1")
app.include_router(mission_router, prefix="/api/v1")

ExceptionHandler.register(app)