FROM python:3.10-slim

# Ставим git для скачивания конвертера
RUN apt-get update && apt-get install -y git

WORKDIR /app

# Клонируем скрипт конвертера
RUN git clone https://github.com/dobrosketchkun/bionic-reading-epub-converter.git converter

# Устанавливаем зависимости бота и конвертера
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -r converter/requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
