# -*- coding: utf-8 -*-
import functools

from aip import AipNlp
from sanic.log import logger
import re

import listutils

_BAIDU_ACCOUNTS = [
    {'app_id': '15428255', 'api_key':	't2OOUBpi0rREk2fXirNYp4G7', 'secret_key': 'gmvQVV0gllz2ICkWQUpMkzEsUumOGXax'},
    {'app_id': '15428373', 'api_key':	'tt0AepbE391GfGw4bzZnLt3i', 'secret_key': 'vXRxjuB0vCZYvuDmnlRPxq7Z93yLrzAp'},
    {'app_id': '15457807', 'api_key':	'9poNFltyjRNXULRYx7v50qD6', 'secret_key': '3Lexv9vkXkMgGo9SK16sE5kQdxfAOMzF'},
    {'app_id': '15457866', 'api_key':	'QvBt8Ghv82phGXO8gr6COtuE', 'secret_key': 'mDifAvCtTG9YyDjoYyYyVwtGXTE2Wl3g'},
    {'app_id': '15457932', 'api_key':	'5FUUSa9PSpSeGWfduFuCr908', 'secret_key': 'sPhwSynOoeAah1zZP7YI9GC9rqxhRetT'},
    {'app_id': '15458058', 'api_key':	'At1TkFUfeOkt4bm9BuKMeQNz', 'secret_key': 'gsurUGRixcfgksNNmncjdkVkWb3e5RBa'},
    {'app_id': '15458141', 'api_key':	'G108AmHG1EZrQOb3IGiPHMF3', 'secret_key': 'WFnQHkqndb3UlDLheHSSCq3lgjAsTd8s'},
    {'app_id': '15458224', 'api_key':	'DGj4ApzN5ENwxQg53ExIUjaH', 'secret_key': 'LGxSxrPjBNtSYdqOInEBzNjhWjw4P3Wz'},
    {'app_id': '15458285', 'api_key':	'5DDoGQlZOng6pFlGffMKQAbH', 'secret_key': 'hczWHLdiNRXzTe3ak3cyEr6Dwd4B31CP'},
    {'app_id': '15458333', 'api_key':	'yTFh9kdS8Vl8DPVTmYfgGGQi', 'secret_key': '0YYjcFm9UhwuPM4O9SNdKKPGm7WwN14Q'},
    {'app_id': '15458414', 'api_key':	'hw2kPI2pCNAZePumGZYyQzzI', 'secret_key': '2FfIfsk7X7AH9WEKvThbmc2PhlhkXh1R'},
    {'app_id': '15458460', 'api_key':	'j20jM8vAVne3vdOlKVGGo5q2', 'secret_key': 'GGID8wvKDlkLdj0KaHqh1KTn0y6kK70z'},
    {'app_id': '15458500', 'api_key':	'UDyyKMT0E2NTuII5dLD3CLn5', 'secret_key': 'MlywXXfkNSA6LOrk4ffqdplUGsOeVCB0'},
    {'app_id': '15458536', 'api_key':	'bDIPCmRtxID3be9EYz92hSo6', 'secret_key': 'KU0elddpDeiTG87oLRgx1fuFGzNzktXg'},
    {'app_id': '15458562', 'api_key':	'FLO1sjwme5ZrFfhnzdRi5RBK', 'secret_key': 'qwZYkxZDRIIb4DTxzKFRuqDPFZuU3WLK'},
    {'app_id': '15458610', 'api_key':	'PFXz6Nw0H9W2oGOfqFtmSdX6', 'secret_key': 'irdL4dgfw4w1ymU2kPnw3VVMv9pukm6q'},
    {'app_id': '15458626', 'api_key':	'6lYWnuEPDMABWrlb2AIbzwG4', 'secret_key': 'kvkBC6YvpgtS6evBVH4xT14WRGyQIyAy'},
    {'app_id': '15458693', 'api_key':	'Te8obDQ1WOntx8yUT5iUWIHj', 'secret_key': 'gGhCETndRplSovfvxaEL3sY5F8irlW2R'},
    {'app_id': '15458720', 'api_key':	'8KaaBEbZwQLj7dLCGwDzgdWu', 'secret_key': 'IRfijMcwH6MHqsw5f5bkVHUjqTUXCGSq'},
    {'app_id': '15459015', 'api_key':	'hBQFFXCyC9pSREfbBt8rGF1s', 'secret_key': 'y87DrDMpg5tPHDObWtI3S1FIqfi2jeHQ'},
]
BAIDU_ACCOUNTS = listutils.cycle(_BAIDU_ACCOUNTS)

