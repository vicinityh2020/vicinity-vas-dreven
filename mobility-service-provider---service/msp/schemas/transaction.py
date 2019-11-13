transaction_start_post = {
    "title": "Post the transaction start",
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

transaction_stop_post = {
    "title": "Post the transaction stop",
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