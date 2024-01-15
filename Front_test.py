from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set the path to your ChromeDriver executable
chromedriver_path = 'https://github.com/photop33/Proceed-Test/chromedriver.exe'  # Change this to the actual path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"executable_path={chromedriver_path}")
driver = webdriver.Chrome(options=chrome_options)
username='lior'
password='12345'

driver.get("http://localhost:5000")
time.sleep(5)

# Find the input element by XPath
driver.find_element("xpath", '//*[@id="username"]').send_keys(username)
driver.find_element("xpath", '//*[@id="password"]').send_keys(password)
driver.find_element("xpath", '/html/body/form/input[3]').click()
time.sleep(2)
current_url = driver.current_url

# Print or use the URL as needed
print("Current URL:", current_url)
target_url = 'http://localhost:5000/enable-mfa/' + username
try:
    if current_url == target_url:
        print('Front Test Success!')
        driver.quit()
except:
    print('front test failed :(')
    driver.quit()
