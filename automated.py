from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import time

class OrangeHRMAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)  # Increased wait time
        
    def login(self, username, password):
        try:
            # Navigate to the website
            self.driver.get("https://opensource-demo.orangehrmlive.com")
            
            # Wait for username field and login
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)
            
            # Enter password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for dashboard to load
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-main-menu"))
            )
            print("Login successful!")
            
        except Exception as e:
            print(f"Login failed! Error: {str(e)}")
            self.take_screenshot("login_error")
            raise
    
    def wait_for_loader_to_disappear(self):
        """Wait for the loader to disappear"""
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "oxd-form-loader"))
            )
        except:
            pass

    def apply_leave(self):
        try:
            # Click on Leave menu
            leave_menu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Leave']"))
            )
            leave_menu.click()
            
            # Wait for loader to disappear
            self.wait_for_loader_to_disappear()
            
            # Click Apply
            apply_button = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Apply"))
            )
            apply_button.click()
            
            # Wait for loader to disappear
            self.wait_for_loader_to_disappear()
            time.sleep(2)  # Additional wait for page stability
            
            # Wait for leave type dropdown and click using JavaScript
            leave_type_dropdown = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-select-text"))
            )
            self.driver.execute_script("arguments[0].click();", leave_type_dropdown)
            
            # Wait and select Casual Leave using JavaScript
            casual_leave = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='CAN - Casual Leave']"))
            )
            self.driver.execute_script("arguments[0].click();", casual_leave)
            
            # Calculate dates
            tomorrow = datetime.now() + timedelta(days=1)
            day_after = datetime.now() + timedelta(days=2)
            
            # Clear and enter From Date
            from_date = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//label[text()='From Date']/following::input[1]"))
            )
            self.driver.execute_script("arguments[0].value = '';", from_date)
            from_date.send_keys(tomorrow.strftime('%Y-%m-%d'))
            
            # Clear and enter To Date
            to_date = self.driver.find_element(
                By.XPATH, "//label[text()='To Date']/following::input[1]"
            )
            self.driver.execute_script("arguments[0].value = '';", to_date)
            to_date.send_keys(day_after.strftime('%Y-%m-%d'))
            
            # Wait for loader to disappear
            self.wait_for_loader_to_disappear()
            
            # Add comment
            comment = self.driver.find_element(
                By.XPATH, "//textarea[@placeholder='Type here']"
            )
            comment.send_keys("Automated test leave application")
            
            # Wait and click Submit using JavaScript
            submit_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            
            # Verify success message
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "oxd-toast"))
            )
            
            if "Successfully" in success_message.text:
                print("Leave applied successfully!")
            else:
                print("Leave application might have failed!")
                
        except Exception as e:
            print(f"Leave application failed! Error: {str(e)}")
            self.take_screenshot("leave_error")
            raise
            
    def take_screenshot(self, name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.driver.save_screenshot(f"{name}_{timestamp}.png")
        
    def cleanup(self):
        if self.driver:
            self.driver.quit()

def main():
    automation = OrangeHRMAutomation()
    try:
        # Login
        automation.login("Admin", "admin123")
        
        # Wait for page to load completely
        time.sleep(3)
        
        # Apply Leave
        automation.apply_leave()
        
    except Exception as e:
        print(f"Test failed! Error: {str(e)}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()