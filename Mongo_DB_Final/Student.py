student_valid = {
  'validator': {
    '$jsonSchema': {
      'bsonType': "object",
      'description':
      'A person attending university to earn a degree or credential',
      'required': ['last_name', 'first_name', 'email'],
      'additionalProperties': False,
      'properties': {
        '_id': {},
        'last_name': {
          'bsonType': 'string',
          'description': 'surname of the student',
          'minLength': 3,
          'maxLength': 80
        },
        'first_name': {
          'bsonType': 'string',
          'description': 'given name of the student',
          'minLength': 3,
          'maxLength': 80
        },
        'email': {
          'bsonType': 'string',
          'description': 'electronic mail address of the student',
          'minLength': 10,
          'maxLength': 255,
          'uniqueItems':True
        }
      }
    }
  }
}
