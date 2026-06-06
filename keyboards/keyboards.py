"""
Модуль для инициализации клавиатур чат-бота ВКонтакте.

Содержит все интерактивные меню (кнопки) для взаимодействия с пользователем:
выбор крепости, вкусовых направлений, наличия холодка и подтверждения действий.
"""

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# --- Главные меню бота ---

# Стартовая клавиатура для приветственного сообщения
_start_kb = VkKeyboard(one_time=False)
_start_kb.add_button("Начать", color=VkKeyboardColor.PRIMARY)
start_keyboard: str = _start_kb.get_keyboard()

# Основная клавиатура после старта
_main_kb = VkKeyboard(one_time=False)
_main_kb.add_button("Подобрать микс", color=VkKeyboardColor.PRIMARY)
keyboard: str = _main_kb.get_keyboard()

# --- Клавиатуры для этапов подбора микса ---

# Выбор крепости кальяна
_strength_kb = VkKeyboard(one_time=True)
_strength_kb.add_button("Лёгкая", color=VkKeyboardColor.POSITIVE)
_strength_kb.add_button("Средняя", color=VkKeyboardColor.PRIMARY)
_strength_kb.add_button("Крепкая", color=VkKeyboardColor.NEGATIVE)
_strength_kb.add_line()
_strength_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
strength_keyboard: str = _strength_kb.get_keyboard()

# Выбор категории вкуса
_taste_kb = VkKeyboard(one_time=True)
_taste_kb.add_button("Фруктовый", color=VkKeyboardColor.POSITIVE)
_taste_kb.add_button("Ягодный", color=VkKeyboardColor.PRIMARY)
_taste_kb.add_line()
_taste_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
taste_keyboard: str = _taste_kb.get_keyboard()

# Выбор профиля вкуса (кислый / сладкий)
_profile_kb = VkKeyboard(one_time=True)
_profile_kb.add_button("Кислый", color=VkKeyboardColor.PRIMARY)
_profile_kb.add_button("Сладкий", color=VkKeyboardColor.POSITIVE)
_profile_kb.add_line()
_profile_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
profile_keyboard: str = _profile_kb.get_keyboard()

# Выбор наличия холодка
_fresh_kb = VkKeyboard(one_time=True)
_fresh_kb.add_button("Да", color=VkKeyboardColor.POSITIVE)
_fresh_kb.add_button("Нет", color=VkKeyboardColor.NEGATIVE)
_fresh_kb.add_line()
_fresh_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
fresh_keyboard: str = _fresh_kb.get_keyboard()

# --- Финальные клавиатуры результатов ---

# Клавиатура для подтверждения критериев перед созданием микса
_confirm_kb = VkKeyboard(one_time=True)
_confirm_kb.add_button("Подтвердить", color=VkKeyboardColor.POSITIVE)
_confirm_kb.add_line()
_confirm_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
confirm_keyboard: str = _confirm_kb.get_keyboard()

# Клавиатура после успешного вывода микса
_result_kb = VkKeyboard(one_time=False)
_result_kb.add_button("Подобрать микс", color=VkKeyboardColor.PRIMARY)
_result_kb.add_line()
_result_kb.add_button("Назад", color=VkKeyboardColor.SECONDARY)
result_keyboard: str = _result_kb.get_keyboard()
