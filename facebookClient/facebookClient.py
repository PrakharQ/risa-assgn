import requests
import uuid


class FacebookClient:
    """
    A client to handle Facebook Graph API operations.

    Attributes:
        app_id (str): Facebook app ID.
        app_secret (str): Facebook app secret.
        redirect_uri (str): Redirect URI for OAuth flow.
        logger: Logger instance for logging operations.
    """

    def __init__(self, app_id: str, app_secret: str, redirect_uri: str, logger):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.logger = logger

    def get_login_url(self) -> str:
        """
        Generates the Facebook login URL.

        Returns:
            str: The URL for Facebook login.
        """
        try:
            url = (
                f"https://www.facebook.com/v12.0/dialog/oauth"
                f"?client_id={self.app_id}"
                f"&redirect_uri={self.redirect_uri}"
                f"&scope=public_profile"
            )
            self.logger.info("Generated Facebook login URL.")
            return url
        except Exception as e:
            self.logger.error(f"Failed to generate login URL: {e}")
            raise

    def exchange_code_for_token(self, code: str) -> str:
        """
        Exchanges the authorization code for an access token.

        Args:
            code (str): Authorization code obtained from Facebook.

        Returns:
            str: Access token.

        Raises:
            ValueError: If the response doesn't contain an access token.
        """
        try:
            url = "https://graph.facebook.com/v12.0/oauth/access_token"
            params = {
                "client_id": self.app_id,
                "redirect_uri": self.redirect_uri,
                "client_secret": self.app_secret,
                "code": code,
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            access_token = data.get("access_token")
            if not access_token:
                raise ValueError("Access token not found in the response.")
            self.logger.info("Successfully exchanged code for access token.")
            return access_token
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error exchanging code for token: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Invalid response during token exchange: {e}")
            raise

    def get_user_profile_picture(self, access_token: str) -> str:
        """
        Fetches the URL of the user's profile picture.

        Args:
            access_token (str): Facebook Graph API access token.

        Returns:
            str: URL of the user's profile picture.

        Raises:
            ValueError: If the response format is unexpected.
        """
        try:
            url = "https://graph.facebook.com/v12.0/me/picture"
            params = {"access_token": access_token, "redirect": "false", "type": "large"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            picture_url = data.get("data", {}).get("url")
            if not picture_url:
                raise ValueError("Profile picture URL not found in the response.")
            self.logger.info("Successfully fetched profile picture URL.")
            return picture_url
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching profile picture: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Invalid response during profile picture fetch: {e}")
            raise

    def download_profile_picture(self, picture_url: str, save_path: str = None) -> str:
        """
        Downloads the profile picture from the provided URL.

        Args:
            picture_url (str): URL of the profile picture.
            save_path (str): Path to save the downloaded file. If None, generates a random file name.

        Returns:
            str: The file path where the profile picture was saved.
        """
        try:
            if save_path is None:
                save_path = f"profile_pictures/{uuid.uuid4()}.jpg"

            response = requests.get(picture_url, timeout=10)
            response.raise_for_status()

            with open(save_path, "wb") as file:
                file.write(response.content)

            self.logger.info(f"Profile picture successfully saved to {save_path}")
            return save_path
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading profile picture: {e}")
            raise
        except IOError as e:
            self.logger.error(f"File I/O error when saving profile picture: {e}")
            raise
