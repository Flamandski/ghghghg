import PySimpleGUI as sg
import random
import json
import os
from datetime import datetime

# Файл для сохранения истории
HISTORY_FILE = "task_history.json"

# Предопределённые задачи с категориями
DEFAULT_TASKS = {
    "Учёба": ["Прочитать главу учебника", "Решить 5 задач по математике", "Повторить иностранные слова",
              "Написать конспект лекции"],
    "Спорт": ["Сделать зарядку", "Пробежать 3 км", "Позаниматься йогой 30 минут", "Отжаться 50 раз"],
    "Работа": ["Проверить почту", "Составить план на день", "Провести совещание", "Написать отчёт"]
}


def load_history():
    """Загрузка истории из JSON-файла"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_history(history):
    """Сохранение истории в JSON-файл"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def generate_random_task():
    """Генерация случайной задачи"""
    category = random.choice(list(DEFAULT_TASKS.keys()))
    task = random.choice(DEFAULT_TASKS[category])
    return {"task": task, "category": category, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


def create_layout():
    """Создание интерфейса"""
    layout = [
        [sg.Text("Random Task Generator", font=("Arial", 16), justification="center")],
        [sg.Button("Сгенерировать задачу", size=(20, 2), key="-GENERATE-")],
        [sg.Text("Текущая задача:", font=("Arial", 12))],
        [sg.Text("", size=(50, 2), key="-CURRENT-", relief="sunken")],
        [sg.Text("Фильтр по категории:", font=("Arial", 10))],
        [sg.Combo(["Все", "Учёба", "Спорт", "Работа"], default_value="Все", key="-FILTER-", enable_events=True)],
        [sg.Text("История задач:", font=("Arial", 12))],
        [sg.Listbox(values=[], size=(60, 15), key="-HISTORY-")],
        [sg.Button("Очистить историю", key="-CLEAR-"), sg.Button("Выход", key="-EXIT-")]
    ]
    return layout


def main():
    # Загрузка истории
    history = load_history()

    # Создание окна
    window = sg.Window("Random Task Generator", create_layout(), finalize=True)

    # Обновление списка истории
    update_history_display(window, history)

    # Основной цикл
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break

        elif event == "-GENERATE-":
            # Генерация новой задачи
            new_task = generate_random_task()
            history.append(new_task)
            save_history(history)

            # Отображение текущей задачи
            window["-CURRENT-"].update(f"{new_task['task']} [{new_task['category']}]")

            # Обновление истории
            update_history_display(window, history, values["-FILTER-"])

        elif event == "-FILTER-":
            # Фильтрация истории
            update_history_display(window, history, values["-FILTER-"])

        elif event == "-CLEAR-":
            # Очистка истории с подтверждением
            if sg.popup_yes_no("Очистить всю историю?") == "Yes":
                history.clear()
                save_history(history)
                update_history_display(window, history)

    window.close()


def update_history_display(window, history, filter_category="Все"):
    """Обновление отображения истории с фильтрацией"""
    display_list = []
    for item in history:
        if filter_category == "Все" or item["category"] == filter_category:
            display_list.append(f"{item['timestamp']} | {item['task']} [{item['category']}]")
    window["-HISTORY-"].update(display_list)


if __name__ == "__main__":
    main()
