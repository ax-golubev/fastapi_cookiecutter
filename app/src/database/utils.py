from contextlib import asynccontextmanager, contextmanager
from typing import Iterator

from database import Database


@contextmanager
def disable_commit(db: Database, log) -> Iterator:
    restore = True
    # If `db.session` already has its `commit` method disabled we won't try disabling *and* restoring it again.
    if db.session.info.get("disabled", False):
        restore = False
    else:
        log.debug("Temporarily disabling commit.")
        db.session.info["disabled"] = True
        db.session.info["logger"] = log
    try:
        yield
    finally:
        if restore:
            log.debug("Reenabling commit.")
            db.session.info["disabled"] = False
            db.session.info["logger"] = None


@asynccontextmanager
async def transactional(db: Database, log) -> Iterator:
    """Run a step function in an implicit transaction with automatic rollback or commit.

    It will rollback in case of error, commit otherwise. It will also disable the `commit()` method
    on `BaseModel.session` for the time `transactional` is in effect.
    """
    try:
        with disable_commit(db, log):
            yield
        log.debug("Committing transaction.")
        await db.session.commit()
    except Exception:
        log.warning("Rolling back transaction.")
        raise
    finally:
        # Extra safe guard rollback. If the commit failed there is still a failed transaction open.
        # BTW: without a transaction in progress this method is a pass-through.
        await db.session.rollback()
