
# Transaction Dashboard API

## Overview

The **Transaction Dashboard API** provides endpoints to query and summarize transaction data stored in MongoDB. This repository includes:

- **Aggregation Pipeline**: Efficiently processes transaction data using MongoDB's aggregation framework.
- **Logging Middleware**: Captures and logs all API requests and responses to the `logs/` directory for comprehensive monitoring and debugging.
- **Notification System**: Built with the **Strategy Design Pattern**, it supports multiple notification mediums (such as email and SMS), implements retry policies for reliability, and utilizes **Celery** for asynchronous task processing to ensure timely delivery of alerts and reports without blocking the main application flow.
- **Django Command**: A dedicated command to summarize transactions, enhancing data processing efficiency by aggregating transaction data and storing summaries for quick access.
- **Postman Collection**: Included in the repository to facilitate easy testing of the APIs.

## Features

- **Transaction History API**: Retrieve transactions based on filters such as type, mode, and optional merchant ID.
- **Transaction Summary API**: Access pre-processed transaction summaries to enhance performance.
- **Logging Middleware**: Logs all incoming requests and outgoing responses to the `logs/` directory.
- **Notification System**:
  - **Strategy Design Pattern**: Manages different notification mediums (e.g., email, SMS) with a flexible and maintainable code structure.
  - **Retry Policies**: Ensures reliable delivery of notifications by handling retries in case of failures.
  - **Celery Integration**: Handles asynchronous processing of notification tasks to maintain application responsiveness.
- **Dockerized**: The entire application is containerized using **Docker** and **Docker Compose** for easy deployment and scalability.

## Setup Instructions

### Prerequisites

- **Docker & Docker Compose**: Ensure Docker and Docker Compose are installed.
- **Git**: To clone the repository.
- **Postman**: For API testing.

### Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/enouraee/transaction_dashboard.git
    cd transaction_dashboard
    ```

2. **Start Services:**
    ```bash
    docker compose up --build -d
    ```
    This command builds and starts all services defined in the `docker-compose.yml` file in detached mode.

3. **Restore MongoDB Data:**
    - **Identify MongoDB Container ID:**
        ```bash
        docker ps
        ```
    - **Execute Restore Command:**
        ```bash
        docker exec -i <mongodb_container_id> mongorestore --gzip --archive=/docker-entrypoint-initdb.d/zibal_db_backup.archive
        ```

## Running the Project

- **Access the APIs:**
    - **Base URL:** `http://localhost:8000`
    - **Transaction History API Example:**
        ```
        GET http://localhost:8000/api/transactions/transaction-history/?type=amount&mode=daily&merchantId=63a69a2d18f9347bdafd5e10
        ```
    - **Transaction Summary API Example:**
        ```
        GET http://localhost:8000/api/transactions/transaction-summary/?type=amount&mode=daily&merchantId=63a69a2d18f9347bdafd5e10
        ```



## Running Django Commands

- **Generate Transaction Summaries:**
    ```bash
    docker-compose exec web python manage.py generate_transaction_summaries
    ```
    This command processes transactions using the aggregation pipeline and stores the results in the `transaction_summary` collection.
