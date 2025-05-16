import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

class SystemLoginTest(unittest.TestCase):
    def setUp(self):
        service = Service("./chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        driver.find_element(By.NAME, "username").send_keys("tester")
        driver.find_element(By.NAME, "password").send_keys("Test123!")
        driver.find_element(By.NAME, "submit").click()

        time.sleep(2)  

        
        self.assertIn("Welcome to GameNalyzer", driver.page_source)

if __name__ == '__main__':
    unittest.main()
