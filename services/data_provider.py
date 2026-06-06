"""
Модуль для получения и кэширования данных о табаках и миксах.

Отвечает за загрузку данных из удаленного источника (Google Таблицы)
и предоставление их остальным модулям приложения.
"""

import csv
from typing import List, Dict
import requests

# URL для экспорта Google Таблицы в формате CSV
URL = (
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRlweNhHHRmHv9PjT0SMtL3J1kGopfKUg"
    "_dNgQE8VxcKNFj5JzzgFUOi4JIZhwfjEAJSHnzHE3SAPL/pub?output=csv"
)


def get_tobaccos() -> List[Dict[str, str]]:
    """
    Загружает актуальный список табаков из Google Таблицы.

    Декодирует полученный CSV-файл и преобразует его в список словарей,
    где ключи — это названия колонок таблицы.

    Returns:
        List[Dict[str, str]]: Список словарей с данными о табаках.
    """
    response = requests.get(URL, timeout=10)
    response.raise_for_status()  # Вызовет ошибку, если интернет упал

    lines: List[str] = response.content.decode("utf-8").splitlines()
    reader = csv.DictReader(lines)

    return list(reader)