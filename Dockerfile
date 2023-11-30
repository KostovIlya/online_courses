FROM python:3.11 AS builder

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry==1.5.0 \
    && poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.11

WORKDIR /app

COPY --from=builder requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
