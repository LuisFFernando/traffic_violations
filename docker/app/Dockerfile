FROM python:3.10

RUN apt-get update \
    && apt-get install -y gcc python3-dev \
    && apt-get -y install libffi-dev \
    && apt-get -y install python3-dev libpq-dev

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /src

RUN pip3 install poetry

COPY pyproject.toml poetry.lock ./
COPY config ./config
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

COPY docker ./docker
# COPY ./docker/app/entrypoint.sh ./
RUN poetry install --no-root
RUN JWT_SECRET=$(openssl rand -base64 32) && echo "JWT_SECRET=$JWT_SECRET" >> /etc/environment

ENV JWT_SECRET=$JWT_SECRET

CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn config.main:app --host 0.0.0.0 --port 8001"]



# Install Poetry
EXPOSE 8001