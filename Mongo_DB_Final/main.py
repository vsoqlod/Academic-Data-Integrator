import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from datetime import datetime
from pymongo import errors
from Department import dept_valid
from Major import major_valid
from Course import course_valid
from Student import student_valid
from Section import section_valid
from StudentMajor import studentmajor_valid
from StudentSection import studentsection_valid
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from menu_definitions import semester_menu
from menu_definitions import schedule_menu
from menu_definitions import enrollment_menu
from menu_definitions import grade_menu
'''TO DO LIST:
        Find a way to make a list unique constraint where, building and office are unique as a pair
        Find a way to merge inheriting tables : see MongoDB Joins
        Define search, add, delete and list functions
            Make sure that the delete function deletes children of the target, for instance, if depts go so do majors and courses for that dept: then we could do a search for all courses and majors with that dept _id and drop them too
            Also the stupid enrollments issue where we enroll students ew: multiple id lookups then'''


def add(db):
  """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
  add_action: str = ''
  while add_action != add_menu.last_action():
    add_action = add_menu.menu_prompt()
    exec(add_action)


def delete(db):
  """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
  delete_action: str = ''
  while delete_action != delete_menu.last_action():
    delete_action = delete_menu.menu_prompt()
    exec(delete_action)


def list_objects(db):
  """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
  list_action: str = ''
  while list_action != list_menu.last_action():
    list_action = list_menu.menu_prompt()
    exec(list_action)


def add_department(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    department_validator = {
        'validator': {
            '$jsonSchema': {
                'bsonType': "object",
                'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
                'properties': {
                    'name': {
                        'bsonType': 'string',
                        'description': 'Name of department',
                        'minLength': 10,
                        'maxLength': 50
                    },
                    'abbreviation': {
                        'bsonType': 'string',
                        'description': 'Department abbreviation',
                        'maxLength': 6
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'description': 'A faculty member in the department',
                        'maxLength': 80
                    },
                    'building': {
                        'bsonType': 'string',
                        'description': 'The building that department located in CSULB',
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
                    },
                    'office': {
                        'bsonType': 'int',
                        'description': 'The office number in integer type',
                        'minLength': 0
                    },
                    "description": {
                        "bsonType": "string",
                        "description": 'The description of department',
                        "minLength": 10,
                        "maxLength": 80
                    }

                }
            }
        }
    }
    db.command('collMod', 'departments', **department_validator)
    collection = db["departments"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building: bool = False
    unique_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while not unique_name or not unique_abbreviation or not unique_chair_name or not unique_building or not unique_office:
        name = input("Department name--> ")
        abbreviation = input("Abbreviation--> ")
        chair_name = input("Chair name--> ")
        building = input("Building name--> ")
        office = int(input("Office--> "))
        description = input("Description--> ")

        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0

        if not unique_name:
            print("We already have a department with that name.  Try again.")
        if unique_name:
            abbreviation_count: int = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that department abbreviation.  Try again.")
            if unique_abbreviation:
                chair_name_count = collection.count_documents({"chair_name": chair_name})
                unique_chair_name = chair_name_count == 0
                if not unique_chair_name:
                    print("We already have a department with that chair name.  Try again.")
                if unique_chair_name:
                    building_count: int = collection.count_documents({"building": building})
                    unique_building = building_count == 0
                    if not unique_building:
                        print("We already have a department with that same occupied building. Try again.")
                    if unique_chair_name:
                        location_count = collection.count_documents({"building": building, "office": office})
                        unique_location = location_count == 0
                    if not unique_location:
                        print("The location is occupied by a different department")

    department = {
        "name": name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description
    }
    try:
        results = collection.insert_one(department)
        print("Department added successfully.")

    except Exception as user:
        print(f"Failed to add the department because violates one or more of your constraints, pleas try again. INPUT: {user}")
        add_department(db)


def add_course(db):
    course_validator = {
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["department_abbreviation", "course_number", "name", "description", "units"],
                "properties": {
                    "course_number": {
                        "bsonType": "int",
                        "minimum": 100,
                        "maximum": 700,
                        "description": "Number of the course"
                    },
                    "units": {
                        "bsonType": "int",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Number of units for a given course"
                    }
                }
            }
        }
    }
  
    db.command('collMod', 'courses', **course_validator)
    course_col = db["courses"]
    department_col = db["departments"]
    department = select_department(db)
    course_number: int = -1
    name: str = ''
    description = ''
    units = -1

    name = input("Course full name--> ")
    course_number = int(input("Course number--> "))
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))

    course = {
        "department_abbreviation": department['abbreviation'],
        "name": name,
        "course_number": course_number,
        "description": description,
        "units": units,
    }
    try:
        result = course_col.insert_one(course)

        department_col.update_one(
            {"abbreviation": department['abbreviation']},
            {"$addToSet": {"courses": course['course_number']}}
        )
        print("Course added successfully!")
    except Exception as e:
        print(f"Failed to add department, please check your input: {e}")
        add_course(db)


def add_section(db):
    section_validator = {
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["department_abbreviation", "course_number", "number", "semester", "year", "building",
                             "room", "schedule", "startTime", "instructor"],
                "properties": {
                    "semester": {
                        "bsonType": "string",
                        "maxLength": 10,
                        "description": "Season of an academic year",
                        "enum": ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                    },
                    "year": {
                        "bsonType": "int",
                        "maxLength": 5,
                        "description": "Current year"
                    },
                    "building": {
                        "bsonType": "string",
                        "description": "The building that the department is located at",
                        "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
                    },
                    "room": {
                        "bsonType": "int",
                        "minLength": 1,
                        "maxLength": 999,
                        "description": "The room the class, assume no ten story buildings on campus"
                    },
                    "schedule": {
                        "bsonType": "string",
                        "maxLength": 10,
                        "description": "Days of the week for a given class",
                        "enum": ['MW', 'TuTh', 'MWF', 'F', 'S']
                    }
                }
            }
        }
    }

    db.command('collMod', 'sections', **section_validator)
    print('Please input the course that the section belongs to:')
    course = select_course(db)
    collection = db["sections"]

    sectionNumber = 0
    semester = ''
    sectionYear = 0
    building = ''
    room = 0
    schedule = ''
    startTime = datetime(1970, 1, 1, 0, 0, 0)
    instructor = ''

    sectionNumber = int(input('What is the section number -->'))
    semester = semester_menu.menu_prompt()
    sectionYear = int(input('Which year is this section? --> '))
    building = input('Which building is this section? --> ')
    room = int(input(f'Which room of building {building} is this section offered in? --> '))
    schedule = schedule_menu.menu_prompt()
    start_hour = None
    while start_hour not in range(8, 20):
        start_hour = int(input('Start hours (8 to 19) --> '))
    start_minute = None
    while start_minute not in range(60):
        start_minute = int(input('Start minutes (0 to 59) --> '))
    startTime = datetime(sectionYear, 1, 1, start_hour, start_minute, 0)
    instructor = input('Instructor full name --> ')

    section = {
        "department_abbreviation": course['department_abbreviation'],
        "course_number": course['course_number'],
        "number": sectionNumber,
        "semester": semester,
        "year": sectionYear,
        "building": building,
        "room": room,
        "schedule": schedule,
        "startTime": startTime,
        "instructor": instructor,
    }
    try:
        results = collection.insert_one(section)
        db["courses"].update_one(
            {"department_abbreviation": course['department_abbreviation']},
            {"$addToSet": {"sections": sectionNumber}}
        )
        print("Course added successfully!")
    except Exception as e:
        print(f"Failed to add section, please check your input: {e}")
        add_section(db)

def add_major(db):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    department_col = db["departments"]
    collection = db["majors"]
    print("Which department offers this major?")
    department = select_department(db)
    unique_name = False
    name = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count = collection.count_documents({"name": name, "department_abbreviation": department['abbreviation']})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major = {
        "department_abbreviation": department['abbreviation'],
        "name": name,
        "description": description,
    }
    try:
        results = collection.insert_one(major)
        department_col.update_one(
            {"abbreviation": department['abbreviation']},
            {"$addToSet": {"majors": major['name']}}
        )
        print("Major added successfully!")
    except Exception as e:
        print(f"Failed to add major, please check your input: {e}")
        add_major(db)

def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    lastName: str = ''
    firstName: str = ''
    email: str = ''

    lastName = input("Student last name--> ")
    firstName = input("Student first name--> ")
    email = input("Student e-mail address--> ")

    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    try:
        results = collection.insert_one(student)
    except Exception as e:
        print(f"Failed to add a student because {e}")
        add_student(db)
      

def add_enrollment(db):
    enrollments = db["enrollments"]
    students_col = db["students"]

    print("What student to enroll:")
    student = select_student(db)
    print("Pick section you want this student to enroll in?")
    section = select_section(db)
    enrollment_type = enrollment_menu.menu_prompt()

    # Check if the student is already enrolled in the section
    existing_enrollment = enrollments.find_one({"section": section["_id"], "student": student["_id"]})
    if existing_enrollment:
        print("Error: Student is already enrolled in this section.")
        return

    enrollment = {
        "department_abbreviation": section['department_abbreviation'],
        "course_number": section['course_number'],
        "student": student['_id'],
        "section": section['_id'],
        "enrollment_type": enrollment_type,
        "application_date": datetime.now()
    }

    if enrollment_type == "lettergrade":
        min_satisfactory = grade_menu.menu_prompt()
        enrollment["min_satisfactory"] = min_satisfactory
    elif enrollment_type != "passfail":
        print("Error: Invalid enrollment type.")
        return


    try:
        result = enrollments.insert_one(enrollment)
        if result.acknowledged:
            students_col.update_one(
                {"_id": student["_id"]},
                {"$addToSet": {"sections": section['number']}}
            )
            print("Enrollment successful.")
    except Exception as e:
        print(f"Error: Enrollment failed.: {e}")
        add_enrollment(db)


def add_student_major(db):
    student = select_student(db)
    major = select_major(db)
    declaration_date = datetime.now()
    try:
        result = db.students.update_one(
            {"_id": student["_id"], "majors.name": {"$ne": major['name']}},
            {"$push": {"majors": {"$each": [{"name": major['name'], "declaration_date": declaration_date}]}}}
        )
        if result.modified_count > 0:
            print("Major added successfully!")
        else:
            print("Student already has this major.")
    except Exception as e:
        print(f"Failed to add major to a student, please check your input: {e}")
        add_student_major(db)

# select
def select_department(db):
    """
    Prompt the user for a specific department by the department abbreviation.
    :param db: The MongoDB database for departments.
    :return: The selected department.
    """
    found = False
    abbreviation = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count = db.count_documents({"abbreviation": abbreviation})
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation. Try again.")
    return_department = db.find_one({"abbreviation": abbreviation})
    return return_department

def select_course(db):
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param db: The MongoDB database object.
    :return: The selected course.
    """
    found = False
    department_abbreviation = ''
    course_number = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count = db["courses"].count_documents({
            "departmentAbbreviation": department_abbreviation,
            "courseNumber": course_number
        })
        found = name_count == 1
        if not found:
            print("No course by that number in that department. Try again.")
    course = db["courses"].find_one({
        "departmentAbbreviation": department_abbreviation,
        "courseNumber": course_number
    })
    return course


