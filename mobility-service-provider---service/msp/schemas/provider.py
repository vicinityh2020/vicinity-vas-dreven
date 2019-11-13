p_update = {
    "title": "Update Provider",
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        }
    }
}

p_post = {
    "title": "Post Provider",
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        }
    },
    "required": [
        "name"
    ]
}