pricing_contract_post = {
    "title": "Post pricing contract",
    "type": "object",
    "properties": {
        "initial_price": {
            "type": "integer",
            "exclusiveMinimum": 0
        }
    },
    "required": [
        "initial_price"

    ]
}