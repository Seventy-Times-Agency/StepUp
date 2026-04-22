import json
from typing import Any, Dict, Optional

import aiosqlite
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey


def _key(k: StorageKey) -> str:
    return (
        f"{k.bot_id}:{k.chat_id}:{k.user_id}:"
        f"{k.thread_id or ''}:{k.business_connection_id or ''}"
    )


class SQLiteStorage(BaseStorage):
    """FSM-хранилище на SQLite — переживает рестарт воркера."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS fsm_state ("
                "key TEXT PRIMARY KEY, state TEXT)"
            )
            await db.execute(
                "CREATE TABLE IF NOT EXISTS fsm_data ("
                "key TEXT PRIMARY KEY, data TEXT NOT NULL)"
            )
            await db.commit()

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state_str = state.state if isinstance(state, State) else state
        async with aiosqlite.connect(self.db_path) as db:
            if state_str is None:
                await db.execute("DELETE FROM fsm_state WHERE key = ?", (_key(key),))
            else:
                await db.execute(
                    "INSERT INTO fsm_state (key, state) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET state = excluded.state",
                    (_key(key), state_str),
                )
            await db.commit()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "SELECT state FROM fsm_state WHERE key = ?", (_key(key),)
            )
            row = await cur.fetchone()
            return row[0] if row else None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            if not data:
                await db.execute("DELETE FROM fsm_data WHERE key = ?", (_key(key),))
            else:
                await db.execute(
                    "INSERT INTO fsm_data (key, data) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET data = excluded.data",
                    (_key(key), json.dumps(data, ensure_ascii=False)),
                )
            await db.commit()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "SELECT data FROM fsm_data WHERE key = ?", (_key(key),)
            )
            row = await cur.fetchone()
            return json.loads(row[0]) if row else {}

    async def close(self) -> None:
        return None
