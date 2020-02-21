FROM python:3.7-rc-alpine

RUN mkdir /app

WORKDIR /app

ENV PYTHONPATH .

ADD main.py /app
ADD requirements.txt /app

RUN pip install virtualenv
RUN python -m virtualenv MyEnv
RUN . MyEnv/bin/activate


RUN pip install -r /app/requirements.txt

CMD python3 main.py

