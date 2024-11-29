import logging
import sys
import time
from datetime import datetime, timedelta

import mysql.connector
import requests

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python_store',
        'USER': 'root',
        'PASSWORD': '123456jklJKL',
        'HOST': '114.132.98.135',
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}


# 建立数据库连接
# 更新数据库库存
def insert_b_seller_metrics(table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for data in table_data:
        # hits_view = data[0]
        # hits_tocart = data[1]
        # session_view_pdp = data[2]
        # conv_tocart = data[3]
        # returns = data[4]
        # delivered_units = data[5]
        # revenue = data[6]
        # ordered_units = data[7]
        # store_name = data[8]
        # date_str= data[9]
        # 执行更新数据的操作
        try:
            insert_sql = """INSERT INTO b_seller_metrics (hits_view, hits_tocart, session_view_pdp, conv_tocart, returns, delivered_units, revenue, ordered_units,store_name,day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            print(insert_sql)
            print(data)
            cursor.execute(insert_sql, data)
        except Exception as e:
            print(e)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


# 更新数据库库存
def get_b_seller_metrics(d):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    results = []  # 用于存储查询结果

    # 执行查询操作
    try:
        # SQL 查询语句
        select_sql = """SELECT * FROM b_seller_metrics WHERE store_name=%s AND day=%s"""
        print(select_sql)
        # 执行查询
        cursor.execute(select_sql, d)
        # 获取查询结果
        query_result = cursor.fetchall()  # 获取所有结果
        print(query_result)
        results.extend(query_result)  # 将结果添加到 results 列表中
    except Exception as e:
        print(f"Error occurred: {e}")
    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()
    return results


def get_time():
    import datetime
    # 获取当前时间
    now = datetime.datetime.utcnow()

    # 计算前30天的时间
    delta = datetime.timedelta(days=1)
    five_days_ago = now - delta
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%d")

    # 计算5天后的时间
    delta = datetime.timedelta(days=-1)
    five_days_later = now + delta
    five_days_later_str = five_days_later.strftime("%Y-%m-%d")
    return five_days_ago_str, five_days_later_str


def get_analytics_data(headers, cutoff_from="", cutoff_to=""):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v1/analytics/data'
    if cutoff_from == "" or cutoff_to == "":
        cutoff_from, cutoff_to = get_time()
    print(cutoff_from, cutoff_to)
    metrics = [
        "hits_view",
        "hits_tocart",
        "session_view_pdp",
        "conv_tocart",
        "returns",
        "delivered_units",
        "revenue",
        "ordered_units"
    ]

    data = {
        "date_from": cutoff_from,
        "date_to": cutoff_to,
        "metrics": metrics,
        "dimension": [
            "sku",
            "day"
        ],
        "filters": [],
        "sort": [
            {
                "key": "revenue",
                "order": "DESC"
            }
        ],
        "limit": 1000,
        "offset": 0
    }
    print(data)
    try:
        response = requests.post(url, headers=headers, json=data)
        products = response.json()
        print(products)
    except Exception as e:
        logging.info(str(e))
        return None
    return products


def get_date_list():
    start_date = datetime(2024, 9, 10)
    end_date = datetime(2024, 9, 10)

    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_list


if __name__ == '__main__':
    ozonIds = {
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        # "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        # "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
        "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
    }
    # now_date_list = get_date_list()
    args = sys.argv[1:]  # 忽略第一个参数（脚本名称）
    sep_store_name = ""
    print(args)
    if len(args) >= 1:
        print("args ", args)
        date_str = args[0]
        if len(args) >= 2:
            sep_store_name = args[1]
    else:
        date_str, _ = get_time()
        print("自动获取时间 :", date_str)

    # for date_str in now_date_list:
    for store_name, ozon_auth in ozonIds.items():
        if sep_store_name != "" and store_name != sep_store_name:
            print("skip store %s" % store_name)
            continue
        if len(get_b_seller_metrics((store_name, date_str))):
            print("数据存在")
            continue

        hits_view = 0  # 总展示次数
        hits_tocart = 0  # hits_tocart
        session_view_pdp = 0  # 所有会话。计算唯一身份访问者。
        conv_tocart = 0  # 购物车总转化率。
        returns = 0  # 退货
        delivered_units = 0
        revenue = 0  # 订购的金额，
        ordered_units = 0  # 订购的商品
        res = get_analytics_data(ozon_auth, date_str, date_str)

        for data in res['result']['data']:
            if len(data['metrics']) == 8:
                hits_view += data['metrics'][0]
                hits_tocart += data['metrics'][1]
                session_view_pdp += data['metrics'][2]
                conv_tocart += data['metrics'][3]
                returns += data['metrics'][4]
                delivered_units += data['metrics'][5]
                revenue += data['metrics'][6]
                ordered_units += data['metrics'][7]
            else:
                revenue += data['metrics'][0]
                ordered_units += data['metrics'][1]

        insert_b_seller_metrics(
            [(hits_view, hits_tocart, session_view_pdp, conv_tocart, returns, delivered_units,
              revenue, ordered_units, store_name, date_str)])

        if sep_store_name == "":
            time.sleep(600)
