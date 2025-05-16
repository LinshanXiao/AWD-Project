from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time, os

# ----------- Configuration -----------
BASE_URL = "http://localhost:5000"
USER_A = {"username": "userA", "password": "passwordA"}
USER_B = {"username": "userB", "password": "passwordB"}
USER_B_ID = 2  # Replace with actual userB ID

# ----------- Launch browser -----------
options = Options()
# options.add_argument("--headless")  # optional
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

def login(user):
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(user["username"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)

    if "login" in driver.current_url.lower():
        os.makedirs("debug", exist_ok=True)
        with open("debug/login_failed.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("debug/login_failed.png")
        return False
    return True

def logout():
    driver.get(f"{BASE_URL}/logout")
    time.sleep(1)

def send_friend_request(from_user, to_user_id):
    if not login(from_user):
        return False

    driver.execute_script(f"""
        fetch('/add_friend', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{ friend_id: {to_user_id} }})
        }});
    """)
    time.sleep(1)
    logout()
    return True

def accept_friend_request(user, expected_friend_name):
    if not login(user):
        return False

    driver.get(f"{BASE_URL}/notifications")
    try:
        accept_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "accept-button")))
        accept_button.click()
        time.sleep(1)

        friend_names = driver.find_elements(By.CLASS_NAME, "access-friend-name")
        if any(expected_friend_name in f.text for f in friend_names):
            logout()
            return True
    except:
        pass

    os.makedirs("debug", exist_ok=True)
    driver.save_screenshot("debug/accept_failed.png")
    with open("debug/accept_failed.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    logout()
    return False

# ----------- Run test -----------
try:
    print("=== 🧪 Running friend system test ===")

    if send_friend_request(USER_A, USER_B_ID):
        print("✅ Friend request sent from User A to User B")
    if accept_friend_request(USER_B, USER_A["username"]):
        print("✅ Friend request accepted by User B")

finally:
    driver.quit()