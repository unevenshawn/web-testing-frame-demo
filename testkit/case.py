import unittest
from pathlib import Path

import allure
import ddt
from api import excelUtil, yamlUtil, seleUtil, funcUtil
from testkit import keys

from api.seleUtil import DriverManager

from api.logUtil import LoggerUtil

logger = LoggerUtil.get_logger(__name__)
error_log = logger.error
info_log = logger.info
debug_log = logger.debug


def entry_dir():
    testsuites = unpack(yamlUtil.read_conf_yml("dir", 'ui_entry'))
    return testsuites


class Runner:
    def __init__(self, case):
        self.case = case
        # "将测试用例名称拿出来，赋值给Runner中的__name__属性，再传入ddt中，可以改变allure中用例的名称"
        self.__name__ = case["case_name"]  # 对象的name属性会成为测试用例名的一部分


# 为了改变测试用例名的方法
def convert_2_Runner(caselist):
    newls = []
    for case in caselist:
        runner = Runner(case)
        newls.append(runner)
    return newls


def create_test(test_suite):
    @allure.suite(funcUtil.string_join("-", test_suite[0]['xl_name']))
    @ddt.ddt
    class Test(unittest.TestCase):

        @classmethod
        def setUpClass(cls) -> None:
            pass
            cls.driver = seleUtil.driver()

        @classmethod
        def tearDownClass(cls) -> None:
            DriverManager.clear()
            # del cls.k
            # info_log(cls.k)

        @ddt.data(*convert_2_Runner(test_suite))
        def test_case(self, runner):
            try:
                case = runner.case
                debug_log(f"\ntest_case方法所传入参数：{case}")
                k: keys.KeyWord = keys.KeyWord(driver=self.driver)
                # 如果会定位alert，那么就是要在alert前一步
                als = rule_out_alert(case['steps'])
                debug_log(als)
                for i in range(len(case['steps'])):
                    step = case['steps'][i]
                    @allure.step(step[1])
                    def foo(关键字=step[2],参数=step[3:]):
                        k.invoke_by_key(step[2], *step[3:])

                        if step[2] not in ['screenshot', 'mysql', 'quit', 'quit_session', 'save_sql', 'alert',
                                           'session',
                                           'sleep', 'wait'] and i + 1 not in als:
                            k.invoke_by_key('screenshot',
                                            funcUtil.string_join("-", case['xl_name'], case['sheetname'], step[0:2]))

                    foo()
            except Exception as e:
                error_log(e)
                raise Exception(e)

    return Test


def rule_out_alert(case_steps):
    string = str(case_steps)
    rtn = []
    if "alert" in string:
        no = 0
        for step in case_steps:
            if 'alert' in str(step) and no - 1 > 0:
                rtn.append(no - 1)
            no += 1
    return rtn


# todo  一个excel中的sheet对应一个Test类，每个Test类调用一次create_test方法，返回一个Test实例，
#  一个sheet中的case对应一条test_方法,一个test_case方法中应该对应多个关键字操作
#  todo 需要进行重新解包，将{"casename":"casedata"}作为kv，传入Test.test中去，在test方法中进行分解，这样才能保证能够在测试报告中形成一个case
def unpack(directory):
    wbs_gen = excelUtil.test_suite_by_excel(directory)
    test_fullname = ''
    for xlsx in wbs_gen:
        xln = fkey(xlsx)
        for workbookname, workbook in xlsx.items():
            wkbn = fkey(workbook)
            for sheetname, sheet in workbook.items():
                debug_log(f'{workbookname}-{sheetname}对应着,{sheet}')

                # rtn = {}
                #
                # for caseorder, cases in sheet.items():
                #     cn = cases['case_name']
                #     steps = cases['steps']
                #     for step in steps:
                #         test_fullname = str_join('-', xln, wkbn, cn, str(step[0]))
                #         debug_log(test_fullname)
                #         rtn[test_fullname] = [cn, step[0]] + step[1:]
                # "对应着的是每一个测试用例包装成一个类方法"

                yield list(sheet.values())


def str_join(char, *args):
    new_str = ''
    for arg in args:
        new_str = new_str + char + arg
    return new_str[1:]


def fkey(d: dict):
    return list(d.keys())[0]


class PysonExcel:

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.py_dir = self.base_dir / "test_ddt.py"

    def py_file(self):
        content = ''

        code = '''
from testkit.case import create_test, str_join, entry_dir

from api.logUtil import LoggerUtil
logger = LoggerUtil.get_logger(__name__)
error_log = logger.error
info_log = logger.info
debug_log = logger.debug

testsuites = entry_dir()
for suite in testsuites:

    if not suite.values():
        continue
    modulename = str_join("-", *list(suite.keys())[1].split("-")[0:2])
    debug_log(list(suite.keys()))
    globals()[f'{modulename}'] = create_test(suite)
    debug_log(f'modulename是{modulename}')
'''
        self.py_dir.write_text(content, encoding='utf-8')

    def py_unlink(self):
        self.py_dir.unlink(True)


def test_som():
    print("--")


if __name__ == '__main__':
    drt = r'C:\Users\Uneven\Desktop\codes\python\seleniumWeb\excel'
    gee = excelUtil.test_suite_by_excel(r'/excel')
    for ge in gee:
        print(ge)
    ds = unpack(drt)
    for i in ds:
        print(i)
