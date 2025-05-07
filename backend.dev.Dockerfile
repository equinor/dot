FROM python:3.10.12-slim@sha256:7a08d7bfedcbf05d15b2bff8f0c86db6dd06bcbaa74c915d2d5585dbd5ba65b0

COPY ./api /home/api
WORKDIR /home/api

RUN apt update && \
    apt install -y gcc && \
    apt install -y libcairo2-dev pkg-config && \
    apt install -y graphviz && \
    apt install -y graphviz-dev

RUN pip install --upgrade pip && \
    pip install poetry==1.8.5 && \
    poetry config virtualenvs.create false

RUN poetry install

CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "main:app"]
