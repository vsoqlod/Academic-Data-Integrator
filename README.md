# Academic Data Integrator

- Developed a Python console application that connects with MongoDB, designed to enforce a set of predefined business rules on academic data, ensuring data integrity and consistency.
- Initially started with a demonstration using SQLalchemy, PostgreSQL, and DataGrip before transitioning to MongoDB for its document-based data model, which offers flexibility in managing academic datasets.

## Key Features:
- **Data Management**: Allows users to add, delete, and list data related to key entities in the academic sphere, such as departments, courses, and schedules.
- **Error Handling**: Incorporates error-trapping mechanisms to prevent and handle incorrect data entries, ensuring the reliability of the database operations.
- **Business Rules Enforcement**: Utilizes MongoDB's unique indexes and schema constraints, along with Python's logic, to apply business rules like preventing schedule overlaps in the same location and ensuring each department has a chairperson.
