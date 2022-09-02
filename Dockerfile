FROM python:3.8 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /src

FROM base as poetry
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install poetry==1.1.12
COPY poetry.lock pyproject.toml /src/
RUN poetry export -o requirements.txt

FROM python:3.8.10-slim as runtime
COPY --from=poetry /src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
WORKDIR /src

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
COPY . /src
EXPOSE 3000
CMD ["uvicorn", "--proxy-headers", "--host=0.0.0.0", "--port=3000", "src.main:app"]