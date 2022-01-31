import logging
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any, Generator, Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


# Copyright 2019-2020 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class WrappedSession(AsyncSession):
    """This Session class allows us to disable commit during steps."""

    async def commit(self) -> None:
        if self.info.get("disabled", False):
            self.info.get("logger", logger).warning(
                "Step function tried to issue a commit. It should not! "
                "Will execute commit on behalf of step function when it returns."
            )
        else:
            await super().commit()


ENGINE_ARGUMENTS = {
    "connect_args": {"timeout": 10},
    "future": True,
    "echo": True,
}
SESSION_ARGUMENTS = {"class_": WrappedSession, "autocommit": False, "autoflush": True}


class Database:
    """Setup and contain our database connection.

    This is used to be able to setup the database in an uniform way while allowing easy testing and session management.

    Session management is done using ``scoped_session`` with a special scopefunc, because we cannot use
    threading.local(). Contextvar does the right thing with respect to asyncio and behaves similar to threading.local().
    We only store a random string in the contextvar and let scoped session do the heavy lifting. This allows us to
    easily start a new session or get the existing one using the scoped_session mechanics.
    """

    def __init__(self, db_url: str) -> None:
        self.request_context: ContextVar[str] = ContextVar(
            "request_context", default=""
        )
        self.engine = create_async_engine(db_url, **ENGINE_ARGUMENTS)
        self.session_factory = sessionmaker(bind=self.engine, **SESSION_ARGUMENTS)

        self.scoped_session = async_scoped_session(
            self.session_factory, self._scopefunc
        )

    def _scopefunc(self) -> Optional[str]:
        scope_str = self.request_context.get()
        return scope_str

    @property
    def session(self) -> WrappedSession:
        return self.scoped_session()

    @asynccontextmanager
    async def database_scope(self, **kwargs: Any) -> Generator["Database", None, None]:
        """Create a new database session (scope).

        This creates a new database session to handle all the database connection
        from a single scope (request or workflow).
        This method should typically only been called in request middleware or at the start of workflows.

        Args:
            ``**kwargs``: Optional session kw args for this session
        """
        token = self.request_context.set(str(uuid4()))
        self.scoped_session(**kwargs)
        yield self
        await self.scoped_session.remove()
        self.request_context.reset(token)
