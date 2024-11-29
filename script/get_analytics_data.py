import logging

import requests


def get_time():
    import datetime
    # 获取当前时间
    now = datetime.datetime.utcnow()

    # 计算前30天的时间
    delta = datetime.timedelta(days=6)
    five_days_ago = now - delta
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%d")

    # 计算5天后的时间
    delta = datetime.timedelta(days=-5)
    five_days_later = now + delta
    five_days_later_str = five_days_later.strftime("%Y-%m-%d")
    return five_days_ago_str, five_days_later_str


def get_analytics_data(headers):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v1/analytics/data'
    cutoff_from, cutoff_to = get_time()
    print(cutoff_from, cutoff_to)
    data = {
        "date_from": cutoff_from,
        "date_to": cutoff_to,
        "metrics": [
            "hits_view_search"
        ],
        "dimension": [
            "spu",
            "day"
        ],
        "filters": [],
        "sort": [
            {
                "key": "hits_view_search",
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
        res = get_analytics_data(ozon_auth)
        print(res)
