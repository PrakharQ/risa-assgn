import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
from logger.logger import CustomLogger



class FacebookSeleniumClient:
    def __init__(self, headless=True, logger: CustomLogger=None):
        # Set up Selenium WebDriver
        self.driver = self._get_webdriver(headless)
        self.logger = logger or CustomLogger()

    def _get_webdriver(self, headless):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self, email, password):
        """Logs into Facebook with the given email and password."""
        try:
            # Open Facebook login page
            self.driver.get("https://www.facebook.com/login.php")
            time.sleep(2)

            # Enter email and password
            email_field = self.driver.find_element(By.ID, "email")
            password_field = self.driver.find_element(By.ID, "pass")
            email_field.send_keys(email)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Check for CAPTCHA
            if "captcha" in self.driver.page_source.lower():
                self.logger.info("CAPTCHA detected. Please solve it manually in the browser.")
                time.sleep(20)

            self.logger.info("Login successful.")
            return True
        except Exception as e:
            print(f"An error occurred during login: {e}")
            return False

    def download_profile_picture(self, output_file="profile_picture.jpg"):
        """Downloads the logged-in user's profile picture."""
        try:
            # Navigate to the user's profile page
            self.driver.get("https://www.facebook.com/me")
            time.sleep(5)

            # Locate profile picture element
            self.driver.execute_script(f"document.body.style.zoom='{2}'")
            time.sleep(2)  # Allow the zoom effect to apply

            # Take a screenshot
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            left = 30
            top = 500
            right = 800
            bottom = 1250

            # Crop the profile picture
            cropped_image = image.crop((left, top, right, bottom))
            buffer = io.BytesIO()
            cropped_image.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer
        except Exception as e:
            self.logger.info(f"An error occurred while downloading the profile picture: {e}")
            return None

    def close(self):
        """Closes the WebDriver session."""
        self.driver.quit()