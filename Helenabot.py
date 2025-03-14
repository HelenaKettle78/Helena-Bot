import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load credentials from Excel
credentials_file = "credentials.xlsx"
df = pd.read_excel(credentials_file)

# Selenium WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service("path/to/chromedriver")  # Update with actual path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)  # Explicit wait for elements

def vote(email, password):
    driver.get("https://www.grandefratello.mediaset.it/vota/")
    time.sleep(3)

    # Click "VAI AL TELEVOTO"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'VAI AL TELEVOTO')]"))).click()
    except:
        print("VAI AL TELEVOTO button not found")
        return

    time.sleep(2)

    # Click "Logout" if not the first user
    try:
        logout_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Logout')]")))
        if logout_button.is_displayed():
            logout_button.click()
            time.sleep(3)
    except:
        print("Logout button not found, proceeding.")

    # Click "Accedi"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accedi')]"))).click()
    except:
        print("Accedi button not found")
        return

    time.sleep(2)

    # Enter email
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_input.clear()
    email_input.send_keys(email)

    # Enter password
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.clear()
    password_input.send_keys(password)

    # Click "Invia"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Invia')]"))).click()
    except:
        print("Invia button not found")
        return

    time.sleep(5)

    # First vote
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Helena')]"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Vota')]"))).click()
        time.sleep(3)
    except:
        print("Voting elements not found")
        return

    # Check for "Vota ancora" or "Attenzione!"
    try:
        vota_ancora_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Vota ancora')]")))
        if vota_ancora_button.is_displayed():
            vota_ancora_button.click()
            time.sleep(3)

            # Second vote
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Helena')]"))).click()
                time.sleep(2)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Vota')]"))).click()
                time.sleep(3)
            except:
                print("Error during second vote")

            # Click "Vota ancora" again
            try:
                vota_ancora_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Vota ancora')]")))
                vota_ancora_button.click()
                time.sleep(3)

                # Third vote
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Helena')]"))).click()
                    time.sleep(2)
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Vota')]"))).click()
                    time.sleep(3)
                except:
                    print("Error during third vote")
            except:
                print("Second 'Vota ancora' not found, stopping early")

    except:
        print("No 'Vota ancora' button detected, assuming 'Attenzione!' page")

    # Click "Chiudi"
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Chiudi')]"))).click()
    except:
        print("Chiudi button not found")

    time.sleep(2)

# Loop through all credentials
for index, row in df.iterrows():
    print(f"Voting with account {row['Email']}")
    vote(row['Email'], row['Password'])

# Close the browser after all votes
driver.quit()
