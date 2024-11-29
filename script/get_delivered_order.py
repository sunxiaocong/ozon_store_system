import logging

import requests


def get_time():
    import datetime
    # 获取当前时间
    now = datetime.datetime.utcnow()

    # 计算前5天的时间
    delta = datetime.timedelta(days=30)
    five_days_ago = now - delta
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # 计算5天后的时间
    delta = datetime.timedelta(days=0)
    five_days_later = now + delta
    five_days_later_str = five_days_later.strftime("%Y-%m-%dT%H:%M:%SZ")
    return five_days_ago_str, five_days_later_str


def get_delivered_packaging(headers):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list'
    cutoff_from, cutoff_to = get_time()
    data = {
        "dir": "ASC",
        "filter": {
            "cutoff_from": cutoff_from,
            "cutoff_to": cutoff_to,
            "delivery_method_id": [],
            "provider_id": [],
            "status": "delivered",
            "warehouse_id": []
        },
        "limit": 999,
        "offset": 0,
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "translit": True
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        products = response.json()
    except Exception as e:
        logging.info(str(e))
        return None
    return products


if __name__ == '__main__':
    ozonIds = {
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        # "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        # "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        # "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        # "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
        # "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
    }
    for ozon_name, ozon_auth in ozonIds.items():
        res = get_delivered_packaging(ozon_auth)
        print(res)
