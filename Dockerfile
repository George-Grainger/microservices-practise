FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && pip install --no-cache-dir --upgrade pip

# Want requirements in seperate layer so if application code changes  
# we can still use cached requirements later - don't need to recreate layer.
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]