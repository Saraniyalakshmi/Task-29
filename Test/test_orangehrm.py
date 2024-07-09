import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Pages.LoginPage import LoginPage  # Make sure this import is correct
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging to output to a file named 'test_login.log' with the specified format
logging.basicConfig(filename='test_login.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read data from an Excel file located at the specified path
df = pd.read_excel('C:/Users/MageSaran/PycharmProjects/Task29_LoginValidation_OrangeHRM/Testdata.xlsx')

@pytest.fixture(scope="class")
def setup(request):
    # Configure Chrome options
    options = Options()
    options.add_experimental_option("detach", True)
    # Initialize WebDriver for Chrome
    driver = webdriver.Chrome(options=options)
    # Navigate to the login page
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    request.cls.driver = driver
    yield
    # Quit the driver after tests are done
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestLogin:
    # Locators for the profile icon and logout button
    profile_icon_locator = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    logout_button_locator = (By.XPATH, "//a[text()='Logout']")

    def test_login(self):
        # Initialize the LoginPage with the driver
        login_page = LoginPage(self.driver)
        results = []

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            test_id = row['Test ID']
            username = row['Username']
            password = row['Password']
            name_of_tester = row['Name of Tester']
            date_of_test = datetime.now().strftime("%Y-%m-%d")
            time_of_test = datetime.now().strftime("%H:%M:%S")
            result = "Failed"  # Default assumption

            try:
                # Log the attempt to login
                logging.info(f"Attempting login for {username}")
                if login_page.login(username, password):
                    # If login is successful, set result to "Passed" and log out
                    result = "Passed"
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(self.logout_button_locator)).click()
                else:
                    # Log a failed login attempt
                    logging.error(f"Login failed for {username}")

            except Exception as e:
                # Log any exception that occurs
                logging.error(f"An error occurred for {username}: {e}")

            # Append the result for this test case to the results list
            results.append([test_id, username, password, date_of_test, time_of_test, name_of_tester, result])

        # Write results back to an Excel file
        results_df = pd.DataFrame(
            results,
            columns=['Test ID', 'Username', 'Password', 'Date', 'Time of Test', 'Name of Tester', 'Test Result']
        )
        results_df.to_excel(
            'C:/Users/MageSaran/PycharmProjects/Task29_LoginValidation_OrangeHRM/test_results.xlsx', index=False
        )
