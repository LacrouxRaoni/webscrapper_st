#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, datetime, time

driver = webdriver.Chrome()
driver.get('https://www.sociotorcedor.com.br/')
wait = WebDriverWait(driver, 10)

def get_data(data) :
	try :
		file = open(data, 'r').read()
		lst = file.split('\n')
		for i in range(len(lst)) :
			lst[i] = str(lst[i])[5:len(lst[i]) - 1]
			if i == 2 :
				lst[i] = str(lst[i])[6:len(lst[i])]
		return lst
	except Exception as e :
		print(e)

def load_page(idx) :
	try :
		if idx == 0 :
			wait.until(EC.url_changes(driver.current_url))
		elif idx == 1 :
			time.sleep(15)
	except Exception as e:
		print(e)

def account_login(data) :
	driver.find_element(By.LINK_TEXT, 'LOGIN').click()
	driver.switch_to.active_element
	driver.find_element(By.XPATH, ("//*[@id='mat-input-0']")).send_keys(data[0])
	driver.find_element(By.XPATH, ("//*[@id='mat-input-1']")).send_keys(data[1])
	driver.find_element(By.CLASS_NAME, 'login-btn').click()
	load_page(0)

def get_time(file) :
	line = open(file, 'r').read().split('\n')
	old_time = line[len(line) - 2].split(' -')
	hour = datetime.datetime.now().strftime("%c")
	if (old_time[0] > hour) :
		time.sleep(60)

def get_points_in_page(data) :
	driver.find_element(By.LINK_TEXT, 'EXPERIÊNCIAS').click()
	load_page(1)
	return driver.find_element(By.CLASS_NAME, 'header-3-logged__content-user-points')

def save_data_in_file(data, points) :
	line = datetime.datetime.now().strftime("%c") + " - " + str(points.get_attribute('innerHTML')).strip() + "\n"
	open(data[2], "a").write(line)

def logout() :
	driver.find_element(By.CLASS_NAME, 'fengi-exit').click()
	driver.switch_to.active_element
	load_page(1)
	driver.find_element(By.CLASS_NAME, 'swal2-confirm').click()
	# Close the browser
	driver.quit()

def webscrapper(data) :
	account_login(data)
	get_time(data[2])
	points = get_points_in_page(data)
	save_data_in_file(data, points)
	logout()

if __name__ == '__main__' :
	data = get_data(sys.argv[1])
	webscrapper(data)
