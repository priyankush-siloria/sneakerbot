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
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',"ecombot.settings")

# from botapp.models import UserProfile,Category,OrderedItem,SneakerItem,AllSkuSize,AvalSkuSize

from dotenv import load_dotenv

from .config import Config

load_dotenv()
 
class EcomBot(object):
	"""docstring for EcomBot"""
	def __init__(self, conf,data_center=None):
		super(EcomBot, self).__init__()
		self.conf = Config()
		self.logger = self.conf.logger
		self.driver = self.conf.drivers()
		self.base_url = 'https://www.artwalk.com.br'
		self.url = self.base_url+"/calendario-sneaker"
		self.driver.get(self.url)
		self.after_checkout_url = 'https://www.artwalk.com.br/checkout#/cart'
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


		crawl_sneaker = os.environ.get('SCRAPE_SNEARKER').replace("'","")

		if False:
			self.scrape_sneaker()
			time.sleep(10)
			self.driver.quit()

			try:
				self.driver.get("https://www.artwalk.com.br/")
			except Exception as e:
				print(e)
		else:
			nextButton = self.driver.find_element_by_xpath('/html/body/header/div/div/div')
			a = ActionChains(self.driver)
			a.move_to_element(nextButton).perform()
			self.driver.implicitly_wait(10)
			self.driver.find_element_by_xpath('/html/body/header/div/div/div/nav/ul/li[3]/a').click()
			self.user_detail_dict = {}

			self.login()
			self.add_to_cart()
			self.get_order_items()
			self.place_order()
			print("Hola!!! clicked!!!!")
			self.data_center = data_center


	def popup(self):
		try:
			self.driver.find_element_by_xpath('//*[@id="btn-seller-default"]').click()
		except Exception as msg:
			print(str(msg))
			print("Unable to dismiss popup blocker")
	
	def is_login(self):
		if self.driver.after_login_url==self.driver.current_url:
			return True
	
	def login(self):
		try:
			nextButton = self.driver.find_elements_by_xpath('//*[@id ="loginWithUserAndPasswordBtn"]')
			nextButton[0].click()
			self.driver.implicitly_wait(15)
			time.sleep(2)
			loginBox = self.driver.find_element_by_xpath('//*[@id ="inputEmail"]')
			loginBox.send_keys(self.EMAIL_DATA)
			passWordBox = self.driver.find_element_by_xpath('//*[@id ="inputPassword"]')
			passWordBox.send_keys(self.PASSWORD_DATA)
			nextButton = self.driver.find_elements_by_xpath('//*[@id ="classicLoginBtn"]')
			nextButton[0].click()
			print('Login Successful...!!')
		except:
			print('Login Failed')



	def add_to_cart(self):
		megaMenuButton = self.driver.find_element_by_xpath('//*[@class ="nav-item has-submenu"]')
		a = ActionChains(self.driver)
		a.move_to_element(megaMenuButton).perform()
		# self.driver.get('https://www.artwalk.com.br/T%C3%AAnis?PS=24&map=specificationFilter_16&O=OrderByReleaseDateDESC');
		self.driver.get('https://www.artwalk.com.br/calendario-sneaker');

		recentSneakerBtn = self.driver.find_element_by_xpath('//div[@class="bt-categoria prox-recente"]')
		recentSneakerBtn.click()


		wait = WebDriverWait(self.driver, 40)
		element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-seller-default"]')))
		soup = BeautifulSoup(self.driver.page_source,'html.parser')
		sku_collection = soup.find('input', {'id':'___rc-p-sku-ids'}).get('value')
		sku_collection = sku_collection.split(',')

		print(sku_collection,'sku_collection sku_collection')

		size_collection = soup.find_all('input', {'class':'skuselector-specification-label'})

		# for indv_size in size_collection:
		# 	print(type(indv_size))
		# 	print(indv_size)
		# 	print(indv_size['class'])


		unavaible_indices = []
		final_size_collection = []

		count_m=0

 
		for i,j in zip(sku_collection,size_collection):
			ind_class = j['class'][-1]
			ind_class_val = j['data-value']
			if ind_class=='item_unavailable':
				unavaible_indices.append(count_m)
			count_m+=1
			final_size_collection.append(ind_class_val)
		new_sku_collection = [v for i, v in enumerate(sku_collection) if i not in unavaible_indices]
		new_size_collection = [v for i, v in enumerate(final_size_collection) if i not in unavaible_indices]

		self.final_size_collection=final_size_collection
		self.sku_collection = sku_collection
		self.new_sku_collection = new_sku_collection
		self.new_size_collection = new_size_collection

		element.click();
		try:
			addToCartButton = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/a[1]')
			addToCartButton.click()
		except:
			addToCartButtonLang = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/a[1]')
			addToCartButtonLang.click()
	def scrape_sneaker(self):
		time.sleep(20)
		self.logger.info("Sneaker Scrapping function is started")
		self.driver.get(self.url)

		page = self.driver.page_source
		soup = BeautifulSoup(page,'html.parser')

		sneaker_group = soup.find_all('div', {'class':'box-banner'})


		for sneaker in sneaker_group:
			img_url = sneaker.find('img').get("src")
			sneaker_name = ' '.join(sneaker.find('img').get("alt").split()[2::])
			sku = sneaker.find('img').get("id").split('/')[-2]
			# SneakerItem.objects.create(sneaker_name=sneaker_name,image=img_url,sku=sku)


	def get_order_items(self):
		time.sleep(20)
		page = self.driver.page_source
		soup = BeautifulSoup(page,'html.parser')
		product_group = soup.find_all('tr', {'class':'product-item'})
		count=0
		product_items_detail = []

		try:
			wait = WebDriverWait(self.driver, 10)
			element = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="link-choose-more-products-wrapper"]')))
			self.driver.get('https://www.artwalk.com.br/calendario-sneaker');
			recentSneakerBtn = self.driver.find_element_by_xpath('//div[@class="bt-categoria prox-recente"]')
			recentSneakerBtn.click()
			self.add_to_cart()
			self.get_order_items()
			action= False		
		except Exception as e:
			action= True
		if action:
			self.logger.info("Scrapping ordered product.")
			for product in product_group:
				count+=1
				sku=product.get_attribute_list('data-sku')[0]
				product_id = 'product-name'+sku
				product_item = product.find('td',{'class':'product-name'})
				product_name = product.find('a',{'id':product_id}).text
				price = product.find('span',{'class':'new-product-price'}).text
				product_amt_id = 'item-quantity-'+sku
				size = product_name.split()[-1]
				time.sleep(10)
				total_price = product.find('span',{'class':'total-selling-price'}).text
				amount = float((total_price.split()[-1]).replace(',',''))//float((price.split()[-1]).replace(',',''))
				self.user_profile,p=UserProfile.objects.get_or_create(first_name=self.FIRST_NAME,last_name=self.LAST_NAME,email=self.EMAIL_DATA,password=self.PASSWORD_DATA)
				order_item_object = OrderedItem.objects.create(user=self.user_profile,product_name=product_name,quantity=amount,price=price,total_price=total_price)
				all_sku_objs = [AllSkuSize(sku=i,size=j,sneaker_item=order_item_object) for i,j in zip(self.sku_collection,self.final_size_collection)]
				sku_objs = [AvalSkuSize(sku=i,size=j,sneaker_item=order_item_object) for i,j in zip(self.new_sku_collection,self.new_size_collection)]
				AllSkuSize.objects.bulk_create(all_sku_objs)
				# AvalSkuSize.objects.bulk_create(sku_objs)
				# self.user_profile,p=UserProfile.objects.get_or_create(first_name=self.FIRST_NAME,last_name=self.LAST_NAME,email=self.EMAIL_DATA,password=self.PASSWORD_DATA)
				# order_item_object=OrderedItem.objects.create(user=self.user_profile,product_name=product_name,quantity=amount,price=price,total_price=total_price)
				

		print(product_items_detail)



	def place_order(self):
		firstnameInput = self.driver.find_element_by_xpath('//input[@id ="client-first-name"]')
		firstnameInput.send_keys(self.FIRST_NAME)
		lastnameInput = self.driver.find_element_by_xpath('//input[@id ="client-last-name"]')
		lastnameInput.send_keys(self.LAST_NAME)
		cpfInput = self.driver.find_element_by_xpath('//input[@id ="client-document"]')
		cpfInput.send_keys(self.CPF)
		phoneInput = self.driver.find_element_by_xpath('//input[@id ="client-phone"]')
		phoneInput.send_keys(self.PHONE_NUMBER)

		time.sleep(2)
		submitOrderBtn = self.driver.find_element_by_xpath('//button[@id ="go-to-shipping"]')
		submitOrderBtn.click()

	def match_data_scrape(self, url_path):
		wait = self.conf.wait()
		url = self.base_url+url_path
		print(url)
		self.driver.get(url)

	def load_json_data(self):
		file_path =  self.scrape_url_file
		data = open(file_path).read()
		data = json.loads(data)
		return data

	def test_scrap(self):
		s="ENGLAND - PREMIER LEAGUE "
		#s='27.11 19:30'
		data=self.load_json_data()
		for x in data:
			if s == x["names"]:
				self.match_data_scrape(x["links"])
			else:
				print("nodata")

	def scrape_live_match_data(self):
		pass

	def check_live_maches(self):
		self.driver.find_element_by_xpath('//*[@id="collapseDashboardMenu"]/div/ul/li[1]/a').click()
		page = self.driver.page_source
		soup = BeautifulSoup(page,'html.parser')
		scedule = soup.find('div',{'class':'schedule-holder'})
		rows = scedule.find_all('div',{'class':"row no-gutters"})
		imp_live = [] 
		for row in rows:
			team1 = row.find('div',class_="home")
			team2 = row.find('div',class_="visitor")
			link = row.find_all('div',recursive=False)[-1].find('a',href=True)
			if link and team1 and team2:
				link = link['href']
				team1 = team1.text.strip()
				team2 = team2.text.strip()

				imp_live.append()
				print(team1)
				print(team2)
				print(link)


# bet = EcomBot(Config())