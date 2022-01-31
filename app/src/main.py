import logging

import sentry_sdk
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

import routers
from core.config import settings
from core.events import create_start_app_handler, create_stop_app_handler
from core.logger import LOGGING
from database import db
from database.middleware import DBSessionMiddleware


def get_application() -> FastAPI:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=1.0)

    application = FastAPI(
        title=settings.project,
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    application.add_middleware(SentryAsgiMiddleware)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(DBSessionMiddleware, database=db)

    application.add_event_handler(
        "startup",
        create_start_app_handler(application),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    application.include_router(routers.router)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
