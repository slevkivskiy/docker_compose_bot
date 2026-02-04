# 1. Беремо за основу легкий Linux з уже встановленим Python
FROM python:3.10-slim

# 2. Створюємо папку всередині контейнера
WORKDIR /app

# 3. Копіюємо файл списку бібліотек
COPY requirements.txt .

# 4. Встановлюємо бібліотеки (прямо всередині контейнера)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копіюємо весь твій код у контейнер
COPY . .

# 6. Команда, яка запустить бота
CMD ["python", "my_firstt_script.py"]
