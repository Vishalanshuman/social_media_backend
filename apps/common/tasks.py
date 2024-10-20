from celery import shared_task
from PIL import Image
import os
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth import get_user_model
import boto3
import pandas as pd
from io import StringIO

User = get_user_model()

@shared_task
def resize_recipe_image(image_path):
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
    try:
        img = Image.open(full_image_path)
        img = img.convert('RGB')  
        img.thumbnail((800, 800)) 
        
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)  
        output.seek(0)
        
        with open(full_image_path, 'wb') as f:
            f.write(output.read())
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False



@shared_task
def send_daily_emails():

    today = datetime.now().strftime('%Y-%m-%d')
    subject = f"Your daily recipe update for {today}"
    message = "Here are today's top-rated recipes!"
    users = User.objects.all()

    recipients = [user.email for user in users]  # Fetch from your user model

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )



@shared_task
def upload_user_data_to_s3():
    users = User.objects.all().values('id', 'username', 'email', 'date_joined')  
    
    df = pd.DataFrame(list(users))
    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    file_name = 'user_data/user_data_weekly.csv'
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )
    
    print(f"Successfully uploaded {file_name} to S3")

