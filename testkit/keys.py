import re
import time

import allure
import pymysql

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from api import seleUtil

from api.logUtil import LoggerUtil

logger = LoggerUtil.get_logger(__name__)
error_log = logger.error
info_log = logger.info
debug_log = logger.debug


class KeyWord:
    # _default_driver = seleUtil.driver()
    _ele: WebElement = ''
    _vars = {}
    # new_drivers = queue.Queue()
    temp_store = None
    new_drivers = []
    self_create_driver_init = False
    _db = None

    def all_keys_and_methods(self):
        all["keys"] = self.all_keys()
        all["assert_methods"] = Validator.all_asserts()

    def all_keys(self):
        kls = []
        for atrs in dir(self):
            if atrs.startswith("key_"):
                kls.append(atrs[4:])
        return kls

    def __init__(self, driver: WebDriver):
        self.driver = driver
        if not driver:
            self.driver = seleUtil.driver()
            # self.self_create_driver_init = True
        self._wait = WebDriverWait(self.driver, 2)

    def __del__(self):
        if self._db:
            self._db.close()
        # print("这个del方法真的执行了吗？？？")

    def _find_ele(self, xpath: str) -> WebElement:
        def f(_):
            try:
                ele = self.driver.find_element(By.XPATH, xpath)
            except Exception as e:
                raise Exception(e)
            return ele

        return self._wait.until(f, f"未能定位到元素{xpath}")

    def invoke_by_key(self, key, *args):
        debug_log(key)
        # debug_log(self.all_keys())
        if key not in self.all_keys():
            raise Exception("no such method, 不存在该关键字及方法")
        fullKey = 'key_' + key.lower()
        method = getattr(self, fullKey)
        method(*args)

    def key_get(self, url):
        self.driver.get(url)

    def key_find(self, xpath: str):
        self._ele = self._find_ele(By.XPATH, xpath)

    def key_click(self, xpath, force=False):
        ele: WebElement = self._find_ele(xpath)
        # if not ele.is_displayed():
        #     ele.send_keys(Keys.ENTER)
        # el
        if not force:
            ele.click()
        else:

            self.driver.execute_script("arguments[0].click()", ele)

    def key_input(self, xpath, content):
        '''
        :param xpath: elput => input with element，即xpath的定位，单次使用参数对应的元素
        :param content: input的具体内容
        :return:
        '''
        ele = self._find_ele(xpath)
        ele.send_keys(content)

    def key_quit(self):
        if self.driver:
            self.driver.quit()

    def close(self):
        if self.driver:
            self.driver.quit()

    def key_wait(self, timespan):
        if not isinstance(timespan, int) and not isinstance(timespan, float):
            raise ArithmeticError("等待时间须为整数或小数")
        if timespan < 0:
            raise ArithmeticError("等待时间不能小于0")
        time.sleep(timespan)

    def key_sleep(self, timespan):
        if not isinstance(timespan, int) and not isinstance(timespan, float):
            raise ArithmeticError("等待时间须为整数或小数")
        if timespan < 0:
            raise ArithmeticError("等待时间不能小于0")
        time.sleep(timespan)

    def _process_brace_value(self, if_brace_value):

        pattern = r"\{\w*\}"
        result = re.match(pattern, if_brace_value)
        if result:
            # debug_log(result)
            return self._vars[result.group(0)[1:-1]]
        else:
            return if_brace_value

    def key_assert(self, expect, method, actual):
        if not isinstance(expect, str):
            expect = str(expect)
        if not isinstance(actual, str):
            actual = str(actual)
        expect = self._process_brace_value(expect)
        actual = self._process_brace_value(actual)

        validator = Validator(expect, method, actual)
        validator.validate()

    def key_save_text(self, xpath, var_name):

        if xpath.lower() == "alert":
            alert = self._wait.until(expected_conditions.alert_is_present(), "key_save_text方法中alert弹窗未能定位到")
            # alert=self._find_ele('alert')
            text = alert.text
            alert.accept()
        else:
            text = self._find_ele(xpath).text
        self._vars[var_name] = text
        # debug_log(f'{self._vars[var_name]} = {text}')

    def key_alert(self):
        alert = self._wait.until(expected_conditions.alert_is_present(), "key_alert方法中alert弹窗未能定位到")
        alert.accept()

    def key_frame(self, xpath):
        ele = self._find_ele(xpath)
        debug_log(ele.tag_name)
        assert ele.tag_name == "iframe"
        self.driver.switch_to.frame(ele)

    def key_session(self):
        # self.new_drivers.put(seleUtil.driver())
        debug_log(f'原有的{self.driver.session_id}')
        self.new_drivers.append(self.driver)
        self.driver = seleUtil.driver()
        debug_log(f'新的{self.driver.session_id}')

    def key_quit_session(self):
        try:
            self.driver.quit()
            # if len(self.new_drivers)>0:
            self.driver = self.new_drivers.pop()
            debug_log(f'原有的{self.driver.session_id}')
        except Exception as e:
            error_log("之前新建浏览器未能正确关闭")
            raise Exception(e)

    def all_driver(self):
        self.new_drivers.append(self.driver)
        return self.new_drivers

    def key_mysql(self, host, port, username, password, database):
        if type(port) == str: port = int(port)
        self._db = pymysql.Connection(host=host, port=port, user=username, password=password, database=database)

    def key_screenshot(self, name):
        # try:
        #     self.driver.find_element(By.XPATH, "alert")
        # except Exception as e:
        #     return
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name,
            allure.attachment_type.PNG
        )

    def key_save_sql(self, var_name, sql):

        assert self._db is not None
        with self._db.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
        self._db.commit()
        self._vars[var_name] = result


class Validator:

    @classmethod
    def all_asserts(cls):
        rtns = []
        for at in dir(cls):
            if at.startswith("assert_"):
                rtns.append(at[7:])
        return rtns

    def __init__(self, expect, method, actual):
        self.expect = expect
        self.assert_method = self.concat_assert(method)
        self.actual = actual

    def validate(self):
        assert_method = getattr(self, self.assert_method)
        assert_method(self.expect, self.actual)

    def concat_assert(self, method):
        return "assert_" + method.lower()

    def assert_in(self, expect, actual):
        '''
        :param expect: 预期结果
        :param actual: 实际返回结果
        :return:
        实际结果包含预期内容
        '''
        assert expect in actual

    def assert_equal(self, expect, actual):
        '''
        :param expect: 预期结果
        :param actual: 实际返回结果
        :return:
        预期结果等于实际结果
        '''
        assert expect == actual

    def assert_not_equal(self, expect, actual):
        assert expect == actual

    def assert_contain(self, expect, actual):
        '''
        :param expect: 预期结果
        :param actual: 实际返回结果
        :return:
        预期内容包含实际返回结果的内容
        '''
        assert actual in expect


if __name__ == '__main__':
    pass

    # try:
    #     key.invoke_by_key("get", "https://baidu.com")
    #     key.invoke_by_key("wait", -1)
    # except Exception as e:
    #     print(e)
    # key.invoke_by_key("quit")
