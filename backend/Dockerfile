FROM python:3.11.8-slim AS builder

COPY . /opt/backend
WORKDIR /opt/backend

RUN poetry install --no-dev

FROM python:3.11.8-slim AS runtime

RUN mkdir --parents /opt/backend
COPY --from=builder /opt/backend/.venv /opt/backend/.venv
COPY --from=builder /opt/backend/bin /opt/backend/bin
COPY --from=builder /opt/backend/lib /opt/backend/lib

WORKDIR /opt/backend
CMD [".venv/bin/python", "-m", "bin.web"]
