import time
import os
import sys
import requests
from helium import *

def log(text):
	print("LOG:", text)
	sys.stdout.flush()
start_chrome("ide.goorm.io", headless = True)
click("Get Started")
time.sleep(5)
write(os.environ.get("EMAIL"))
log("Bot wrote email")
press(TAB)
log("Bot pressed tab")
write(os.environ.get("PASSWORD"))
log("Bot wrote password")
click("Login")
log("Bot pressed Login")
time.sleep(3)
go_to("https://ide-run.goorm.io/workspace/MySql?language=us")
log("Bot is running the container")
time.sleep(10)
while True:
	write("ls")
	press(ENTER)
	time.sleep(10)
