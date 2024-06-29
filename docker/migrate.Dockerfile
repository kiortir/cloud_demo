FROM python:3.12-slim as base

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100    

RUN apt update && python3 -m pip install --user pipx
RUN python3 -m pipx ensurepath --force

ENV POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1
RUN python3 -m pipx install poetry==$POETRY_VERSION

FROM base as poetry
WORKDIR /app

COPY pyproject.toml /app
RUN python3 -m pipx run poetry install --no-interaction --no-ansi

FROM base as setup

WORKDIR /app
COPY --from=poetry /app/.venv ./.venv
# COPY ./cloud /app/cloud

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/cloud:$PYTHONPATH"


COPY ./alembic.ini /app
COPY ./alembic/ /app/alembic/