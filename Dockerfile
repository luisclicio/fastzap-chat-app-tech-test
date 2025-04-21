FROM python:3.13-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.5.28 /uv /uvx /bin/
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /app
EXPOSE 8000

FROM base AS dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
ENV PATH="/app/.venv/bin:$PATH"
COPY . .

FROM dependencies AS development
ENV DEBUG=1
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM dependencies AS celery
CMD [ "celery", "-A", "config.celery", "worker", "--loglevel=info" ]

FROM dependencies AS production
ENV DEBUG=0
# Collect static files
RUN python manage.py collectstatic --noinput
CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application" ]
