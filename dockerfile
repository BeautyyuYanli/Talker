FROM python:3.11
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt waitress

COPY . .
CMD [ "python", "-m", "waitress", "api.index:app" ]