# 🐾 Selenium Tests for PetFriends

## 📌 Описание проекта
Этот проект содержит автоматизированные тесты для веб-приложения [PetFriends](https://petfriends.skillfactory.ru).  
Тесты написаны с использованием **Python, Selenium и Pytest**.

## 🛠️ Используемые технологии
- Python 3.x
- Selenium WebDriver
- Pytest
- WebDriverWait (явные ожидания)
- implicitly_wait (неявные ожидания)

## 🚀 Установка и запуск тестов

### 1️⃣ Установите зависимости
```bash
pip install -r requirements.txt

2️⃣ Запуск тестов

pytest main.py --verbose
📝 Описание тестов
✅ Авторизация
✅ Проверка отображения всех питомцев
✅ Проверка списка "Мои питомцы"
✅ Проверка наличия фото, имен и описаний
✅Проверка уникальности имен питомцев
✅ Отсутствие дубликатов питомцев

📂 Структура
bash
Копировать
Редактировать
selenium-pet-tests/
│── main.py           # Основной файл с тестами
│── requirements.txt  # Список зависимостей
│── README.md         # Описание проекта
└── tests/            # Каталог с тестами

