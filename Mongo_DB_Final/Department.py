
dept_valid = {'validator': {
    "$jsonSchema": {
        "bsonType": "object",
        'description': 'A University Department',
        "required": ['abbreviation', 'building', 'chairName', 'description', 'name', 'office'],
        "additionalProperties": False,
        "properties": {
            "_id": {},
            "name": {
                "bsonType": "string",
                "description": "Department Name",
                "uniqueItems": True
            },

            "abbreviation": {
                "bsonType": "string",
                "description": "Department Abbreviation",
                "minLength": 1,
                "maxLength": 6,
                "uniqueItems": True
            },

            "chairName": {
                "bsonType": "string",
                "description": "Department Chair Name",
                "minLength": 1,
                "maxLength": 80,
                "uniqueItems": True
            },

            "building": {
                "description": "building name for the department",
                "enum": ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
            },

            "office": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Department Office Number"
            },

            "description": {
                "bsonType": "string",
                "description": "Department Description",
                "minLength": 1,
                "maxLength": 80,
                "uniqueItems": True
            }
        }
    }
}
}

'''student_validator ={
'validator': {
'$jsonSchema': {
'bsonType': "object",
'description': 'A person attending university to earn a degree or credential',
'required': ['last_name', 'first_name' ,'e_mail'],
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
'e_mail': {
'bsonType': 'string',
'description': 'electronic mail address of the student',
'minLength': 10,
'maxLength': 255
}
}
}
}
}
'''
