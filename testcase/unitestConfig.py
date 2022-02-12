import  unittest

class MyTestLoader(unittest.TestLoader):
    testMethodPrefix = "test"
    sortTestMethodsUsing = None #按照编写顺序
