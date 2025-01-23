import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from awsClients.s3Client import S3Client
from facebookClient import FacebookClient
from logger.logger import CustomLogger
load_dotenv()

FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
UPLOAD_BUCKET = os.getenv("UPLOAD_BUCKET")


if not FACEBOOK_APP_ID or not FACEBOOK_APP_SECRET:
    raise ValueError("Facebook App ID and Secret must be set in the environment.")

app = FastAPI()
logger = CustomLogger()
s3_client = S3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, region='ap-south-1', logger=logger)
facebook_client = FacebookClient(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, REDIRECT_URI, logger)
    


class UserInput(BaseModel):
    email: str
    password: str   

@app.get("/api/download-picture")
async def redirect_to_facebook():
    """
    Redirects the user to the Facebook login page.
    """
    fb_login_url = facebook_client.get_login_url()
    logger.info("Redirecting user to Facebook login.")
    return RedirectResponse(url=fb_login_url)



@app.get("/api/callback")
async def facebook_callback(request: Request):
    """
    Handles the Facebook login callback and downloads the profile picture.
    """
    code = request.query_params.get("code")
    if not code:
        logger.error("No code parameter found in callback URL.")
        raise HTTPException(status_code=400, detail="Missing 'code' parameter")

    try:
        # Exchange the code for an access token
        access_token = facebook_client.exchange_code_for_token(code)
        logger.info(f"Access token retrieved")

        # Fetch the profile picture URL
        profile_picture_url = facebook_client.get_user_profile_picture(access_token)
        logger.info(f"Profile picture URL: {profile_picture_url}")
        save_path = uuid.uuid4().hex + ".jpg"
        # Download and save the profile picture
        response = facebook_client.download_profile_picture(profile_picture_url, save_path=save_path)

        s3_client.upload_file(response, save_path, bucket_name=UPLOAD_BUCKET)
        pre_signed_url = s3_client.get_signed_url(bucket_name=UPLOAD_BUCKET,key=save_path, expiration=60)
        logger.info("Profile picture downloaded successfully.")
        return {"message": "Profile picture downloaded successfully!", "picture_url": pre_signed_url}

    except Exception as e:
        logger.error(f"Error during Facebook callback: {e}")
        raise HTTPException(status_code=500, detail="Error processing Facebook login")
