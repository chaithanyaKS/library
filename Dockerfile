FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN mkdir /home/app
WORKDIR /home/app


RUN pip3 install poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

RUN chmod +x ./start-server.sh 
EXPOSE 8000

CMD  ["./start-server.sh"]