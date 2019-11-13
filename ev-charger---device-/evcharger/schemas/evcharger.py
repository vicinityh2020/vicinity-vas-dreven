evcharger_update = {
    "title": "Update Evcharger",
    "type": "object",
    "properties": {
        "lastStartTransaction": {
            "type": "integer"
        },
        "lastStopTransaction": {
            "type": "integer"
        },
        "meterValue": {
            "type": "number"
        },
        "status": {
            "type": "string"
        }
    },
    "minProperties": 1,
    "additionalProperties": False
}
