# Mobility service provider - Service
Installation
------------

From the cloned source, execute:

```shell
$ docker-compose up service
```


Running args
-------

Once installed you can run the service using the ``python msp/__main__.py`` command.

```shell
$ python msp/__main__.py -h
usage: __main__.py [-h] [-dev | -qa]

optional arguments:
  -h, --help  show this help message and exit
  -dev        Use development confifuration with in-memory db (DEFAULT)
  -qa         Use remote db with postgres configuration

```


