import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_helper import *
import selenium

from api.logUtil import info_log


def temp():
    driver = get_webdriver()
    driver.get("https://cn.bing.com/")
    ele = driver.find_element(By.TAG_NAME, "div")
    print(type(ele), ele.id, ele.text, ele.accessible_name)
    eles = driver.find_elements(By.TAG_NAME, "div")  # eles是一个list
    print(type(eles), len(eles))
    # driver.find_element(By.ID, "sb_form_q").send_keys("selenium test automation")
    srch_icon = driver.find_element(By.ID, "search_icon")
    srch_icon.click()
    # 以上为selenium代码执行元素点击，以下为js代码执行点击指令
    # driver.execute_script("return arguments[0].click()",srch_icon)
    driver.switch_to.new_window("window")
    # driver.switch_to.new_window("tab")
    # WebDriverWait(driver,20)
    time.sleep(1)
    driver.quit()


def instance():
    driver = webdriver.Chrome(service=Service(r"C:\Users\Uneven\Desktop\codes\python\knowledge\chromedriver.exe"))
    driver.get(url="https://www.baidu.com")
    ele = driver.find_element(By.XPATH, '//*[@id="kw"]')
    ele.send_keys("selenium test automation")
    time.sleep(2)
    ele.submit()
    # driver.find_element(By.ID,"su").click()
    # (By.XPATH, '//*[@id="tsn_inner"]/div[2]/div')
    WebDriverWait(driver, 10).until(element_to_be_clickable((By.XPATH, '//*[@id="tsn_inner"]/div[2]/div')))

    time.sleep(3)
    driver.quit()


def main():
    # print("开始")
    temp()
    # instance()


if __name__ == '__main__':
    main()