def select_student(db):
    """
    Select a student by the combination of the last and first name.
    :param db: The MongoDB database object.
    :return: The selected student.
    """
    found = False
    last_name = ''
    first_name = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count = db["students"].count_documents({
            "lastName": last_name,
            "firstName": first_name
        })
        found = name_count == 1
        if not found:
            print("No student found by that name. Try again.")
    student = db["students"].find_one({
        "lastName": last_name,
        "firstName": first_name
    })
    return student


def select_section(db):
    """
    Select a section by the primary key.
    :param db: The MongoDB database object.
    :return: The selected section.
    """
    found = False
    while not found:
        print('Please provide the course that this section belongs to:')
        course = select_course(db)
        section_number = int(input('What is the section number -->'))
        semester = semester_menu.menu_prompt()
        section_year = int(input('Which year is this section offered in? --> '))
        pk_count = db["sections"].count_documents({
            "course.departmentAbbreviation": course["departmentAbbreviation"],
            "course.courseNumber": course["courseNumber"],
            "sectionNumber": section_number,
            "sectionYear": section_year,
            "semester": semester
        })
        found = pk_count == 1
        if not found:
            print("No section found by that course, section number, semester, and year. Try again.")
    section = db["sections"].find_one({
        "course.departmentAbbreviation": course["departmentAbbreviation"],
        "course.courseNumber": course["courseNumber"],
        "sectionNumber": section_number,
        "sectionYear": section_year,
        "semester": semester
    })
    return section

