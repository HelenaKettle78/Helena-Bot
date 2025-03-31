import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Get the directory where the executable is running
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the credentials file
credentials_file = os.path.join(base_dir, "credentials_web.xlsx")

chromedriver_autoinstaller.install()

# Selenium WebDriver setup
chrome_options = Options()

#chromedriver_path = chromedriver_autoinstaller.install()
#chrome_options.binary_location = chromedriver_path

chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

n = 0

driver.get("https://voting.mediasetinfinity.mediaset.it/sms.grandefratello.eliminazione.web/index.html")
time.sleep(3)

def vote(email, password):
    """Attempts to vote using the given email and password."""
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/button'))).click()
        time.sleep(2)
    except:
        print(f"Accedi button not found for {email}, skipping login.")
        return False

    try:
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[1]/input')))
        email_input.clear()
        email_input.send_keys(email)
    except:
        print(f"Unable to find email input field for {email}, skipping...")
        return False

    try:
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[2]/input')))
        password_input.clear()
        password_input.send_keys(password)
    except:
        print(f"Unable to find password input field for {email}, skipping...")
        return False

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[6]/input'))).click()
        time.sleep(2)
    except:
        print(f"Invia button not found for {email}, skipping...")
        return False

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
        print(f"Successfully logged in with {email}")
    except:
        print(f"Login failed for {email}, skipping...")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/a'))).click()
        return False

    try:
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/button'))).click()
        time.sleep(1)
    except:
        print("Voting elements not found, skipping...")
        return False

    try:
        logout_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
        logout_button.click()
        time.sleep(2)
    except:
        print("Logout button not found, continuing anyway.")

    print(f"Voting completed for {email}.")
    return True  # Vote was successful


# Start voting loop
while True:
    try:
        df = pd.read_excel(credentials_file)  # Reload file before each loop
        if df.empty:
            print("No more accounts left to vote with.")
            break

        success = False  # Flag to track if voting was successful

        for index, row in df.iterrows():  # Iterate through each row
            email, password = row["Email"], row["Password"]
            print(f"Attempting to vote with account: {email}")

            if vote(email, password):  # If successful, remove from file
                df.drop(index=index, inplace=True)  # Delete row immediately
                success = True
                break  # Exit loop after a successful vote to reload DataFrame

        if success:  # Only save if a row was removed
            df.to_excel(credentials_file, index=False)
        else:
            driver.quit()
            exit()
        #n = n + 1
        #if n == 10:
        #    print("Sleeping for 5 minutes to avoid rate limits...")
        #    time.sleep(310)
        #    n = 0

    except Exception as e:
        print(f"Error occurred: {e}")
        break

# Close the browser after all votes
driver.quit()
