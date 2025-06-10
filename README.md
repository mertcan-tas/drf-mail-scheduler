# DRF Mail Scheduler

This project is a Django REST Framework (DRF) application for scheduling and sending emails. It leverages **Django**, **Django REST Framework**, **Redis** (for task queuing with `rq` and `rq-scheduler`), and **Mailpit** for email testing. All API requests are logged to **MongoDB** using a custom handler.

## Features

* **Email Scheduling**: Schedule emails to be sent at a specific future time.
* **API for Scheduling**: A straightforward API endpoint to submit email scheduling requests.
* **Asynchronous Task Processing**: Uses `rq` and `rq-scheduler` for efficient background email sending.
* **Request Logging**: Logs all incoming API requests to MongoDB for auditing and debugging.
* **Email Testing**: Integrates with Mailpit for easy local email development and testing.


## Preview

![](https://raw.githubusercontent.com/mertcan-tas/drf-mail-scheduler/refs/heads/master/client/public/preview.gif)

## Technologies Used

* **Django**: Web framework.
* **Django REST Framework (DRF)**: For building the API.
* **Redis**: In-memory data store, used by `rq` and `rq-scheduler`.
* **RQ (Redis Queue)**: Python library for queueing jobs and processing them in the background with Redis.
* **RQ Scheduler**: An RQ extension that allows you to schedule jobs to be executed at a later time.
* **MongoDB**: NoSQL database for logging API requests.
* **Mailpit**: A small, fast, and easy-to-use API-based SMTP server for testing emails.

## Setup and Installation

### Prerequisites

* Docker

### 1. Clone the repository

```bash
git clone https://github.com/mertcan-tas/drf-mail-scheduler.git
cd drf-mail-scheduler
```

### 2. Set up environment variables

Copy the `.env.copy` file to `.env`:

```bash
cp .env-copy .env
```

You can then edit the newly created `.env` file if you need to customize any variables. The `.env-copy` typically contains:

```
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres 
POSTGRES_PORT=5432
 
MONGO_ROOT_USERNAME=mongo
MONGO_ROOT_PASSWORD=password
MONGO_DB_NAME=django_logs
MONGO_HOST=mongodb    
MONGO_PORT=27017

REDIS_HOST=redis       
REDIS_PORT=6379
REDIS_PASSWORD=password
REDIS_DB=0
```

### 3. Run with Docker Compose

Simply run the following command to build and start all services (Django, Redis, MongoDB, Mailpit, RQ worker, RQ scheduler):

```bash
docker compose up -d --build
```

This command will:
* Build the Docker images for your application.
* Start containers for Django, Redis, MongoDB, Mailpit, the RQ worker, and the RQ scheduler.
* Apply Django database migrations.

## API Endpoint

### Schedule Mail

Schedules an email to be sent at a specified time.

* **URL**: `http://localhost:8000/api/schedule-mail/`
* **Method**: `POST`
* **Content-Type**: `application/json`

#### Request Body Example:

```json
{
  "recipient_email": "test@example.com",
  "subject": "Scheduled Test Email",
  "message": "Hello, this is a test email scheduled via DRF Mail Scheduler!",
  "scheduled_time": "2024-12-25T14:30:00Z"
}
```

#### Response Example (Success):

```json
{
  "message": "Mail was scheduled successfully",
  "recipient_email": "test@example.com",
  "scheduled_time": "2024-12-25T14:30:00Z",
  "job_id": "9aa42ae6-6788-4842-a1cc-4ddfee1a76de"
}
```

## Logging

All API requests to `/api/schedule-mail/` are logged to a MongoDB collection.

## Mailpit

Mailpit is accessible at `http://localhost:8025`. You can view all emails sent by the application here during development.

## Project Structure

```
.
├── app
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py # RQ tasks
│   ├── urls.py
│   └── views.py # RQ tasks for sending emails
├── config
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── apps.py
│   ├── logging.py  # Custom MongoDB logging handler
│   └── middleware.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── nginx
│   └── nginx.conf
└── requirements.txt
```

## Contributing

Feel free to fork this repository and contribute!

## License

DRF Mail Scheduler is distributed under the MIT License

See [LICENSE](/LICENSE)
