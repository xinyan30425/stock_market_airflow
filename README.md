# Stock Market Data Pipeline with Apache Airflow

This project implements a stock market data pipeline using Apache Airflow to automate data extraction, processing, and storage. The pipeline fetches stock prices from a remote API, stores them in MinIO (an S3-compatible object storage), processes the data using Docker containers, and loads the final output to a PostgreSQL database.

## Project Structure

- **`dags/stock_market.py`**: Defines the DAG (Directed Acyclic Graph) for orchestrating tasks such as fetching stock prices, storing them, formatting, and loading to the data warehouse.
- **`include/stock_market/tasks.py`**: Contains Python functions (tasks) for interacting with external services, such as APIs, MinIO, and databases.

## Workflow Overview

1. **Check API Availability**: Uses a sensor to check if the stock market API is available.
2. **Fetch Stock Prices**: Retrieves stock price data for a specified symbol from the stock market API.
3. **Store Prices in MinIO**: Saves the retrieved data as a JSON file in MinIO.
4. **Format Prices**: Processes the stored data using a Docker container.
5. **Get Formatted CSV**: Fetches the processed CSV file from MinIO.
6. **Load Data to Data Warehouse**: Loads the final CSV data into a PostgreSQL database.

## UML Diagram

Below is a UML activity diagram representing the stock market data pipeline workflow:

```mermaid
graph TD;
    A[Start] --> B{Check API Availability}
    B -->|API Available| C[Fetch Stock Prices]
    C --> D[Store Prices in MinIO]
    D --> E[Format Prices using Docker]
    E --> F[Get Formatted CSV from MinIO]
    F --> G[Load Data to PostgreSQL]
    G --> H[End]
    B -->|API Not Available| I[Wait and Retry]
    I --> B


## Requirements

- **Apache Airflow**: Version 2.10.0 or later
- **Docker**: Docker Engine and Docker Compose
- **MinIO**: Server for object storage
- **PostgreSQL**: Database for storing processed data
- **Python Packages**:
  - `requests`
  - `minio`
  - `astro-sdk-python`

Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
    - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'airflow' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5435/postgres'.

Deploy Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/


