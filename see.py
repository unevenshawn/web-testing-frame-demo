import os
import queue
import sys
import time
import unittest
from pathlib import Path
import re
import ddt
import pymysql
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from api import seleUtil, logUtil


def enclosure(arg):
    def f(_):
        return arg + "inner circle"

    return


class Jasper:
    def __new__(cls, args) -> tuple:
        return args

    pass


def exe():
    j = Jasper(123)
    print(j)
    # setattr(j, "name", "small jasper")
    # print(j.name)


def equ():
    a = [1, 2]
    b = [1, 2]
    assert [1, 2] == [1, 2]
    print([1, 2] == a, b)
    a = None
    if a != None:
        print("!=")
    if not a:
        print("not a ")
    if a == None:
        print("==None")


class Singleton1:
    __instance = None

    def __new__(cls, *args, **kwargs):
        print(cls.__instance)


class Singleton2:
    __instance = None

    def __init__(self):
        if not self.__instance:
            pass


def ps():
    driver = webdriver.Chrome(service=Service(r"C:\Users\Uneven\Desktop\codes\python\knowledge\chromedriver.exe"))
    driver.get("https://www.shell.com")
    wait = WebDriverWait(driver, 10)
    x = wait.until(lambda x: x)
    print(x)
    driver.quit()


def formatMap():
    di = {"a": 1, "b": 2, 'c': {"gg": 123}}
    v = '{c}'.format_map(di)
    k = 'a'
    print(v)
    print(di[k])


# Press the green button in the gutter to run the script.


def mutireturn():
    for i in range(10):
        yield i


def suite_add():
    suite = unittest.TestSuite


def path_finder():
    pathls = []
    a1 = os.path.abspath("..")
    a2 = Path('.').absolute()
    pathls.append(a1)
    pathls.append(a2)
    print(pathls)


# def c():
#     @ddt.ddt
#     class Test(unittest.TestCase):
#         @ddt.data(*[{'Sheet1': [{'case_no': 1, 'case_name': '测试登录', 'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]},
#                                 {'case_no': 1, 'case_name': '测试登录', 'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]},
#                                 {'case_no': 1, 'case_name': '测试登录',
#                                  'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]}]},
#                     {'Sheet2': []}])
#         def test_ui(self, case1):
#             print(case1)
#
#     return Test


def str_join(char, *args):
    new_str = ''
    for arg in args:
        new_str = new_str + char + arg
    return new_str[1:]


def f_(__, *aa, **kw):
    print(__)
    __ = "aa"
    print(__)
    print(type(aa))
    print(type(kw))


def te_sele():
    driver = seleUtil.driver()
    driver.get("https://www.w3school.com.cn/tiy/t.asp?f=hdom_alert")
    ele = driver.find_element(By.XPATH, '//*[@id="iframeResult"]')
    print(ele.tag_name)
    driver.switch_to.frame(ele)
    inpoot = driver.find_element(By.XPATH, '/html/body/input')
    print(inpoot)
    inpoot.click()
    alert = WebDriverWait(driver, 10).until(expected_conditions.alert_is_present())
    print(alert)
    print(alert.text)
    alert.accept()
    driver.quit()


def que():
    a = []
    for i in range(5):
        a.append(i)
        print(a)
    for i in range(5):
        print(a)


class K:
    ui = "pp"


val: queue.Queue = queue.Queue()


def driver_start():
    for i in range(1, 3):
        driv = seleUtil.driver()
        driv.get("https://www.baidu.com")
        val.put(driv)


def driver_close():
    while not val.empty():
        i: webdriver.Chrome = val.get()
        i.service.stop()


def mysql():
    db = pymysql.Connection(host="47.106.168.208", port=3306, user="shawn", password="Nbch48mysql.", database="tsl")
    cur = db.cursor()
    cur.execute("select * from stu where name ='abort'")
    result = cur.fetchone()
    db.commit()
    print(result[1:-1])


def str_convert():
    print(type(str({"A": 1})))


dt = [{'case_no': 1, 'case_name': '测试登录', 'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]},
      {'case_no': 1, 'case_name': '测试登录', 'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]},
      {'case_no': 1, 'case_name': '测试登录', 'steps': [[1, '跳转网页', 'get'], [2, '输入', 'input']]}]


# class Test_1:
#     @pytest.mark.parametrize('a', dt)
#     def test_go(self,a):
#         print(f"\n{a}")


@ddt.ddt
class Test_2(unittest.TestCase):

    @ddt.data(*dt)
    def test_go(self, v):
        print(f"\n{v}")
def alert_t():

    try:
        dr = seleUtil.driver()
        wait = WebDriverWait(dr, 10)
        dr.get("https://www.w3school.com.cn/tiy/t.asp?f=hdom_alert")
        time.sleep(1)
        ele = dr.find_element(By.XPATH, '//*[@id="iframeResult"]')
        dr.switch_to.frame(ele)
        dr.find_element(By.XPATH,'//*/input').click()
        alert=dr.switch_to.alert
        # alert=dr.find_element(By.XPATH,"alert")
        # alert = wait.until(expected_conditions.alert_is_present())
        print(alert.text)
        # print(dr.find_element('alert').text)
        # alert.accept()
        dr.get_screenshot_as_png()
    finally:
        seleUtil.clear()
if __name__ == '__main__':
    # argv = sys.argv
    # argv.append("-v")
    # unittest.main(argv=argv, module='see')
    # pytest.main()
    pattern = r"\{\w*\}"
    result = re.match(pattern, '{msg}')
    print(result.)
    print('{msg}'[1:-1])
