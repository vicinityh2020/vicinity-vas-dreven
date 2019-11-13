FROM python:3.8-rc-alpine

RUN mkdir /app

WORKDIR /app

ENV PYTHONPATH .

ADD config /app/config
ADD etc /app/etc
ADD evcharger /app/evcharger
ADD objects /app/objects
ADD requirements.txt /app

RUN apk add --no-cache gcc musl-dev python3-dev postgresql-dev
RUN pip3 install virtualenv
RUN python3 -m virtualenv MyEnv
RUN . MyEnv/bin/activate
RUN pip3 install -r /app/requirements.txt

CMD python3 evcharger/__main__.py -dev

