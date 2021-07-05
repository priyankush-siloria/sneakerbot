import time
import json
from bs4 import BeautifulSoup
from selenium import common
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import re
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',"ecombot.settings")

# from botapp.models import UserProfile,Category,OrderedItem,SneakerItem,AllSkuSize,AvalSkuSize


from .config import Config
 
class EcomBot(object):
	"""docstring for EcomBot"""
	def __init__(self, conf,data_center=None):
		super(EcomBot, self).__init__()
		self.conf = Config()
		self.logger = self.conf.logger
		self.driver = self.conf.drivers()
		self.base_url = 'https://www.nike.com'
		self.login_url = 'https://www.nike.com/in/login/'
		self.url = self.base_url+"/in/"
		self.driver.get(self.url)
		self.after_checkout_url = 'https://www.nike.com/in/cart'
		self.scrape_url_file = 'ecom_url.json'
		time.sleep(5)
		self.user_profile = None

		#end user detail
		self.EMAIL_DATA = os.environ.get('EMAIL_DATA')
		self.PASSWORD_DATA = os.environ.get('PASSWORD_DATA')
		self.FIRST_NAME = os.environ.get('FIRST_NAME')
		self.LAST_NAME = os.environ.get('LAST_NAME')
		self.CPF = os.environ.get('CPF')
		self.PHONE_NUMBER = os.environ.get('PHONE_NUMBER')

		# self.login()
		self.add_to_cart()
	def popup(self):
		try:
			self.driver.find_element_by_xpath('//*[@id="btn-seller-default"]').click()
		except Exception as msg:
			print(str(msg))
			print("Unable to dismiss popup blocker")
	
	def is_login(self):
		if self.driver.after_login_url==self.driver.current_url:
			return True

	# def add_to_cart(self):
	# 	time.sleep(5)
	# 	self.driver.get('https://www.nike.com/in/');

	def slow_typing(self,param,ele):
		self.chice_list=[0.2,0.4,0.5,0.3]
		for character in param:
			ele.send_keys(character)
			time.sleep(random.choice(self.chice_list))


	def login(self):
		self.driver.get(self.login_url)
		try:
			self.driver.implicitly_wait(15)
			# time.sleep(2)
			# nextButton = self.driver.find_elements_by_xpath('//*[@data-var="loginBtn"]')
			# nextButton[0].click()
			loginBox = self.driver.find_element_by_xpath('//*[@data-componentname="emailAddress"]')
			print(self.EMAIL_DATA)
			# loginBox.send_keys('webevnt2@gmail.com')
			self.slow_typing('webevnt2@gmail.com',loginBox)
			time.sleep(5)
			passWordBox = self.driver.find_element_by_xpath('//*[@data-componentname="password"]')
			# passWordBox.send_keys('7779833188Uv')
			self.slow_typing('7779833188Uv',passWordBox)
			time.sleep(5)
			nextButton = self.driver.find_elements_by_xpath('//div[@class="nike-unite-submit-button loginSubmit nike-unite-component"]')
			nextButton[0].click()
			time.sleep(20)
			# self.driver.implicitly_wait(25)
			print('Login Successful...!!')
		except:
			print('Login Failed')


	def add_to_cart(self):
		
		self.driver.get('https://www.nike.com/in/w/new-mens-shoes-3n82yznik1zy7ok')

		wait = WebDriverWait(self.driver, 40)
		element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="product-card css-1jijlv2 css-z5nr6i css-11ziap1 css-14d76vy css-dpr2cn product-grid__card "]')))
		print("waiting")
		time.sleep(5)
		element.click()
		product_id = self.driver.find_element_by_xpath()
		# self.driver.find_element_by_xpath()
		print(element, "element")


		# element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-seller-default"]')))
		# soup = BeautifulSoup(self.driver.page_source,'html.parser')
		# sku_collection = soup.find('input', {'id':'___rc-p-sku-ids'}).get('value')
		# sku_collection = sku_collection.split(',')

		# print(sku_collection,'sku_collection sku_collection')

		# size_collection = soup.find_all('input', {'class':'skuselector-specification-label'})

		# for indv_size in size_collection:
		# 	print(type(indv_size))
		# 	print(indv_size)
		# 	print(indv_size['class'])


		# unavaible_indices = []
		# final_size_collection = []

		# count_m=0

 
		# for i,j in zip(sku_collection,size_collection):
		# 	ind_class = j['class'][-1]
		# 	ind_class_val = j['data-value']
		# 	if ind_class=='item_unavailable':
		# 		unavaible_indices.append(count_m)
		# 	count_m+=1
		# 	final_size_collection.append(ind_class_val)
		# new_sku_collection = [v for i, v in enumerate(sku_collection) if i not in unavaible_indices]
		# new_size_collection = [v for i, v in enumerate(final_size_collection) if i not in unavaible_indices]

		# self.final_size_collection=final_size_collection
		# self.sku_collection = sku_collection
		# self.new_sku_collection = new_sku_collection
		# self.new_size_collection = new_size_collection

		# element.click()
		# try:
		# 	addToCartButton = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/a[1]')
		# 	addToCartButton.click()
		# except:
		# 	addToCartButtonLang = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/a[1]')
		# 	addToCartButtonLang.click()


# bet = EcomBot(Config())