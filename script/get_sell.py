import logging
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
def insert_ozon_cost(table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for data in table_data:
        store_name = data[0]
        cost_type = data[1]
        day = data[2]
        cost = data[3]
        # 执行更新数据的操作
        insert_sql = f"INSERT INTO ozon_cost (store_name, cost_type, day, cost) VALUES ('{store_name}', '{cost_type}', '{day}', {cost});"
        print(insert_sql)
        cursor.execute(insert_sql)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


def get_time():
    import datetime
    # 获取当前时间
    now = datetime.datetime.utcnow()

    # 计算前30天的时间
    delta = datetime.timedelta(days=2)
    five_days_ago = now - delta
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%d")

    # 计算5天后的时间
    delta = datetime.timedelta(days=-2)
    five_days_later = now + delta
    five_days_later_str = five_days_later.strftime("%Y-%m-%d")
    return five_days_ago_str, five_days_later_str


def get_analytics_data(headers, cutoff_from="", cutoff_to=""):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v3/finance/transaction/list'
    if cutoff_from == "" or cutoff_to == "":
        cutoff_from, cutoff_to = get_time()
    print(cutoff_from, cutoff_to)
    data = {
        "filter": {
            "date": {
                "from": f"{cutoff_from}T00:00:00.000Z",
                "to": f"{cutoff_to}T23:59:59.000Z"
            },
            "operation_type": [],
            "posting_number": "",
            "transaction_type": "orders"
        },
        "page": 1,
        "page_size": 1000
    }
    print(data)
    try:
        response = requests.post(url, headers=headers, json=data)
        products = response.json()
    except Exception as e:
        logging.info(str(e))
        return None
    return products


def get_date_list():
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 9, 3)

    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_list


if __name__ == '__main__':
    ozonIds = {
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        # "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        # "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        # "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        # "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
        # "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
    }

    _type = {
        "orders": "0",  # 模版费用
    }

    # now_date_list = get_date_list()
    # for date_str in now_date_list:
    date_str, _ = get_time()
    amount = 0
    for store_name, ozon_auth in ozonIds.items():
        res = get_analytics_data(ozon_auth, date_str, date_str)
        for info in res["result"]["operations"]:
            amount += info["accruals_for_sale"]
    print(amount)
