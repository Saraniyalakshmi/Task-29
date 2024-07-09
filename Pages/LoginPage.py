# Import necessary Selenium components
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        # Initialize the driver and define locators for the login page elements
        self.driver = driver
        self.username_input = (By.NAME, 'username')
        self.password_input = (By.NAME, 'password')
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.logout_button = (By.XPATH, "//a[text()='Logout']")
        self.profile_icon = (By.XPATH, "//p[@class='oxd-userdropdown-name']")

    def enter_username(self, username):
        # Wait for the username input field to be present, clear it if necessary, and enter the provided username
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_input)).clear()
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        # Wait for the password input field to be present, clear it if necessary, and enter the provided password
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_input)).clear()
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login_button(self):
        # Wait for the login button to be clickable and click it
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.login_button)).click()

    def login(self, username, password):
        # Perform the login steps: enter username, enter password, and click the login button
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        # Verify if login is successful by checking for the presence of the profile icon and the logout button
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.profile_icon)).click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.logout_button)).click()
            print(f"Login successful for {username}")
            return True
        except Exception as e:
            # If any exception occurs (e.g., elements not found), consider the login as failed
            print(f"Login failed for {username}")
            return False
