import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from config import routes
from app.core.commons.inject_clients import instantiate_and_inject_clients


API_VERSION = "v0.1.0"

sentry_sdk.init(os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)

itemsInit = {}

app = FastAPI(
    title="Registro Infracciones de Transito",
    description="Registro de Infracciones De Transito",
    version=API_VERSION,
    redoc_url="/api/v1/redoc",
    docs_url="/api/v1/docs",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.urls)

instantiate_and_inject_clients()


SentryAsgiMiddleware(app)
