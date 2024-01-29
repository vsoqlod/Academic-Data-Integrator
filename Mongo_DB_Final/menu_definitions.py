from menu import Menu
from Option import Option

"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(db)"),
    Option("List", "list_objects(db)"),
    Option("Delete", "delete(db)"),
    #    Option("Boilerplate Data", "boilerplate(db)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department(db)"),
    Option("Course", "add_course(db)"),
    Option("Section", "add_section(db)"),
    Option("Major", "add_major(db)"),
    Option("Student", "add_student(db)"),
    Option("Student to Major", "add_student_major(db)"),
    Option("Major to Student", "add_major_student(db)"),
    Option("Enrollment", "add_enrollment(db)"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department(db)"),
    Option("Course", "delete_course(db)"),
    Option("Sections", "delete_section(db)"),
    Option("Major", "delete_major(db)"),
    Option("Student", "delete_student(db)"),
    Option("Student to Major", "delete_student_major(db)"),
    Option("Major to Student", "delete_major_student(db)"),
    Option("Enrollment", "delete_enrollment(db)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Department", "list_department(db)"),
    Option("Course", "list_course(db)"),
    Option("Sections", "list_section(db)"),
    Option("Major", "list_major(db)"),
    Option("Student", "list_student(db)"),
    Option("Student to Major", "list_student_major(db)"),
    Option("Major to Student", "list_major_student(db)"),
    Option("Enrollment", "list_enrollment(db)"),
    Option("Exit", "pass")
])

# {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
# 1. This one is new. Essentially, we are making sure that no student can be
# enrolled in more than one section of the same course during the same
# semester.
# 2. You may or may not "migrate" departmentAbbreviation and
# courseNumber into

semester_menu = Menu('semester', 'Please indicate the section semester:', [
    Option("Fall", "Fall"),
    Option("Spring", "Spring"),
    Option("Winter", "Winter"),
    Option("Summer I", "Summer I"),
    Option("Summer II", "Summer II"),
    Option("Summer III", "Summer III")
])

schedule_menu = Menu('schedule', 'Please input the section schedule:', [
    Option("Monday/Wednesday", "MW"),
    Option("Monday/Wednesday/Friday", "MWF"),
    Option("Tuesday/Thursday", "TuTh"),
    Option("Friday", "F"),
    Option("Saturday", "S"),
])

enrollment_menu = Menu('enrollment', 'Enter enrollment (passfail or lettergrade):', [
    Option("passfail", "passfail"),
    Option("lettergrade", "lettergrade")
])


grade_menu = Menu('grade', 'Enter grade (minimum satisfactory grade input, A/B/C):', [
    Option("A", "A"),
    Option("B", "B"),
    Option("C", "C")
])