# To do
# multiple constraints again so that the same student cannot enroll in the same section 
studentsection_valid = {
    'validator': {
        '$jsonSchema': {
            'bsonType': "object",
            'description': 'The link connecting a student to a major the relationship is one major to many students',
            'required': ['student', 'section'],
            'additionalProperties': False,
            'properties': {
                '_id': {},
                'student': {
                    'bsonType': 'objectId',
                    'description': 'Student Id'
                },
                'section': {
                    'bsonType': 'objectId',
                    'description': 'Section Id'
                }
            }
        }
    }
}