ORG_QUALIFIED = [
    "宣布.*盈利",
    "宣布.*裁员",
    "宣布.*计划",
    "进入",
    "加盟",
    "加入",
    "当上",
    "先后任",
    "担任",
    "晋升",
    "改任",
    "调往",
    "启动",
    "位居",
    "月任",
    "升任",
    "任职",
    "回归",
    "出任",
    "当学徒",
    "接掌",
    "接替",
    "执导",
    "率领",
    "聘为",
    "聘任",
    "现任",
    "聘请",
    "投身",
    "供职",
    "被任命",
    "就职于",
    "离开",
    "辞去",
    "辞职",
    "离职",
    "创办",
    "ALL IN",
    "创立",
    "建立",
    "成立",
    "创建",
    "自立门户",
    "共同成立",
    "开始.*创业",
    "二次创业",
    "共同创建",
    "独立创业",
    "连续创业",
    "推出",
    "负责",
    "年任",
    "曾在.*工作",
    "创始",
    "历任",
    "创立",
    "曾任",
    "大学.*主任",
    "大学.*教授",
    "CEO",
    "董事长",
    "联合.*创建",
    "联合.*创办",
    "拥有.*经验",
    "曾在.*担任",
    "曾在.*担当",
    "曾在.*经验",
    "工作",
    "管理",
    "合伙人",
    "创始人",
    "员工",
    "从业",
    "从事",
    "创立",
    "副总裁",
    "带领",
    "总裁",
    "主管",
    "首席",
    "总监",
    "董事",
    "专家",
    "leader",
    "总经理",
    "工程师",
    "产品经理",
    "产品设计师",
    "经理",
    "进入",
    "CEO",
    "CTO",
    "COO",
    "CFO",
    "CMO",
    "CSO",
    "科学家",
    "一职",
    "法人",
    "取得.*学位",
    "就读",
    "毕业",
    "考上",
    "获.*博士",
    "获.*硕士",
    "获.*学位",
    "保送",
    "免试",
    "攻读",
    "获得.*学历",
    "获得.*学位",
    "休学",
    "大学.*硕士",
    "大学.*博士",
    "大学.*MBA",
    "校友",
    "大学.*本科",
    "拥有.*学位",
    "拥有.*硕士",
    "拥有.*博士",
    "拥有.*学士",
    "拥有.*本科",
    "大学.*EMBA",
    "学院.*EMBA",
    "学院.*MBA",
    "考入",
    "深造",
    "本科",
    "学士",
    "硕士",
    "博士",
    "硕博",
    "求学",
    "学位",
    "大学.*专业",
    "学院.*专业",
    "加盟",
]

any_backspaces = re.compile("\b+")


def strip_to_none(text: str):
    if text is None:
        return None
    text = text.strip()
    text = re.sub(any_backspaces, '', text)
    if len(text) == 0:
        return None
    if text == 'None':
        return None
    return text


def get_client():
    account = next(BAIDU_ACCOUNTS)
    app_id = account.get('app_id')
    api_key = account.get('api_key')
    secret_key = account.get('secret_key')
    return AipNlp(app_id, api_key, secret_key)


def convert_encoding(f):
    @functools.wraps(f)
    def wrapper(sentence, *args, **kwargs):
        text = strip_to_none(sentence)
        if text is None or len(text) > 700:
            return list()
        text = text.encode('gbk', 'ignore').decode('gbk')
        times = 2
        while times > 0:
            try:
                result = f(text, *args)
                times = 0
                return result
            except Exception as err:
                logger.debug(f"Failed with text: {text}, due to {err}")
                times -= 1

    return wrapper


@convert_encoding
def cut(text: str) -> list:
    result = get_client().lexer(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        logger.error(msg)
        # notifier.notify(msg)
        return []
    items = result.get('items')
    if items is None:
        return []
    return [item.get('item') for item in items]


@convert_encoding
def lexer(text: str, debug=False) -> list:
    text = strip_to_none(text)
    if text is None:
        return []
    result = get_client().lexerCustom(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        logger.error(msg)
        return []
    items = result.get('items')
    if items is None:
        return []
    return items


@convert_encoding
def original_lexer(text: str, debug: object = False) -> list:
    text = strip_to_none(text)
    if text is None:
        return []
    result = get_client().lexer(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        logger.error(msg)
        return []
    items = result.get('items')
    if items is None:
        return []
    return items