def select_major(db):
    """
    Select a major by its name.
    :param db: The MongoDB database object.
    :return: The selected major.
    """
    found = False
    name = ''
    while not found:
        name = input("Major's name--> ")
        name_count = db["majors"].count_documents({"name": name})
        found = name_count == 1
        if not found:
            print("No major found by that name. Try again.")
    major = db["majors"].find_one({"name": name})
    return major

# list
def list_department(db):
    departments = db["departments"].find().sort("abbreviation", 1)
    for department in departments:
        print(department)

def list_course(db):
    """
    List all courses currently in the database.
    :param db: The MongoDB database object.
    :return: None
    """
    courses = db["courses"].find().sort("courseNumber", 1)
    for course in courses:
        print(course)

def list_student(db):
    """
    List all students currently in the database.
    :param db: The MongoDB database object.
    :return: None
    """
    students = db["students"].find().sort([("lastName", 1), ("firstName", 1)])
    for student in students:
        print(student)

def list_major(db):
    """
    List all majors in the database.
    :param db: The MongoDB database object.
    :return: None
    """
    majors = db["majors"].find().sort("departmentAbbreviation", 1)
    for major in majors:
        print(major)

def list_section(db):
    """
    List all sections in the database.
    :param db: The MongoDB database object.
    :return: None
    """
    sections = db["sections"].find().sort([
        ("departmentAbbreviation", 1),
        ("courseNumber", 1),
        ("sectionNumber", 1),
        ("sectionYear", 1),
        ("semester", 1)
    ])
    for section in sections:
        print(section)

