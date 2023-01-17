# Test task for Myna Labs

## Run project

1. Run project by docker compose
  ```shell
  docker compose up --build -d 
  ```
2. Create database
  ```shell
  docker exec test_task_backend python3 src/scripts/create_db.py
  ```
3. Go to [Swagger](http://0.0.0.0:8000/docs):


## Backend Structure

- src - Source code of application
    - api - FastApi web server with routes
    - data - Data layer module. Including Unit of Work and repositories
    - domain - Business logic and entities of the application
    - config - Configs of the application
    - container - Dependency Injector container that connects all parts 
    of the application together
- tests - Unit tests