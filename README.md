# Automate Facebook Profile Picture Download

This project automates the download of Facebook profile pictures using two methods: through Facebook's Developer API and Selenium automation.

## How to Start the App Locally

Follow these steps to set up and run the application locally:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/risa-assgn.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd risa-assgn
    ```
3. **Create a virtual environment:**
    ```bash
    python3 -m venv env
    ```
4. **Activate the virtual environment:**
    - **On macOS/Linux:**
        ```bash
        source env/bin/activate
        ```
    - **On Windows:**
        ```bash
        .\env\Scripts\activate
        ```
5. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6. **Start the application using `uvicorn`:**
    ```bash
    uvicorn application:app --reload
    ```

### Available APIs

There are two main APIs for downloading the profile picture:

1. **`/api/download-picture`**:
   - This API uses the Facebook App for Developers. It requires the user to manually log in with their Facebook credentials and grant permission to access their profile picture.
   - Once authenticated, a pre-signed URL will be generated to download the profile picture from Facebook.

2. **`/api/automate/download-picture`**:
   - This API accepts a JSON payload containing the user's email and password. 
   - The Selenium client will attempt to automatically log in to Facebook, navigate to the user's profile, and take a screenshot of the profile picture. 
   - **Note:** This method is against Facebook's Terms of Service, and CAPTCHA may be triggered, requiring the user to manually solve it before the profile picture can be downloaded.

## Project Structure and Module Explanation

### Module 1: **awsClients**
This module contains the `S3Client`, which uses `boto3` to interact with Amazon S3. The `S3Client` provides the following functionalities:
- **Upload Image:** Uploads the profile picture to an S3 bucket.
- **Generate Pre-Signed URL:** Generates a pre-signed URL for the uploaded image, which is valid for 1 minute.

### Module 2: **facebookClients**
This module contains two clients:
1. **FacebookClient:**
   - This client utilizes the Facebook App for Developers, requiring the Facebook App ID and App Secret stored in environment variables.
   - It is responsible for obtaining an access token, retrieving the user's profile, and downloading the profile picture.
   - The downloaded image is then uploaded to S3 using `S3Client`, and a pre-signed URL is generated for it.
   
2. **FacebookSeleniumClient:**
   - This client uses Selenium to automate the login and navigation on Facebook.
   - It opens the login page, enters the credentials, navigates to the user's profile page, and takes a screenshot of the profile picture.
   - The profile picture is then uploaded to S3 and a pre-signed URL is generated for it.
   - **Note:** Selenium automation might trigger Facebook’s CAPTCHA system, requiring manual input from the user to complete the login process.

### Module 3: **Custom Logger**
This module contains a simple custom logger for logging messages at different levels (Info, Debug, Error). The custom logger helps track the flow of the application and makes it easier to troubleshoot issues during development and in production. It ensures that logs are:
- Structured and formatted according to the needs of the application.
- Stored in the appropriate places, such as console output or files.
- Separated into different log levels to distinguish between informational messages, debugging data, and error messages.

## Additional Notes

- **Facebook Terms of Service:** The use of Selenium to automate Facebook login and download profile pictures violates Facebook's Terms of Service. This method should only be used for educational purposes or with explicit user consent.
- **Captcha Handling:** The automated method might trigger CAPTCHA, which requires the user to manually solve it to proceed.

