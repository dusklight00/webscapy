from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class Webscapy:
    def __init__(self):
        pass

    def setup_driver(self, headless = True, executable_path = None, remote_url = None):
        if remote_url is not None:
            self.create_remote_driver(remote_url)
        else:
            self.create_offline_driver(headless, executable_path)
    
    def create_remote_driver(self, remote_url = None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("browserVersion", "67")
        chrome_options.set_capability("platformName", "Windows XP")
        self.driver = webdriver.Remote(
            command_executor = remote_url, 
            options = chrome_options
        )

    def create_offline_driver(self, headless = True, executable_path = None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument('--disable-gpu')
        if headless:
            chrome_options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        if executable_path is not None:
            self.driver = webdriver.Chrome(
                service = service, 
                options = chrome_options,
                executable_path = executable_path
            )
        else:
            self.driver = webdriver.Chrome(
                service = service, 
                options = chrome_options
            )

    def load_wait(self, xpath):
        delay = 9999
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False
    
    def load_element(self, xpath):
        return self.driver.find_element('xpath', xpath)

    def get(self, url):
        self.driver.get(url)
    
    def get_network_data(self):
        network_data_retriever_script = """
            const performance = window.performance || 
                            window.mozPerformance || 
                            window.msPerformance || 
                            window.webkitPerformance || 
                            {};

            const network = performance.getEntries() || {}; 

            return network;
        """

        network_data = self.driver.execute_script(network_data_retriever_script)

        return network_data
    
    def close(self):
        self.driver.close()