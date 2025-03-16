import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Load credentials from Excel
credentials_file = "credentials.xlsx"
df = pd.read_excel(credentials_file)

chromedriver_autoinstaller.install()

# Selenium WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

#service = Service("path/to/chromedriver")  # Update with actual path to chromedriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)  # Explicit wait for elements

driver.get("https://www.grandefratello.mediaset.it/vota/")
time.sleep(8)

# Click "VAI AL TELEVOTO"
# try:
#    time.sleep(5)

# Check for ads

ads_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[11]/div/div/a')))
if ads_button.is_displayed():
    ads_button.click()

wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/button/div/h3/span'))).click()
time.sleep(2)

driver.switch_to.frame("modal-frame")


# except:
#    print("VAI AL TELEVOTO button not found, skipping...")
#    return

def vote(email, password):

    # Click "Accedi"
    try:
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/button'))).click()
        time.sleep(2)
    except:
        print("Accedi button not found, assuming logout...")
        time.sleep(2)
        logout_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
        if logout_button.is_enabled():
            logout_button.click()
            time.sleep(2)
    #        time.sleep(3)
    #        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/button'))).click()
    #        time.sleep(2)
    #        print("Logging in again...")
        return

    # Enter email
    try:
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[1]/input')))
        email_input.clear()
        email_input.send_keys(email)
    except:
        print(f"Unable to find email input field for {email}, skipping...")
        return

    # Enter password
    try:
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[2]/input')))
        password_input.clear()
        password_input.send_keys(password)
    except:
        print(f"Unable to find password input field for {email}, skipping...")
        return

    # Click "Invia"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/form/div[2]/div[3]/div[6]/input'))).click()
        time.sleep(2)
    except:
        print(f"Invia button not found for {email}, skipping...")
        return

    # Verify if login was successful
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
        print(f"Successfully logged in with {email}")
    except:
        print(f"Login failed for {email}, skipping...")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/a'))).click()

        return

    # First vote
    try:
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div'))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/button'))).click()
        time.sleep(2)
    except:
        print("Voting elements not found, skipping...")
        return

    # Check for "Vota ancora" or "Attenzione!"
    try:
        time.sleep(2)
        vota_ancora_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/img')))

        if vota_ancora_button.is_displayed():

            print("2nd vote")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/button'))).click()
            time.sleep(1)

            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div'))).click()
            time.sleep(1)
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/button'))).click()

            print("3rd vote")
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/button'))).click()
            time.sleep(1)

            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div/div'))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/button'))).click()
            time.sleep(2)


            print("1. Vote complete. Chiudi found need to logout...")
            logout_button = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
            logout_button.click()
            time.sleep(2)
            #chiudi_button.click()
            #time.sleep(3)
            return

    except:
        print("No 'Vota ancora' button detected, assuming 'Attenzione!' page")

        time.sleep(2)

        print("2. Vote complete. Chiudi found need to logout...")
        logout_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/header/div/button')))
        logout_button.click()
        time.sleep(2)

#    time.sleep(2)

# Loop through all credentials
for index, row in df.iterrows():
    print(f"Attempting to vote with account: {row['Email']}")
    vote(row['Email'], row['Password'])

# Close the browser after all votes
driver.quit()