def list_student_major(db):
    student = select_student(db)
    recs = db["students"].aggregate([
        {"$match": {"studentID": student["studentID"]}},
        {"$lookup": {
            "from": "studentmajors",
            "localField": "studentID",
            "foreignField": "studentId",
            "as": "majors"
        }},
        {"$unwind": "$majors"},
        {"$lookup": {
            "from": "majors",
            "localField": "majors.majorName",
            "foreignField": "name",
            "as": "major"
        }},
        {"$unwind": "$major"},
        {"$project": {
            "lastName": 1,
            "firstName": 1,
            "majorName": "$major.name",
            "majorDescription": "$major.description"
        }}
    ])
    for stu in recs:
        print(f"Student name: {stu['lastName']}, {stu['firstName']}, Major: {stu['majorName']}, "
              f"Description: {stu['majorDescription']}")


def list_major_student(db):
    major = select_major(db)
    recs = db["majors"].aggregate([
        {"$match": {"name": major["name"]}},
        {"$lookup": {
            "from": "studentmajors",
            "localField": "name",
            "foreignField": "majorName",
            "as": "students"
        }},
        {"$unwind": "$students"},
        {"$lookup": {
            "from": "students",
            "localField": "students.studentId",
            "foreignField": "studentID",
            "as": "student"
        }},
        {"$unwind": "$student"},
        {"$project": {
            "lastName": "$student.lastName",
            "firstName": "$student.firstName",
            "majorName": "$name",
            "majorDescription": "$description"
        }}
    ])
    for stu in recs:
        print(f"Student name: {stu['lastName']}, {stu['firstName']}, Major: {stu['majorName']}, "
              f"Description: {stu['majorDescription']}")

def list_enrollment(db):
    recs = db["enrollments"].find().sort([
        ("departmentAbbreviation", 1),
        ("courseNumber", 1),
        ("sectionYear", 1)
    ])
    for rec in recs:
        print(rec)

