from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import json


class Webscapy:
    def __init__(
        self,
        headless=True,
        executable_path=None,
        remote_url=None,
        undetected=False,
        version=None,
    ):
        self.setup_driver(headless, executable_path, remote_url, undetected, version)

    def setup_driver(
        self,
        headless=True,
        executable_path=None,
        remote_url=None,
        undetected=False,
        version=None,
    ):
        if remote_url is not None:
            self.create_remote_driver(remote_url)
        else:
            if undetected:
                self.create_undetected_driver(headless, executable_path, version)
            else:
                self.create_offline_driver(headless, executable_path)

    def create_undetected_driver(
        self, headless=True, executable_path=None, version=None
    ):
        if executable_path is None:
            chrome_manager = ChromeDriverManager()
            executable_path = chrome_manager.install()
            version = int(
                chrome_manager.driver.get_browser_version_from_os().split(".")[0]
            )
        elif version is None:
            raise Exception("Version of the executable path is not provided")
        options = uc.ChromeOptions()
        options.headless = headless
        self.driver = uc.Chrome(
            use_subprocess=True,
            driver_executable_path=executable_path,
            version_main=version,
            options=options,
        )

    def create_remote_driver(self, remote_url=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("browserVersion", "67")
        chrome_options.set_capability("platformName", "Windows XP")
        self.driver = webdriver.Remote(
            command_executor=remote_url, options=chrome_options
        )

    def create_offline_driver(self, headless=True, executable_path=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-gpu")
        if headless:
            chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        if executable_path is not None:
            self.driver = webdriver.Chrome(
                service=service, options=chrome_options, executable_path=executable_path
            )
        else:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def load_wait(self, type, selector, timeout = 9999):
        selector_obj = None
        if type == "id":
            selector_obj = By.ID
        if type == "name":
            selector_obj = By.NAME
        if type == "xpath":
            selector_obj = By.XPATH
        if type == "link-text":
            selector_obj = By.LINK_TEXT
        if type == "partial-link-text":
            selector_obj = By.PARTIAL_LINK_TEXT
        if type == "tag-name":
            selector_obj = By.TAG_NAME
        if type == "class-name":
            selector_obj = By.CLASS_NAME
        if type == "css-selector":
            selector_obj = By.CSS_SELECTOR

        if selector_obj == None:
            return False

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((selector_obj, selector))
            )
            return True
        except TimeoutException:
            return False

    def load_element(self, type, selector):
        if type == "id":
            return self.driver.find_element(By.ID, selector)
        if type == "name":
            return self.driver.find_element(By.NAME, selector)
        if type == "xpath":
            return self.driver.find_element(By.XPATH, selector)
        if type == "link-text":
            return self.driver.find_element(By.LINK_TEXT, selector)
        if type == "partial-link-text":
            return self.driver.find_element(By.PARTIAL_LINK_TEXT, selector)
        if type == "tag-name":
            return self.driver.find_element(By.TAG_NAME, selector)
        if type == "class-name":
            return self.driver.find_element(By.CLASS_NAME, selector)
        if type == "css-selector":
            return self.driver.find_element(By.CSS_SELECTOR, selector)
        raise TypeError(f"Type {type} is not a valid type")

    def load_elements(self, type, selector):
        if type == "id":
            return self.driver.find_elements(By.ID, selector)
        if type == "name":
            return self.driver.find_elements(By.NAME, selector)
        if type == "xpath":
            return self.driver.find_elements(By.XPATH, selector)
        if type == "link-text":
            return self.driver.find_elements(By.LINK_TEXT, selector)
        if type == "partial-link-text":
            return self.driver.find_elements(By.PARTIAL_LINK_TEXT, selector)
        if type == "tag-name":
            return self.driver.find_elements(By.TAG_NAME, selector)
        if type == "class-name":
            return self.driver.find_elements(By.CLASS_NAME, selector)
        if type == "css-selector":
            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        raise TypeError(f"Type {type} is not a valid type")

    def wait_load_element(self, type, selector, timeout = 9999):
        self.load_wait(type, selector, timeout)
        return self.load_element(type, selector)

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

    def add_cookie(self, cookie):
        self.driver.add_cookie(cookie)

    def get_cookie(self, name):
        return self.driver.get_cookie(name)
    
    def delete_cookie(self, name):
        self.driver.delete_cookie(name)

    def cookie_editor_parser(self, cookie):
        if cookie["sameSite"] == "lax":
            cookie["sameSite"] = "Lax"
        if cookie["sameSite"] == "no_restriction":
            cookie["sameSite"] = "None"
        if cookie["sameSite"] == "strict":
            cookie["sameSite"] = "Strict"
        return cookie

    def is_host_cookie(self, cookie):
        cookie_name = cookie["name"]
        if cookie_name.startswith("__Host"):
            return True
        return False

    def load_cookie_json(self, path):
        file = open(path, "r")
        cookies = json.load(file)
        for cookie in cookies:
            cookie = self.cookie_editor_parser(cookie)
            cookie_name = cookie["name"]
            if self.get_cookie(cookie_name) is not None:
                self.delete_cookie(cookie_name)
            if self.is_host_cookie(cookie):
                del cookie["domain"]
            self.add_cookie(cookie)

    def close(self):
        self.driver.close()
