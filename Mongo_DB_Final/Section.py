# To Do
# again the constraints with multiple fields ;-;
section_valid = {
  'validator': {
    "$jsonSchema": {
      "bsonType":
      "object",
      'description':
      'A Departments Courses',
      "required": [
        'course', 'sectionNumber', 'semester', 'sectionYear', 'building',
        "room", "schedule", "instructor", "startTime"
      ],
      "additionalProperties":
      False,
      "properties": {
        "_id": {},
        "course": {
          "bsonType": "objectId",
          "description": "The course that offers the section "
        },
        "sectionNumber": {
          "bsonType": "int",
          "description": "Section Number",
          "minimum": 0
        },
        "semester": {
          "description":
          "Section Semester",
          "enum":
          ["Fall", "Spring", "Summer I", "Summer II", "Summer III", "Winter"]
        },
        "sectionYear": {
          "bsonType": "int",
          "description": "Section Year"
        },
        "building": {
          "description":
          "Section Room",
          "enum": [
            "ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET",
            "HSCI", "NUR", "VEC"
          ]
        },
        "room": {
          "bsonType": "int",
          "description": "Section Room",
          "minimum": 1,
          "maximum": 999
        },
        "schedule": {
          "description": "Section Schedule",
          "enum": ["MW", "TuTh", "MWF", "F,", "S"]
        },
        "instructor": {
          "bsonType": "string",
          "description": "Section Prof"
        },
        "startTime": {
          "bsonType":
          "string"  #FIXME needs the constraint (time >= 08:00 and  time <= 17:45) unless convert into in and % by 60
        }
      }
    }
  }
}
