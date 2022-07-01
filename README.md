# FastApiWorker

A Simple FastAPI webserver that proccesses an CSV file and returns it.

## Description

This project uses FastAPI for the webserver and pandas for the CSV operations

## Getting Started

### Dependencies

* Python >=3.5
* FastAPI
* uvicorn (ASGI Server)

### Installing

* pip install fastapi 
* pip install "uvicorn[standard]"

### Executing program

* How to run the server
```
uvicorn main:app --reload
```
* How to run tests
```
pytest
```

## Improvements

### Decoupling

Running time consuming tasks like csv proccessing on the endpoint is a very bad idea and is just for proof-of-concept, the next step is to implement a message queue and have all the csv processing be dealt with on a seperate application, which would improve the webserver performance and the problems of requests timing out.

### Dockerized environment

Creating docker containers for the whole solution (webserver, messaging queue, worker)

## Known Bugs

* git might change the test files from LF back to CRLF if you are on windows (to be confirmed)

* missing some input validation for columns that have currency
