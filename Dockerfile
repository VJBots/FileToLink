# Created By: Md Sahadat Hossen
# Subscribe YouTube Channel: https://youtube.com/@loveranyanime?si=3sJqjGIXzfI7EyWp
# telegram channel: @ss_anime_box

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "bot.py"]
