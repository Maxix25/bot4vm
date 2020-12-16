import time
import os
import sys
import requests
from helium import *

def log(text):
	print("LOG:", text)
	sys.stdout.flush()

def webhook(body):
	url = os.environ.get("WEBHOOK_URL")
	values = {'username': 'VM Bot', 'content': body}
	response = requests.post(url, data = values)
	log(f"Webhook response={'false' if response.text else 'true'}")

start_chrome("ide.goorm.io", headless = True)
click("Get Started")
time.sleep(5)
write(os.environ.get("EMAIL"))
press(TAB)
write(os.environ.get("PASSWORD"))
click("Login")
webhook("Bot logged in!")
time.sleep(3)
go_to("https://ide-run.goorm.io/workspace/MySql?language=us")
webhook("Container is running!")
time.sleep(10)
while True:
	write("ls")
	press(ENTER)
	time.sleep(10)
