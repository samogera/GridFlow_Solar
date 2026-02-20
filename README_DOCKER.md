# Docker Setup for Ecobright

This app can be run using Docker for portability.

## Prerequisites
- Docker
- Docker Compose

## Build and Run

1.  **Build the Image**
    ```bash
    docker-compose build
    ```

2.  **Start the Stack**
    ```bash
    docker-compose up -d
    ```

3.  **Initialize Site (First Time Only)**
    You might need to create a new site inside the container if one doesn't exist.
    ```bash
    docker-compose exec backend bench new-site ecobright.docker --admin-password 123 --db-root-password 123 --install-app ecobright
    ```

4.  **Access the App**
    Open [http://localhost:8000](http://localhost:8000)

## Development
To run commands inside the container:
```bash
docker-compose exec backend bench --site ecobright.docker [command]
```
