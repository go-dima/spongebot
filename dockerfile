FROM python:3.8
LABEL Author="DimaG <dima.gonikman@gmail.com>"

RUN apt-get update -y && apt-get upgrade -y
RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY clients-list.dat .
COPY spongebot.py .
COPY base_bot base_bot/
COPY number_parser number_parser/

ENTRYPOINT [ "python" ]
CMD [ "spongebot.py" ]
