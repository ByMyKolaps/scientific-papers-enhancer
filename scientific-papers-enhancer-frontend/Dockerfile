FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Указываем команду для запуска
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]