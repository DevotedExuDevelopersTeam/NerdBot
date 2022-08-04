FROM python:3.10-bullseye
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry install
COPY . .
CMD ["poetry", "run", "python3", "main.py"]
