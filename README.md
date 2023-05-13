# Alar test case

## Description
    1. There are three data sources (for the test task, these can be three
    simple tables with an id and some text field).

    Example:
    -- Create table
    CREATE TABLE data_1 (
        id INT PRIMARY KEY,
        name VARCHAR(255)
    );
    -- Insert data into table
    INSERT INTO data_1 (id, name)
    VALUES (1, 'Test 1'), (2, 'Test 2');

    The IDs are distributed as follows:
    - 1st source: IDs 1-10, 31-40;
    - 2nd source: IDs 11-20, 41-50;
    - 3rd source: IDs 21-30, 51-60;

    2. There is a single common access point to these data sources (a
    Flask/FastAPI application) that provides a correlated result. The access
    point is available via HTTP.

    Example:
    [
        {“id”:1,”name”:”Test 1”},
        {“id”:2,”name”:”Test 2”}
    ]

    3. This access point should make requests to all data sources
    "asynchronously" and wait for the results from all of them.
    4. Upon receiving the results from all sources, return the data sorted
    by ID (data from all sources).
    5. An error from any of the sources is ignored and interpreted as
    missing data.
    6. A timeout is also considered an error (2 seconds).
    7. Write tests to cover all added logic, preferably use mocks for db
    connection.
    8. It is essential to demonstrate the use of both ORM and raw SQL.
    9. Provide code comments, docstrings, documentation and typing
    annotations [bonus].

## Endpoints
 - base_url/get_all/ - to get async all raws from 3 tables
 - base_url/get_name/{id} - to get existing raw from table
 - base_url/get_by_range/ - to get range of raws from all 3 tables
    |__ json_body:
                |__ {
                    "start": "int",
                    "end": "int"
                }

## Technologies Used
 - Python
 - FastAPI
 - Docker
 - PostgreSQL
 - Pytest
 - SqlAlchemy

## Getting Started
1. Clone the repository to your PC
2. create .env file like in example:
```
DB_NAME=postgres
DB_HOST=db_alar
DB_PORT=5432
DB_USER=postgres
DB_PASS=mypassword
```
3. In the project directory, run the following command:
```
docker-compose up --build -d
```