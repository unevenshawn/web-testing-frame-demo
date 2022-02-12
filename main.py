import os
import unittest
from datetime import datetime

import pytest
from HtmlTestRunner import HTMLTestRunner

import sys


def usewhichframe(name="pytest"):
    if name == "unittest":
        argv = sys.argv
        argv.append("-v")
        # argv.append("-b")

        unittest.main(module=None,
                      argv=argv,
                      # testLoader=MyTestLoader(),
                      testRunner=HTMLTestRunner()
                      )  # 加上module=None，才会让loader自动启用，并发现测试用例
    elif name == "pytest":
        pytest.main(['-vs'])
    else:
        raise Exception("no such frame")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    alluredir = f"./reports/report_{str(datetime.today().date())}"
    pytest.main()
    os.system(f"allure generate ./temps -o  {alluredir} --clean")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
