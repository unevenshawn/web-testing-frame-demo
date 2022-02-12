from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from api import logUtil



def driver():
    # service = Service(r"C:\Users\Uneven\Desktop\codes\python\chromedriver.exe")
    # driver = webdriver.Chrome(service=service)
    driver=DriverManager.driver()
    return driver

def clear():
    DriverManager.clear()

class DriverManager:
    dvs = []

    service_store=None

    @classmethod
    def service(cls):
        if not cls.service_store:
            service = Service(r"C:\Users\Uneven\Desktop\codes\python\chromedriver.exe")
            # cls.service_store=service
        else:
            service = cls.service_store
        return service

    @classmethod
    def driver(cls):
        service = cls.service()
        driver = webdriver.Chrome(service=service)
        cls.dvs.append(driver)
        return driver


    @classmethod
    def clear(cls):
        for d in cls.dvs:
            d.service.stop()
        cls.dvs.clear()

if __name__ == '__main__':
    pass
