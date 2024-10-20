
## Recipe Social Media Platform Backend

This backend platform allows users to share and rate recipes, built with Django Rest Framework (DRF). Customers can view and rate recipes, while Sellers can add new recipes with images, names, and descriptions.

## Features

- **Authentication and Authorization**: Token-based authentication for both Customers and Sellers.
- **Rate Limiting and Throttling**: Fair usage enforced through request throttling.
- **Recipe API**: RESTful APIs for managing and interacting with recipes and ratings.
- **Asynchronous Tasks**: Image resizing and daily email notifications implemented with Celery.
- **Scheduled Services**: Weekly user data export to Amazon S3 in CSV format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Asynchronous Tasks](#asynchronous-tasks)
- [Scheduled Services](#scheduled-services)
- [License](#license)

## Installation

### Requirements

- Python 3.10+
- Django 4.x
- Django Rest Framework
- PostgreSQL
- Celery
- Redis (for Celery broker)
- Amazon S3 (for data storage)
- Pillow (for image processing)
- Boto3 (for S3 interactions)

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/Vishalanshuman/social_media_backend.git
   cd recipe-platform-backend
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Setup PostgreSQL database:

   ```bash
   psql -U postgres -c "CREATE DATABASE socialDB;"
   ```

5. Configure your `.env` file with the following:

   ```bash
   DATABASE_NAME=socialDB
   DATABASE_USER=postgres
   DATABASE_PASSWORD=root
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   SECRET_KEY=your_secret_key
   CELERY_BROKER_URL=redis://localhost:6379/0
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
   DEFAULT_FROM_EMAIL=your_email@example.com
   ```

6. Apply migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

### Starting Celery Worker

To process asynchronous tasks (image resizing, email sending, data uploading), start a Celery worker:

```bash
celery -A config worker --loglevel=info --pool=solo
```

### Starting Celery Beat

To schedule tasks, run Celery Beat:

```bash
celery -A config beat --loglevel=info
```

## API Endpoints

### Authentication

- **Signup**:  
  `POST /auth/signup/`  
  Registers a new user.

- **Login**:  
  `POST /auth/login/`  
  Logs in and returns tokens.

- **Token Refresh**:  
  `POST /auth/token/refresh/`  
  Refreshes the JWT access token.

### Recipe APIs

- **List Recipes**:  
  `GET /recipes/`  
  Fetches the list of recipes.

- **Recipe Details**:  
  `GET /recipes/{id}/`  
  Fetches details for a specific recipe.

- **Create Recipe** (Sellers only):  
  `POST /recipes/`  
  Adds a new recipe.

### Rating APIs

- **Rate Recipe**:  
  `POST /recipes/{id}/rate/`  
  Allows a user to rate a recipe.

- **Get Ratings**:  
  `GET /recipes/{id}/ratings/`  
  Fetches all ratings for a recipe.

### Throttling

- **Anonymous Users**: 10 requests per minute.
- **Authenticated Users**: 100 requests per minute.

## Asynchronous Tasks

### Image Resizing

Sellers can upload images when adding recipes. The image is resized asynchronously using Celery to ensure the uploaded images are optimized for performance. The task is defined as:

```python
@shared_task
def resize_recipe_image(image_path):
    ...
```

### Daily Emails

A daily email task is scheduled to send recipe updates to all users (except on weekends). The task is defined as:

```python
@shared_task
def send_daily_emails():
    ...
```

## Scheduled Services

### Weekly User Data Export to S3

Every week, user data is retrieved from the database and uploaded to Amazon S3 in CSV format. The task is defined as:

```python
@shared_task
def upload_user_data_to_s3():
    ...
```

