# To do
# - find a way to have multiple fields for your unique constraints
course_valid = {
  'validator': {
    "$jsonSchema": {
      "bsonType":
      "object",
      'description':
      'A Departments Courses',
      "required":
      ['department', 'courseNumber', 'courseName', 'units', 'description'],
      "additionalProperties":
      False,
      "properties": {
        "_id": {},
        "department": {
          "bsonType": "objectId",
          "description": "Department Name"
        },
        "courseNumber": {
          "bsonType": "int",
          "description": "Course Number",
          "minimum": 100,
          "maximum": 700
        },
        "courseName": {
          "bsonType": "string",
          "description": "Course Name",
          "uniqueItems": True
        },
        "description": {
          "bsonType": "string",
          "description": "Course Description",
          "minLength": 1,
          "maxLength": 80,
          "uniqueItems": True
        },
        "units": {
          "bsonType": "int",
          "description": "Course Description",
          "minimum": 1,
          "maximum": 5
        }
      }
    }
  }
}


