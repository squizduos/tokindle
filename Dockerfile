FROM python:3.8-slim

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install --no-cache-dir pipenv && \
    pipenv install

COPY . .

EXPOSE 8000

CMD [ "pipenv", "run", "python", "app.py" ]
