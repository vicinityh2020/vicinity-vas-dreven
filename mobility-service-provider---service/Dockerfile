FROM python:3.7-rc-alpine
#FROM python:3.8-rc-alpine  - Gives comflict installing cytoolz

RUN mkdir /app

WORKDIR /app

ENV PYTHONPATH .

ADD config /app/config
ADD etc /app/etc
ADD msp /app/msp
ADD ethereum /app/ethereum
ADD requirements.txt /app


RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python -m virtualenv MyEnv
RUN . MyEnv/bin/activate


RUN apk add --no-cache gcc musl-dev python3-dev postgresql-dev
RUN pip3 install -r /app/requirements.txt

RUN pip freeze

CMD python3 msp/__main__.py -dev