# delete
def delete_department(db):
    """
    Delete a department from the database if its courses array is empty.
    :param db:  The current database connection.
    :return:    None
    """
    department = select_department(db)
    departments = db["departments"]

    if len(department.get('courses', [])) > 0:
        print("Cannot delete department, first delete its courses.")
        return

    if len(department.get('majors', [])) > 0:
        print("Cannot delete department, first delete its majors.")
        return

    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments.")


def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    departments = db["departments"]
    # Check if there are any sections associated with the course
    sections_count = db["sections"].count_documents({"course_number": course["course_number"]})
    if sections_count > 0:
        print("Cannot delete course, first delete its sections.")
        return
    # Delete the course and remove its course number from the department's courses array
    result = courses.delete_one({"_id": course["_id"]})
    if result.deleted_count == 1:
        departments.update_one(
            {"abbreviation": course["department_abbreviation"]},
            {"$pull": {"courses": course["course_number"]}}
        )
        print("Course deleted successfully.")
    else:
        print("Error: Course not found.")


def delete_section(db):
    section = select_section(db)
    enrollments_col = db["enrollments"]
    sections_col = db["sections"]
    count = enrollments_col.count_documents({"section": section['_id']})
    if count > 0:
        print("Cannot delete section, first delete its enrollments.")
        return
    deleted = sections_col.delete_one({"_id": section["_id"]})
    if deleted.deleted_count == 1:
        print(f"We just deleted: {deleted.deleted_count} section.")
    else:
        print("Error: Section not deleted.")


def delete_major(db):
    major = select_major(db)
    students = db["students"]
    result = students.count_documents({"majors.name": major["name"]})
    if result == 0:
        db["departments"].update_one(
            {"abbreviation": major["department_abbreviation"]},
            {"$pull": {"majors": major["name"]}}
        )
        db["majors"].delete_one({"_id": major["_id"]})
        print(f"{major['name']} major has been deleted because it was not used by any student.")
    else:
        print('Cannot delete major, first delete its students.')

def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    students = db["students"]
    # check if student has any sections
    if "sections" in student and student["sections"]:
        print("Cannot delete student, first delete its enrollments.")
        return
    # check if student has any majors
    if "majors" in student and student["majors"]:
        print("Cannot delete student, first delete its majors.")
        return
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} students.")

def delete_student_major(db):
    student = select_student(db)
    major = select_major(db)
    students = db["students"]
    if students is not None and student.get('sections'):
        print("Cannot delete student, first delete its enrollments.")
        return
    students.update_one({"_id": student["_id"]}, {"$pull": {"majors": {"name": major["name"]}}})
    print(f"Successfully deleted major: {major['name']} from student: {student['first_name']} {student['last_name']}.")


def delete_enrollment(db):
    enrollments = db["enrollments"]
    students = db["students"]

    # select the enrollment to delete
    student = select_student(db)
    section = select_section(db)
    enrollment = enrollments.find_one({"student": student["_id"], "section": section["_id"]})
    if not enrollment:
        print("Error: Enrollment not found.")
        return

    # delete the enrollment
    result = enrollments.delete_one({"_id": enrollment["_id"]})
    if result.deleted_count == 1:
        print("Enrollment deleted.")
    else:
        print("Error: Failed to delete enrollment.")

    # update the student's sections array
    students.update_one(
        {"_id": student["_id"]},
        {"$pull": {"sections": section["number"]}}
    )



def dept_id(abbreviation: str):
  # honestly, the project is gratuitous since I just ask for
  # the _id from the resulting dict.
  collection = db["Departments"]
  found = collection.find_one({"abbreviation": abbreviation},
                              {"_id": 1})["_id"]
  return found

def course_id(name: str):
    collection = db["Courses"]
    found = collection.find_one({"courseName": name}, {"_id": 1})["_id"]
    return found

def student_id(last_name: str, first_name:str):
    collection = db["Students"]
    found = collection.find_one({"last_name": last_name, "first_name":first_name}, {"_id": 1})["_id"]
    return found

def major_id(department, name:str):
    collection = db["Majors"]
    found = collection.find_one({"department": department, "name":name}, {"_id": 1})["_id"]
    return found

def section_id(course_id , section_num:int):
    collection = db["Sections"]
    found = collection.find_one({"course": course_id, "sectionNumber": section_num}, {"_id": 1})["_id"]
    return found



