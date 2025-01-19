from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import os
import requests
from dotenv import load_dotenv


class FacebookClient:
    """
    A client to handle Facebook Graph API operations.
    """
    def __init__(self, app_id: str, app_secret: str, redirect_uri: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.base_auth_url = "https://www.facebook.com/v12.0/dialog/oauth"
        self.token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
        self.graph_url = "https://graph.facebook.com/v12.0"

    def get_login_url(self, scope: str = "public_profile") -> str:
        return (
            f"{self.base_auth_url}?client_id={self.app_id}&redirect_uri={self.redirect_uri}&scope={scope}"
        )

    def exchange_code_for_token(self, code: str) -> str:
        params = {
            "client_id": self.app_id,
            "redirect_uri": self.redirect_uri,
            "client_secret": self.app_secret,
            "code": code,
        }
        response = requests.get(self.token_url, params=params)
        response.raise_for_status()
        return response.json().get("access_token")

    def fetch_user_profile(self, access_token: str) -> dict:
        fields = "id,name,picture.type(large)"
        response = requests.get(
            f"{self.graph_url}/me", params={"fields": fields, "access_token": access_token}
        )
        response.raise_for_status()
        return response.json()

    def download_profile_picture(self, picture_url: str, output_file: str):
        response = requests.get(picture_url, stream=True)
        response.raise_for_status()

        with open(output_file, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Profile picture downloaded successfully: {output_file}")


