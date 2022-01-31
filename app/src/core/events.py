from typing import Callable

from fastapi import FastAPI


def create_start_app_handler(
    _: FastAPI,
) -> Callable:
    async def start_app() -> None:
        return None

    return start_app


def create_stop_app_handler(_: FastAPI) -> Callable:
    async def stop_app() -> None:
        return None

    return stop_app
