# FastAPI Application

This is a FastAPI application that provides access to greenhouse gas emissions data.

## Purpose

This FastAPI application serves as a platform for accessing and querying greenhouse gas emissions data, making it easier for researchers and environmental enthusiasts to analyze and explore this critical information. Researchers can view summary data for emissions or drill into the detail by fetching more detailed data per emission element id.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python](https://www.python.org/) (version 3.11.3)
- [Docker](https://www.docker.com/) (version 24.0.2)

## Getting Started

Follow these steps to set up and run the FastAPI application:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ecoact.git
   cd ecoact
   ```

````

2. Run the setup script

```bash
./setup.sh
````

## Configuration

The application supports the following configuration options via environment variables:

DATABASE_URL: The URL of the PostgreSQL database. Default is postgresql://admin:welovetheenvironment@db:5432/ecoact_db.
FASTAPI_HOST: The host on which FastAPI listens. Default is 0.0.0.0.
FASTAPI_PORT: The port on which FastAPI runs. Default is 8000.

## Usage

This application provides various endpoints to access greenhouse gas emissions data. You can interact with the API using HTTP requests. Below are a couple of examples:

Retrieve summary data by specifying the ID.

**Endpoint**: `/summary-data/{id}`

**Method**: GET

**Example Request**:

```bash
curl http://localhost:8000/summary-data/12892
```

Retrieve detailed data specific to a summary id.

**Endpoint**: `/detailed-data/by-summary/{summary_id}`

**Method**: GET

**Example Request**:

```bash
curl http://localhost:8000/detailed-data/by-summary/12892
```

Navigate to http://localhost:8000/docs to see the full API documentation

## UI

A rudimentary UI set up with Dash can be accessed by navigating to: http://localhost:8050

### Next steps

- The dash folder represents the beginning of a simple frontend UI built using Dash however as this is an API, it could be designed using any suitable web application framework. The frontend would be made more beautiful, eventually incorporate filter options to search for specific data types and a form to submit further details. Beyond that you could add graphing and data visualisation options.
- Unit tests should be written for the APIs and any future APIs
- The raw data can be further cleaned, particularly with more context around its origin and purpose.
