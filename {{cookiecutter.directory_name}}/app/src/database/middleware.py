from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from database.session import Database


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, database: Database, commit_on_exit: bool = False):
        super().__init__(app)
        self.commit_on_exit = commit_on_exit
        self.database = database

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        async with self.database.database_scope():
            response = await call_next(request)
        return response
