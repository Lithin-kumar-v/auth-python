# app/audit/base.py
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
import asyncio

logger = logging.getLogger("audit")


def _utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _json(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        return json.dumps(value, default=str, ensure_ascii=False)
    except Exception:
        return json.dumps({"_unserializable": str(value)})


# ------------------------------------------------------------------
# INTERNAL WRITE (SYNC)
# ------------------------------------------------------------------
def _write_sync(session: Session, payload: dict):
    stmt = text("""
        INSERT INTO audit_log (
            action, resource, resource_id,
            before_state, after_state, meta,
            actor_id, ip, user_agent, created_at
        )
        VALUES (
            :action, :resource, :resource_id,
            :before_state, :after_state, :meta,
            :actor_id, :ip, :user_agent, :created_at
        )
    """)
    session.execute(stmt, payload)
    session.commit()


# ------------------------------------------------------------------
# INTERNAL WRITE (ASYNC)
# ------------------------------------------------------------------
async def _write_async(session: AsyncSession, payload: dict):
    stmt = text("""
        INSERT INTO audit_log (
            action, resource, resource_id,
            before_state, after_state, meta,
            actor_id, ip, user_agent, created_at
        )
        VALUES (
            :action, :resource, :resource_id,
            :before_state, :after_state, :meta,
            :actor_id, :ip, :user_agent, :created_at
        )
    """)
    await session.execute(stmt, payload)
    await session.commit()


# ------------------------------------------------------------------
# 🌍 UNIVERSAL AUDIT ENTRY POINT
# ------------------------------------------------------------------
def write_audit(
    *,
    session,
    action: str,
    resource: str,
    resource_id: str,
    before: Optional[Dict[str, Any]] = None,
    after: Optional[Dict[str, Any]] = None,
    meta: Optional[Dict[str, Any]] = None,
    actor_id: Optional[str] = None,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> None:
    """
    UNIVERSAL audit writer.
    - Works with Session and AsyncSession
    - Never raises
    - Never blocks ERP
    """

    payload = {
        "action": action,
        "resource": resource,
        "resource_id": resource_id[:255],
        "before_state": _json(before),
        "after_state": _json(after),
        "meta": _json(meta),
        "actor_id": actor_id,
        "ip": ip,
        "user_agent": user_agent,
        "created_at": _utc_now(),
    }

    try:
        if isinstance(session, AsyncSession):
            # fire-and-forget safe async
            asyncio.create_task(_write_async(session, payload))
        else:
            _write_sync(session, payload)

    except Exception:
        logger.exception("[AUDIT] write failed")