def drop_collection(schema_ref, collection_name: str):
  """
    Little utility for dropping collections and letting the user know.
    :param schema_ref:          The reference to the current schema.
    :param collection_name:     The name of the collection to drop within that schema.
    :return:                    None
    """
  if collection_name in schema_ref.list_collection_names():
    print(f'Dropping collection: {collection_name}')
    schema_ref[collection_name].drop()


if __name__ == '__main__':
  # CHANGE THIS TO YOUR OWN DATABASE
  cluster = "mongodb+srv://jaebumjang01:V2ss2931@cluster0.7xrzh4c.mongodb.net/?retryWrites=true&w=majority"
  print(f'Cluster:{cluster}')
  client = MongoClient(cluster)
  print(
    f"The current database names in this cluster are: {client.list_database_names()}"
  )

  db = client['Final_MongoDB']  # Create pointer to the Final MongoDB database
  collections = db.list_collection_names()  # just a check to ensure it worked.
  print(f"The current collections in the Schema database are: {collections}")

  # \\\\\\\\\\\\\\\\\\\TEST BENCH AND BOILER PLATE\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # DROPPING LIST
  drop_collection(db, 'Departments')
  drop_collection(db, "Majors")
  drop_collection(db, "Courses")
  drop_collection(db, "Students")
  drop_collection(db, "Sections")
  drop_collection(db, "StudentMajor")
  drop_collection(db, "StudentSection")


  # CREATION LIST

  db.create_collection("Departments", **dept_valid) # works
  db.create_collection("Majors", **major_valid)
  db.create_collection("Courses", **course_valid)
  db.create_collection("Students", **student_valid)
  db.create_collection("Sections", **section_valid)
  db.create_collection("StudentMajor", **studentmajor_valid)
  db.create_collection("StudentSection", **studentsection_valid)



  collections = db.list_collection_names()
  dept_test1 = {
      "name": "department1",
      "abbreviation": "DEPT1",
      "chairName": "DEPT1",
      "building": "ANAC",
      "office": 1,
      "description": "Department1 Test Description"
  }
  db['Departments'].insert_one(dept_test1)

  major_test1 = {"department": dept_id("DEPT1"),
                 "name": 'Major1',
                 "description": "Major 1 description"
                 }
  db['Majors'].insert_one(major_test1)

  course_test1 = {"department": dept_id("DEPT1"),
                 "courseNumber": 100,
                  "courseName": "Course Test 1",
                 "description": "Major 1 description",
                  "units": 5
                 }
  db['Courses'].insert_one(course_test1)

  # section_test1 = {
  #     "course": course_id("Course Test 1"),
  #     "sectionNumber": 1,
  #     "semester": "Fall",
  #     "sectionYear": 2023,
  #     "building": "ANAC",
  #     "room": 1,
  #     "schedule": "MW",
  #     "instructor": "Test Prof 1",
  #     "startTime": "08:00"
  # }
  # db['Sections'].insert_one(section_test1)
  #
  # student_test1 = {"last_name" : "Student",
  #                  "first_name": "Test",
  #                  "email": "Testmail@test.com"
  # }
  # db['Students'].insert_one(student_test1)
  #
  # studentmajor_test1 = {"student" : student_id("Student","Test"),
  #                    "major": major_id(dept_id("DEPT1"), "Major1"),
  #                         "declarationDate": str(datetime.now().date())
  #   }
  # db['StudentMajor'].insert_one(studentmajor_test1)
  #
  # studentsection_test1 = {"student" : student_id("Student","Test"),
  #                  "section": section_id(course_id("Course Test 1"),1 )
  # }
  # db['StudentSection'].insert_one(studentsection_test1)
  #
  #
  #
  #
  # # error tests
  # test2 = {"name": "test1",
  #          "abbreviation": "TEST1",
  #          "chairName": "TEST1",
  #          "building": "ANAC",
  #          "office": 1,
  #          "description": "Test Description"}
  #
  #
  #
  #
  # db['Departments'].insert_one(test2)    # should trigger a unique constraint it, it does 6/28/2023 10:01pm