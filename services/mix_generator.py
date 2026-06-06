"""
Модуль для генерации миксов на основе предпочтений пользователя.

Выбирает случайные табаки из базы данных (исходя из заданных критериев) и рассчитывает пропорции
в зависимости от требований к наличию холодка.
"""

import random
from typing import Dict, Any, List
from database.database import fetch_mixes


def generate_mix(user_preferences: Dict[str, Any]) -> str:
    """
    Генерирует текстовое сообщение с рецептом микса на основе предпочтений.

    Args:
        user_preferences (Dict[str, Any]): Словарь с критериями пользователя.

    Returns:
        str: Готовый текст рецепта или сообщение об ошибке.
    """
    # Делаем быстрый запрос в локальную СУБД SQLite вместо скачивания из сети
    filtered: List[Dict[str, Any]] = fetch_mixes(
        strength=user_preferences.get("strength", ""),
        taste=user_preferences.get("taste", ""),
        profile=user_preferences.get("profile", "")
    )

    # Если подходящих табаков в базе хватает, собираем микс
    if len(filtered) >= 3:
        mixes = random.sample(filtered, 3)
        result_message = "Ваш микс:\n\n"
        is_fresh = user_preferences.get("fresh") == "да"

        # Рассчитываем пропорции основных табаков
        for mix in mixes:
            percentage = "30%" if is_fresh else "33.3%"
            result_message += f" {mix['name']} — {percentage}\n"

        # Добавляем финальный штрих по холодку
        if is_fresh:
            result_message += "\n❄️Сарма Зима — 10%"
        else:
            result_message += "\nБез холодка"
    else:
        result_message = "Недостаточно подходящих табаков в базе для создания микса."

    return result_message