import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Set up Chrome WebDriver
chrome_driver_path = "chromedriver.exe"  # Ensure this is in the same folder
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()

# ✅ Bypass detection by pretending to be a real user
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")

# ✅ Launch Chrome
driver = webdriver.Chrome(service=service, options=options)

# ✅ File to store cookies
COOKIE_FILE = "cookies.json"

def save_cookies():
    """Saves cookies after login."""
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "w") as file:
        json.dump(cookies, file)
    print("✅ Cookies saved.")

def load_cookies():
    """Loads cookies if available."""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as file:
            cookies = json.load(file)
        return cookies
    return None

# ✅ Open DeviantArt
driver.get("https://www.deviantart.com")

# ✅ Load cookies before refreshing the page
cookies = load_cookies()
if cookies:
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print("✅ Cookies loaded. Checking if still logged in...")

time.sleep(5)

# ✅ Function to check if logged in
def is_logged_in():
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Sinulated')]")
        return True
    except:
        return False

# ✅ If not logged in, ask user to manually log in
if not is_logged_in():
    print("🔒 Please log in manually.")
    input("Press Enter after logging in...")
    save_cookies()  # ✅ Save cookies after successful login
    driver.refresh()
    time.sleep(5)
    if is_logged_in():
        print("✅ Login detected. Proceeding...")
    else:
        print("❌ Login failed. Restart the script.")
        driver.quit()
        exit()

print("✅ Ready for automation!")

# Function to get links using getlinks.js
def get_album_links():
    album_url = input("📂 Enter the DeviantArt album link: ").strip()
    driver.get(album_url)
    time.sleep(5)

    # ✅ Load and execute `getlinks.js`
    with open("getlinks.js", "r", encoding="utf-8") as js_file:
        js_script = js_file.read()

    driver.execute_script(js_script)  # Run script in the browser

    print("✅ JavaScript injected. Waiting for link collection...")

    time.sleep(10)  # Allow JavaScript time to collect links

    # ✅ Retrieve the collected links
    extracted_links = driver.execute_script("return window.getArtworkUrls();")

    if extracted_links:
        with open("artwork_links.txt", "w") as file:
            file.write("\n".join(extracted_links))
        print(f"✅ Extracted {len(extracted_links)} links and saved to `artwork_links.txt`.")
    else:
        print("❌ No links found. Please check the album URL.")

# ✅ Do NOT quit the browser here! 

# ✅ Check if `artwork_links.txt` exists, otherwise run `get_album_links()`
if not os.path.exists("artwork_links.txt"):
    get_album_links()

print("✅ Process complete.")






# ✅ Function to find the correct delete button
def find_correct_delete_button(driver):
    try:
        # ✅ Find all buttons on the page
        all_buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in all_buttons:
            # ✅ Check if the button contains the delete icon (SVG trash bin)
            try:
                svg = btn.find_element(By.TAG_NAME, "svg")
                svg_path = svg.get_attribute("outerHTML")
                if "M14 3a1 1 0 011 1v1h5a1 1 0 010 2h-1v11.586a1 1 0 01-.293.707l-1.414 1.414a1 1 0 01-.707.293H7.414a1 1 0 01-.707-.293l-1.414-1.414A1 1 0 015 18.586V7H4a1 1 0 110-2h5V4a1 1 0 011-1h4z" in svg_path:
                    print(f"✅ Found delete button")
                    return btn  # ✅ Return the correct button
            except:
                continue  # If no SVG, move to next button

        print("❌ Delete button not found.")
        return None

    except Exception as e:
        print(f"❌ Error finding delete button: {e}")
        return None



# ✅ Function to find and click the confirm delete button using CSS Selector
def confirm_deletion():
    try:
        print("🛑 Waiting for delete confirmation modal...")

        # ✅ Wait for the modal (NO FIXED DELAYS)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Overlay"))
        )

        # ✅ Find all buttons and locate the one with "Delete" text
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        confirm_button = None

        for btn in all_buttons:
            if "Delete" in btn.text.strip():
                confirm_button = btn
                break

        # ✅ Click the confirm delete button as soon as possible
        if confirm_button:
            print("✅ Confirm delete button found. Clicking...")
            driver.execute_script("arguments[0].scrollIntoView();", confirm_button)  # Ensure visibility
            confirm_button.click()
            return True

        print("❌ Confirm delete button not found.")
        return False

    except Exception as e:
        print(f"❌ Error clicking confirm delete button: {e}")
        return False




# ✅ Function to wait for redirect and proceed to next image
def wait_for_redirect():
    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://www.deviantart.com/sinulated")
        )
        print("✅ Redirect detected. Proceeding to next image.")
        return True
    except:
        print("⚠️ Redirect to DeviantArt profile not detected. Skipping.")
        return False

# ✅ Function to delete an artwork and update the file
def delete_artwork(url, urls):
    try:
        driver.get(url)  # Open the artwork page

        # ✅ Wait for the page to load dynamically
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        retries = 0
        while retries < 3:
            try:
                # ✅ Find and click the delete button as soon as it's visible
                delete_button = WebDriverWait(driver, 3).until(lambda d: find_correct_delete_button(d))
                if delete_button:
                    delete_button.click()
                    print(f"🗑 Clicked delete on: {url}")

                    # ✅ IMMEDIATELY wait for the modal (NO fixed sleep)
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Overlay"))
                    )
                    print("🛑 Confirmation modal detected.")

                    # ✅ Click the confirm delete button as fast as possible
                    if confirm_deletion():
                        print("✅ Deletion successful. Removing from list...")
                        urls.remove(url)

                        # ✅ Update file only when necessary
                        if urls:
                            with open("artwork_links.txt", "w") as file:
                                file.write("\n".join(urls))

                        return  # ✅ Exit after successful deletion

                else:
                    print("❌ Delete button not found. Retrying...")
                    retries += 1

            except Exception as e:
                print(f"⚠️ Retry {retries + 1}/3: Delete button click failed ({e}). Trying again...")
                retries += 1

        print(f"❌ Skipping {url} after 3 failed attempts.")

    except Exception as e:
        print(f"❌ Error deleting {url}: {e}")



# ✅ Load the artwork links
if os.path.exists("artwork_links.txt"):
    with open("artwork_links.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]
else:
    urls = []

# ✅ Loop through all URLs and delete them
for url in urls[:]:  # Iterate over a copy to modify the list inside the loop
    delete_artwork(url, urls)
    time.sleep(2)  # Small delay to avoid triggering rate limits

# ✅ After all deletions, check if the file is empty and delete it
if not urls and os.path.exists("artwork_links.txt"):
    os.remove("artwork_links.txt")
    print("🗑 All images deleted. Removed artwork_links.txt.")

# ✅ Close the browser
driver.quit()
print("✅ All artwork deletions completed!")
