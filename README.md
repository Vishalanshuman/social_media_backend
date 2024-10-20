Recipe Social Media Platform Backend
This is the backend for a Social Media Platform focused on sharing and rating recipes. It is built using Django Rest Framework (DRF) and provides token-based authentication for Customers and Sellers. Customers can view and rate recipes, while Sellers can add recipes with images, names, and descriptions.

Features
Authentication and Authorization: Token-based authentication for both Customers and Sellers using Django Rest Framework Simple JWT.
Rate Limiting and Throttling: Fair usage enforcement for API requests.
API for Recipes: Allows access to recipes and ratings through RESTful APIs.
Asynchronous Tasks: Celery tasks to optimize recipe images and send daily emails.
Scheduled Services: Weekly data updates to Amazon S3 in CSV format.
Table of Contents
Installation
Usage
API Endpoints
Authentication
Asynchronous Tasks
Scheduled Services
License
Installation
Requirements
Python 3.10+
Django 4.x
Django Rest Framework
PostgreSQL
Celery
Redis (for Celery broker)
Amazon S3 (for data storage)
Pillow (for image processing)
Boto3 (for S3 interactions)
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/social_media_backend.git
cd recipe-platform-backend
Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Setup PostgreSQL database:

bash
Copy code
# Create the database (if not done already)
psql -U postgres -c "CREATE DATABASE socialDB;"
Configure your .env file with the following:

bash
Copy code
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
Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Start the development server:

bash
Copy code
python manage.py runserver
Usage
Starting Celery Worker
To process asynchronous tasks (image resizing, email sending, data uploading), start a Celery worker:

bash
Copy code
celery -A recipe_platform worker --loglevel=info
Starting Celery Beat
To schedule tasks, run Celery Beat:

bash
Copy code
celery -A recipe_platform beat --loglevel=info
API Endpoints
Authentication
User Signup:
POST /auth/signup/
Registers a new user (Customer or Seller).

User Login:
POST /auth/login/
Logs in and returns access and refresh tokens.

Token Refresh:
POST /auth/token/refresh/
Refreshes an access token using a refresh token.

Recipe APIs
List Recipes:
GET /recipes/
Fetches the list of available recipes.

Recipe Details:
GET /recipes/{id}/
Fetches details for a specific recipe.

Create Recipe: (Sellers only)
POST /recipes/
Adds a new recipe with an image, name, and description.

Rating APIs
Rate Recipe:
POST /recipes/{id}/rate/
Allows a customer to rate a recipe (1 to 5 stars).

Get Ratings:
GET /recipes/{id}/ratings/
Fetches the ratings for a specific recipe.

Throttling
The following throttling rules apply:

Anonymous Users: 10 requests per minute.
Authenticated Users: 100 requests per minute.
Authentication
This project uses JWT (JSON Web Tokens) for authentication.

Access Token: Used to authenticate the user for each request.
Refresh Token: Used to obtain a new access token when the old one expires.
To authenticate requests, include the following header:

http
Copy code
Authorization: Bearer <access_token>
Asynchronous Tasks
Image Resizing (Celery Task)
When a seller uploads a recipe image, a Celery task is triggered to resize the image to a maximum resolution of 800x800 pixels. This reduces the image size to optimize storage. The task is handled asynchronously to avoid blocking the main request.

python
Copy code
@shared_task
def resize_recipe_image(image_path):
    # Logic to resize the image and save it
Daily Email Notifications (Celery Task)
Daily emails are sent to users every day at 6 AM (except Saturdays and Sundays). These emails contain updates and top-rated recipes.

python
Copy code
@shared_task
def send_daily_emails():
    # Logic to send daily email notifications
To schedule this task, Celery Beat must be running to ensure the task executes at the specified time.

Scheduled Services
Weekly Data Upload to Amazon S3 (Celery Task)
Every week, a scheduled task retrieves user data from the database and uploads it to Amazon S3 in CSV format. This service ensures that all user data is securely backed up.

python
Copy code
@shared_task
def upload_user_data_to_s3():
    # Logic to upload user data to S3
The task generates a CSV file containing user information like username, email, and registration date. The file is then uploaded to a specified S3 bucket.

License
This project is licensed under the MIT License.

Notes:
You will need to configure Amazon S3 for the data backup.

You will need to set up Redis for Celery to function properly. You can use Docker for Redis with the following command:

bash
Copy code
docker run -d -p 6379:6379 redis
If you encounter any issues during setup or execution, feel free to open an issue on GitHub or contact the project maintainers.