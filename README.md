# 📦 Storage Management — Inventory Control System

This is a multi-service containerized inventory control system built with **FastAPI** (backend), **Flask** (frontend), and **PostgreSQL** (database). The services are orchestrated using **Docker Compose**.

---

## 🚀 How to Run the Project (Docker)

### 1. Prerequisites
Ensure you have the following installed on your machine:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### 2. Configure Environment Variables
Copy the example environment file to create your own configuration:
```bash
cp .env.example .env
```
Open the `.env` file and make sure the database settings match your needs (the defaults are preconfigured to work out of the box with Docker).

### 3. Start the Containers
Build and spin up all services in the background:
```bash
docker-compose up -d --build
```
This will start three containers:
* **`storage_db`**: PostgreSQL 16 database.
* **`storage_backend`**: FastAPI REST API listening on port `8000`.
* **`storage_frontend`**: Flask web interface listening on port `3000`.

### 4. Verify Services Status
To make sure everything is up and running correctly:
```bash
docker-compose ps
```

---

## 🖥 Accessing the Application

Once the containers are running, you can access the following interfaces:

* **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)
  * View stock levels, low-stock warnings, and latest movements.
  * Manage inventory details and perform stock entries/removals.
* **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
  * Explore and test the API endpoints interactively.
* **Backend API Docs (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Tests (Inside Docker)

You can run the backend unit and integration test suite inside the running backend container:
```bash
docker-compose exec backend pytest -v
```

---

## 🛑 Stopping the Application

To shut down all containers and networks:
```bash
docker-compose down
```
To stop the services and also remove the database persistent volume (warning: this will clear all data):
```bash
docker-compose down -v
```
