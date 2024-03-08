FROM python:3.11.8-slim AS builder

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /opt/backend

RUN  pip install --no-cache-dir --upgrade pip \
     && apt-get -y update && apt-get -y install gcc libpq-dev python3-dev \
     && apt-get install -y --no-install-recommends curl \
     && curl -sSL https://install.python-poetry.org | python3 -

COPY . /opt/backend
RUN poetry install --no-dev

FROM python:3.11.8-slim AS runtime

RUN mkdir --parents /opt/backend
COPY --from=builder /opt/backend/.venv /opt/backend/.venv
COPY --from=builder /opt/backend/bin /opt/backend/bin
COPY --from=builder /opt/backend/lib /opt/backend/lib

WORKDIR /opt/backend
CMD [".venv/bin/python", "-m", "bin.web"]
