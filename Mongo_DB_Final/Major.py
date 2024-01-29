



major_valid = {'validator': {
    "$jsonSchema": {
        "bsonType": "object",
        'description': 'A Departments Major',
        "required": ['name', 'description'],
        "additionalProperties": False,
        "properties": {
            "_id": {},
            "department": {
                "bsonType": "objectId",
                "description": "Department Name",
            },
            "name": {
                "bsonType": "string",
                "description": "Major Name",
                "uniqueItems": True
            },
            "description": {
                "bsonType": "string",
                "description": "Major Description",
                "minLength": 1,
                "maxLength": 80,
                "uniqueItems": True
            }
        }
    }
}
}
