studentmajor_valid = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'The link connecting a student to a major the relationship is one major to many students',
            'required': ['student', 'major',"declarationDate"],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'student': {
                    'bsonType': 'objectId',
                    'description': 'Student Id',
                    "uniqueItems": True
                },
                'major': {
                    'bsonType': 'objectId',
                    'description': 'Major Id'
                },
                "declarationDate":{
                    "bsonType": "string",  # so not sure how to return this as a type:date
                    "description":"The recorded date that a student enrolled in a major, the time posted is the time a student object is created"
                }
            }
        }
    }
}
