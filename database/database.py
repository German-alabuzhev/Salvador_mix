"""
Модуль для работы с локальной базой данных SQLite.

Обеспечивает кэширование данных из удаленного CSV-источника
и фильтрацию элементов по критериям пользователя.
"""

import sqlite3
from typing import List, Dict, Any

DB_PATH = "database/hookah.db"


def init_db() -> None:
    """Инициализирует структуру таблиц в базе данных."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tobaccos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                strength TEXT,
                taste TEXT,
                profile TEXT
            )
        """)
        conn.commit()


def update_tobaccos_cache(tobacco_list: List[Dict[str, str]]) -> None:
    """
    Обновляет локальные данные на основе полученного списка.

    Args:
        tobacco_list (List[Dict[str, str]]): Данные для импорта.
    """
    init_db()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tobaccos")

        for item in tobacco_list:
            cursor.execute("""
                INSERT INTO tobaccos (name, strength, taste, profile)
                VALUES (?, ?, ?, ?)
            """, (
                item.get('name', ''),
                item.get('strength', ''),
                item.get('taste', ''),
                item.get('profile', '')
            ))
        conn.commit()


def fetch_mixes(strength: str, taste: str, profile: str) -> List[Dict[str, Any]]:
    """
    Выполняет выборку данных по заданным параметрам фильтрации.

    Args:
        strength (str): Значение крепости.
        taste (str): Категория вкуса.
        profile (str): Вкусовой профиль.

    Returns:
        List[Dict[str, Any]]: Результат выборки из базы данных.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, strength, taste, profile 
            FROM tobaccos 
            WHERE LOWER(strength) = LOWER(?) 
              AND LOWER(taste) = LOWER(?) 
              AND LOWER(profile) = LOWER(?)
        """, (strength, taste, profile))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]