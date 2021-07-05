##########project configurations#########
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import logging
import sys
# from batting.constants import *
LOGFILE = "testlog"
logging.basicConfig(filename=LOGFILE, 
                    format='%(asctime)s %(message)s', 
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

class Config(object):
	"""docstring for Config"""
	def __init__(self):
		super(Config, self).__init__()
		self.driver = None
		self.wait_attrib = None
		self.betcris_username = 'PE157459'
		self.betcris_password = 'Peru2024.'
		self.xbet_username = '244498881'
		self.xbet_password = 'y6hfrsfa'
		self.logger = logger
		
	def drivers(self):
		capa = DesiredCapabilities.CHROME
		capa["pageLoadStrategy"] = "none"
		options = Options()
		options.add_argument('start-maximized')
		prefs = {
		"translate_whitelists": {"pt":"en"},
		"translate":{"enabled":"true"}
		}
		options.add_experimental_option("prefs", prefs)
		options.add_extension('./translate.crx')
		options.add_experimental_option("useAutomationExtension", False)
		options.add_experimental_option("excludeSwitches",["enable-automation"])
		# options.add_argument("--incognito")

		proxy = Proxy()
		proxy.proxyType = ProxyType.MANUAL
		proxy.autodetect = False
		proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = "127.0.0.1:9000"
		options.Proxy = proxy
		options.add_argument("ignore-certificate-errors")
		self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options,desired_capabilities=capa)
		# self.driver.maximize_window()
		return self.driver

	def wait(self):
		self.wait_attrib = WebDriverWait(self.driver, 20)
		return self.wait_attrib