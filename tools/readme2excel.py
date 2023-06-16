import datetime
import os
import pandas as pd
import re
from functools import reduce
from pathlib import Path


with open("README.md", 'r', encoding="utf-8") as f:
    contents = f.read()
contents[-10:]

def find_first(fun, it):
    for i, item in enumerate(it):
        if fun(item):
            return i
    return -1
def find_last(fun, it):
    return len(it)-1-find_first(fun, reversed(it))

paragraphs = contents.split("# ")
# paragraphs = list(filter(lambda x:"大学" in x or "学院" in, paragraphs))
first_uni = find_first(lambda x:"大学" in x or "学院" in x, paragraphs)
last_uni = find_last(lambda x:"大学" in x or "学院" in x, paragraphs)
paragraphs = paragraphs[first_uni:last_uni+1]

def item2dict(item):
    print(item)
    try:
        报名截止 = item[item.index("：")+1:item.index("】")]
        报名截止 = datetime.datetime.strptime(报名截止, "%Y.%m.%d")
    except:
        报名截止 = float("nan")
    try:
        院系名称 = item[item.index("[")+1:item.index("]")]
    except:
        院系名称 = ""
    try:    
        通知网址 = item[item.index("(")+1:item.index(")")]
    except:
        通知网址 = ""
    return dict(报名截止=报名截止,院系名称=院系名称, 通知网址=通知网址)


def paragraph2dicts(paragraph):
    # 学校名称 = line.split("\n\n")[0]
    lines = re.split("\n+", paragraph)
    # print(lines)
    学校名称 = lines[0]
    学校网址 = lines[1].split("> ")[1] if "> " in lines[1] else ""
    school_dict = dict(学校名称=学校名称, 学校网址=学校网址)
    
    
    criti = lambda x:"【报名截止" in x and "~~" not in x
    # criti = lambda x:"【报名截止" in x
    
    # first_item = find_first(criti, lines)
    # last_item = find_last(criti, lines)
    # items = lines[first_item:last_item+1]
    
    items = list(filter(criti, lines))
    
    return [{k:v for d in [item2dict(item), school_dict] for k,v in d.items()}
        for item in items
    ]
    
    # return dict(学校名称=学校名称).update(item2dict(itmes))
    
    
datas = list(reduce(lambda x,y:x+y, 
                    map(paragraph2dicts, paragraphs), []))


df = pd.DataFrame(datas)
df.head()
df.to_excel("数据汇总.xlsx", index=False)
