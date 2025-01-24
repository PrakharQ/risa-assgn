import os
from dotenv import load_dotenv

load_dotenv()


config = {
    "FACEBOOK_APP_ID": os.getenv("FACEBOOK_APP_ID"),
    "FACEBOOK_APP_SECRET": os.getenv("FACEBOOK_APP_SECRET"),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "REDIRECT_URI": os.getenv("REDIRECT_URI"),
    "UPLOAD_BUCKET": os.getenv("UPLOAD_BUCKET")
}
