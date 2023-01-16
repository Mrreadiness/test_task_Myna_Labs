# Test task for Myna Labs

## Backend Structure

- src - Source code of application
    - api - FastApi web server with routes
    - data - Data layer module. Including Unit of Work and repositories
    - domain - Business logic and entities of the application
    - config - Configs of the application
    - container - Dependency Injector container that connects all parts 
    of the application together
- tests - Unit tests