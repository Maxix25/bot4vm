from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, sys, os
import requests

# DEVELOPMENT
# from dotenv import load_dotenv
# load_dotenv()

def log(text):
	print(text)
	sys.stdout.flush()

def webhook(body):
	url = str(os.environ.get('WEBHOOK_URL'))
	values = {'username': 'VM Bot', 'content': body}
	response = requests.post(url, data=values)
	log(f"Webhook response={'👎' if response.text else '👍'}")


class Bot():
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
		webhook("Starting VM Bot! 🖥️")
		error_count = 0

		try:
			driver.get("https://ide.goorm.io/")
			time.sleep(3)
			log("Logging in...")

			#signin_btn = driver.find_element_by_xpath("//*[text()='Sign In']")}
			signin_btn = driver.find_element_by_xpath("//span[1]")
			signin_btn.click()
			time.sleep(5)

			email_field = driver.find_element_by_name("email")
			email_field.send_keys(email, Keys.TAB, password, Keys.RETURN)
			time.sleep(5)
			log("Bot logged in successfully!")

			self.run_container()
			time.sleep(120)

		except Exception as e:
			log(f"ERROR_MSG={e}")


		while True:
			try:
				self.type_cmd(os.environ.get('CMD_TO_RUN'))
				time.sleep(3600)
			except Exception as e:
				log(f"Encountered error while typing command!\nERROR_MSG={e}")
				webhook("Encountered error while typing command! Check logs for more info.")
				error_count+=1

				if error_count > 5:
					webhook("Too many errors! All creator's fault... Shutting down...")
					self.mission_abort()

	def run_container(self):
		driver = self.driver
		driver.execute_script("window.scrollTo(0, 450)")
		run_btn = driver.find_elements_by_xpath(f"/html/body/div[1]/section[2]/div/section/div[2]/div[5]/div[2]/div/button")
		run_btn[0].click()
		driver.switch_to.window(driver.window_handles[1])

	def type_cmd(self, command):
		driver = self.driver
		terminal = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[3]/div[1]/div[2]/div')
		terminal.send_keys(command, Keys.RETURN)

	def mission_abort(self):
		sys.exit(0)


awake = (os.environ.get('AWAKE').lower() == 'true')
if awake:
	bot = Bot(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
else:
	log("Bot is asleep....")
