# Device adapter - EVCharger
Installation
------------

From the cloned source, execute:

```shell
$ docker-compose up
```
3 services:

- Open gateway API (OGWAPI)

- Vicinity Agent

- Device adapter (EVCharger)

Requests should be executed towards Vicinity Agent (10.5.0.7:9997)

**[GET] - /agent/remote/objects/{oid}/properties/{pid}** -> Gets value of Property ID {pid} from Object ID {oid}



**[PUT] - /agent/remote/objects/{oid}/properties/{pid}** -> Changes value of Property ID {pid} from Object ID {oid}