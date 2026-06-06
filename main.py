"""
Главный модуль запуска чат-бота ВКонтакте.

Управляет состояниями пользователей, обрабатывает входящие сообщения,
реализует систему навигации и координирует обновление локальной базы данных.
"""

from typing import Dict, Any
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN
from services.mix_generator import generate_mix
from services.data_provider import get_tobaccos
from database.database import update_tobaccos_cache

from keyboards.keyboards import (
    start_keyboard,
    keyboard,
    strength_keyboard,
    taste_keyboard,
    profile_keyboard,
    fresh_keyboard,
    result_keyboard,
    confirm_keyboard
)

# Автоматическое обновление базы данных из Google Таблицы при старте
try:
    print("Синхронизация с Google Таблицей...")
    remote_data = get_tobaccos()
    update_tobaccos_cache(remote_data)
    print("Локальный кэш SQLite успешно обновлен!")
except Exception as e:
    print(f"Ошибка обновления базы данных (используется старый кэш): {e}")

# Инициализация сессии VK API
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Оперативная память для хранения состояний пользователей
user_data: Dict[int, Dict[str, Any]] = {}

print("Бот запущен и готов к работе!")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        # Очищаем текст от лишних пробелов по краям
        message: str = event.text.strip().lower()
        user_id: int = event.user_id


        # Вспомогательная функция, чтобы определять, какую клавиатуру вернуть при ошибке
        def get_current_keyboard(uid: int):
            if uid not in user_data:
                return keyboard
            current_state = user_data[uid].get("state")
            if current_state == "strength":
                return strength_keyboard
            elif current_state == "taste":
                return taste_keyboard
            elif current_state == "profile":
                return profile_keyboard
            elif current_state == "fresh":
                return fresh_keyboard
            elif current_state == "result":
                return confirm_keyboard
            return keyboard


        # Если сообщение пустое (стикер, фото, голосовое)
        if not message:
            vk.messages.send(
                user_id=user_id,
                message="Пожалуйста, используйте кнопки на клавиатуре для выбора!",
                random_id=0,
                keyboard=get_current_keyboard(user_id)
            )
            continue

        # СТАРТОВЫЕ КОМАНДЫ
        if message in ["/start", "привет"]:
            vk.messages.send(
                user_id=user_id,
                message=(
                    "Добро пожаловать в кальянный бот!\n\n"
                    "Я помогу подобрать микс под ваши предпочтения."
                ),
                random_id=0,
                keyboard=start_keyboard
            )

        elif message == "начать":
            user_data[user_id] = {"state": "start"}
            vk.messages.send(
                user_id=user_id,
                message=(
                    "Добро пожаловать в кальянный бот!\n\n"
                    "Я помогу подобрать микс под ваши предпочтения."
                ),
                random_id=0,
                keyboard=keyboard
            )

        elif message == "подобрать микс":
            user_data[user_id] = {"state": "strength"}
            vk.messages.send(
                user_id=user_id,
                message="Выберите крепость:",
                random_id=0,
                keyboard=strength_keyboard
            )

        elif message in ["лёгкая", "средняя", "крепкая"]:
            user_data[user_id] = {
                "strength": message,
                "state": "taste"
            }
            vk.messages.send(
                user_id=user_id,
                message="Выберите направление вкуса:",
                random_id=0,
                keyboard=taste_keyboard
            )

        elif message in ["фруктовый", "ягодный"]:
            if user_id in user_data and user_data[user_id].get("state") == "taste":
                user_data[user_id]["taste"] = message
                user_data[user_id]["state"] = "profile"
                vk.messages.send(
                    user_id=user_id,
                    message="Выберите профиль вкуса:",
                    random_id=0,
                    keyboard=profile_keyboard
                )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Пожалуйста, соблюдайте порядок опроса!",
                    random_id=0,
                    keyboard=get_current_keyboard(user_id)
                )

        elif message in ["кислый", "сладкий"]:
            if user_id in user_data and user_data[user_id].get("state") == "profile":
                user_data[user_id]["profile"] = message
                user_data[user_id]["state"] = "fresh"
                vk.messages.send(
                    user_id=user_id,
                    message="Добавить холодок❄️?",
                    random_id=0,
                    keyboard=fresh_keyboard
                )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Пожалуйста, соблюдайте порядок опроса!",
                    random_id=0,
                    keyboard=get_current_keyboard(user_id)
                )

        elif message in ["да", "нет"]:
            if user_id in user_data and user_data[user_id].get("state") == "fresh":
                user_data[user_id]["fresh"] = message
                user_data[user_id]["state"] = "result"
                vk.messages.send(
                    user_id=user_id,
                    message=(
                        "Вот твои критерии:\n\n"
                        f"Крепость: {user_data[user_id]['strength']}\n"
                        f"Направление: {user_data[user_id]['taste']}\n"
                        f"Профиль: {user_data[user_id]['profile']}\n"
                        f"Холодок: {message}\n\n"
                        "Все верно?"
                    ),
                    random_id=0,
                    keyboard=confirm_keyboard
                )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Пожалуйста, соблюдайте порядок опроса!",
                    random_id=0,
                    keyboard=get_current_keyboard(user_id)
                )

        elif message == "подтвердить":
            if user_id in user_data and user_data[user_id].get("state") == "result":
                result_message = generate_mix(user_data[user_id])
                vk.messages.send(
                    user_id=user_id,
                    message=result_message,
                    random_id=0,
                    keyboard=result_keyboard
                )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Подтверждать пока нечего. Начните подбор микса!",
                    random_id=0,
                    keyboard=get_current_keyboard(user_id)
                )

        elif message == "назад":
            if user_id in user_data:
                state = user_data[user_id].get("state")

                if state == "taste":
                    vk.messages.send(
                        user_id=user_id,
                        message="Выберите крепость:",
                        random_id=0,
                        keyboard=strength_keyboard
                    )
                    user_data[user_id]["state"] = "strength"

                elif state == "profile":
                    vk.messages.send(
                        user_id=user_id,
                        message="Выберите направление вкуса:",
                        random_id=0,
                        keyboard=taste_keyboard
                    )
                    user_data[user_id]["state"] = "taste"

                elif state == "fresh":
                    vk.messages.send(
                        user_id=user_id,
                        message="Выберите профиль вкуса:",
                        random_id=0,
                        keyboard=profile_keyboard
                    )
                    user_data[user_id]["state"] = "profile"

                elif state == "result":
                    vk.messages.send(
                        user_id=user_id,
                        message="Добавить холодок❄️?",
                        random_id=0,
                        keyboard=fresh_keyboard
                    )
                    user_data[user_id]["state"] = "fresh"

                else:
                    vk.messages.send(
                        user_id=user_id,
                        message="Главное меню",
                        random_id=0,
                        keyboard=keyboard
                    )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message="Главное меню",
                    random_id=0,
                    keyboard=keyboard
                )

        # ОБРАБОТКА ЛЮБОГО ДРУГОГО ТЕКСТА
        else:
            vk.messages.send(
                user_id=user_id,
                message="Я вас не понял 🫥\nПожалуйста, нажимайте на кнопки ниже.",
                random_id=0,
                keyboard=get_current_keyboard(user_id)
            )
