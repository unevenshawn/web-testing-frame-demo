import json
import queue


def str_minus(a: str, b: str):
    if len(a) < len(b):
        temp = a
        a = b
        b = temp


def attr_values(ob: object):
    for attr in dir(ob):
        if not attr.startswith('__'):
            val = getattr(ob, attr)
            print(f"属性名称是{attr}，属性值为{val}")


def compare_if_same(list1: list, list2: list):
    flag = True
    for l in list1:
        if l not in list2:
            flag = False
    return flag


# 层序遍历
def dict_traverse(data: dict, func):
    que = queue.Queue()
    que.put(data)
    # for key in data.keys():
    #     que.put(key)
    while not que.empty():
        item = que.get()
        if hasattr(item, "keys"):
            for key, value in item.items():
                func(key, value)
                que.put(value)
        elif isinstance(item, list):
            for l in item:
                func(l)
                que.put(l)


def replace_json_str_if_int(fullstring: str, old, new, symbol="$"):
    temp_type = type(new)
    new_string = ""
    if temp_type == int or temp_type == float:
        # 保证{"key":"${content}"}这样的能够被替代
        new_string = fullstring.replace('"' + symbol + '{' + old + '}"', str(new))
        # 保证{"key":"token=${content}"}这样的能够被替代
        new_string = new_string.replace(symbol + "{" + old + "}", str(new))
    elif temp_type == list or temp_type == dict:
        new_string = fullstring.replace(symbol + "{" + old + "}", json.dumps(new))
    else:
        new_string = fullstring.replace(symbol + "{" + old + "}", new)
    return new_string


def string_join(symbol, ls: list = None, *args):
    rtn = ''

    if ls is None:
        ac_ls = args
    elif ls:
        if not isinstance(ls,list):ls=[ls]
        ac_ls = ls + list(args)
    for i in ac_ls:
        if not isinstance(i, str): i = str(i)
        rtn = rtn + symbol + i
    return rtn[len(symbol):]

if __name__ == '__main__':
    print(string_join("-", [1], 2, 3, 4))
