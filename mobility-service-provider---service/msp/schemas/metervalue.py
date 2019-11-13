metervalue_put = {
    "title": "Put the transaction metervalue",
    "type": "object",
    "properties": {
        "idTag": {
            "type": "string"
        },
        "meterValue": {
            "type": "integer"
        },
        "vicinityOid": {
            "type": "string"
        }
    },
    "required": [
        "idTag",
        "meterValue",
        "vicinityOid"

    ]
}