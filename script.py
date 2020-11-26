from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys, os
import requests
# DEVELOPMENT
# from dotenv import load_dotenv
# load_dotenv()

def log(text):
	print("LOG:", text)
	sys.stdout.flush()

def webhook(body):
	url = "https://discord.com/api/webhooks/780825549769015318/vcT3OpQRH2VOlI4fy9lD4kzGz_vn9D83LHMEKdn7bJ8L_z-wHc-nmu8TIYGv8-jv8aDa"
	values = {'username': 'VM Bot', 'content': body}
	response = requests.post(url, data=values)
	log(f"Webhook response={'false' if response.text else 'true'}")


class Bot():
	try:
		def __init__(self, email, password):
			# DEVELOPMENT
			# self.driver = webdriver.Chrome()
			# PRODUCTION
			chrome_options = webdriver.ChromeOptions()
			chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_PATH")
			chrome_options.add_argument("--headless")
			chrome_options.add_argument('--disable-dev-shm-usage')
			chrome_options.add_argument('--no-sandbox')
			self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
			driver = self.driver
			error_count = 0

			try:
				driver.get("https://ide.goorm.io/")
				time.sleep(3)
				log("Logging in...")
				print(driver.current_url)

				#signin_btn = driver.find_element_by_xpath("//*[text()='Sign In']")
				signin_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/header/nav/ul/li[1]/a")))
				signin_btn.click()
				print(driver.current_url)
				time.sleep(5)
				log("Sign in button located")
				email_field = driver.find_element_by_name("email")
				password_field = driver.find_element_by_name("password")
				log("Email field found successfully")
				email_field.send_keys(email)
				log("Email written")
				password_field.send_keys(password)
				log("Password written")
				print(email_field.get_attribute("value"))
				print(password_field.get_attribute("value"))
				email_field.send_keys(Keys.RETURN)
				log("Pressed enter")
				time.sleep(5)
				log("Bot logged in successfully!")
				webhook("Bot logged in successfully!")
				self.run_container()

			except ValueError as e:
				log(f"ERROR_MSG={e}")

			webhook("Container is running!")
			terminal = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body")))
			while True:
				terminal.send_keys("ls", Keys.BACKSPACE, Keys.BACKSPACE)
				time.sleep(10)


		def run_container(self):
			driver = self.driver
			driver.execute_script("window.scrollTo(0, 450)")
			print(driver.current_url)
			#run_btn = driver.find_elements_by_xpath("/html/body/div[1]/section[2]/div/section/div[2]/div[5]/div[2]/div/button")
			run_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section[2]/div/section/div[2]/div[5]/div[2]/div/button')))
			run_btn.click()
			driver.switch_to.window(driver.window_handles[1])
			print(driver.current_url)

			

		def mission_abort(self):
			sys.exit(0)
	except Exception as e:
		print(f"ERROR: {e}")
		


bot = Bot(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))

