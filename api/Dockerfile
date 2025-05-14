# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

RUN apt update && \
    apt install -y gcc && \
    apt install -y libcairo2-dev pkg-config && \
    apt install -y graphviz && \
    apt install -y graphviz-dev

RUN pip install --upgrade pip && \
    pip install poetry==1.8.5 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/

# Install project dependencies
RUN poetry install --no-root --only main

# Copy the rest of the application code
COPY . /code/

WORKDIR /code

# Add a new group "non-root-group" with group id 1001 and user "non-root-user" with the same id
RUN groupadd --gid 1001 non-root-group && \
    useradd --uid 1001 --gid 1001 --create-home non-root-user

USER 1001

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
