# Initialize FastAPI and FacebookClient
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
import requests
from dotenv import load_dotenv
from facebookClient.facebookClient import FacebookClient
from logger.logger import CustomLogger

load_dotenv()
app = FastAPI()

APP_ID = os.getenv("FACEBOOK_APP_ID")
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
REDIRECT_URI = "http://localhost:8000/api/callback"  # Update based on your setup
facebook_client = FacebookClient(app_id=APP_ID, app_secret=APP_SECRET, redirect_uri=REDIRECT_URI)
logger = CustomLogger()



@app.get("/api/download-profile-picture")
async def login():
    """
    Redirects the user to Facebook's login page.
    """
    logger.info("Root endpoint was accessed")
    login_url = facebook_client.get_login_url()
    return RedirectResponse(login_url)


@app.get("/api/callback")
async def callback(request: Request):
    """
    Handles the callback from Facebook and retrieves the user's profile information.
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided by Facebook")

    try:
        # Exchange code for an access token
        access_token = facebook_client.exchange_code_for_token(code)

        # Fetch user profile
        user_profile = facebook_client.fetch_user_profile(access_token)
        picture_url = user_profile["picture"]["data"]["url"]

        # Download profile picture
        output_file = f"{user_profile['id']}_profile_picture.jpg"
        facebook_client.download_profile_picture(picture_url, output_file)

        return JSONResponse(content={
            "message": "Profile retrieved successfully",
            "user_profile": user_profile,
            "profile_picture": f"Downloaded as {output_file}"
        })

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# Run FastAPI using: uvicorn main:app --reload
