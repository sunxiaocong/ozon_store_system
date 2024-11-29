import logging

import mysql.connector
import requests

# 创建 logger 对象
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# 创建 FileHandler 对象
log_file = "d_order.log"
file_handler = logging.FileHandler(log_file)

# 设置日志级别和格式
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# 将 FileHandler 添加到 logger 中
logger.addHandler(file_handler)

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


def get_sku_by_offer_id(offer_id):
    sku = ""
    o_ids = offer_id.split("-")
    if len(o_ids) >= 2:
        sku = "O9880-" + o_ids[0] + "-" + o_ids[1]
    return sku


# 建立数据库连接
def get_b_order(s_name):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 获取所有的订单
    query = "SELECT order_number FROM b_order where status = 0 and store_name='%s'" % s_name
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    order_list = list()
    # 遍历结果
    for row in result:
        # 处理每一行数据
        order_list.append(row[0])
    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()
    return order_list


def get_time():
    import datetime
    # 获取当前时间
    now = datetime.datetime.utcnow()

    # 计算前5天的时间
    delta = datetime.timedelta(days=90)
    five_days_ago = now - delta
    five_days_ago_str = five_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # 计算5天后的时间
    delta = datetime.timedelta(days=0)
    five_days_later = now + delta
    five_days_later_str = five_days_later.strftime("%Y-%m-%dT%H:%M:%SZ")
    return five_days_ago_str, five_days_later_str


# 获取商品列表
# {'result': {'posting_number': '84348849-0012-4', 'order_id': 24570574017, 'order_number': '84348849-0012',
#             'status': 'delivering',
#             'delivery_method': {'id': 1020001302885000, 'name': 'Доставка Ozon самостоятельно, Москва',
#                                 'warehouse_id': 1020001302885000, 'warehouse': 'sdk1', 'tpl_provider_id': 24,
#                                 'tpl_provider': 'Доставка Ozon'}, 'tracking_number': '', 'tpl_integration_type': 'ozon',
#             'in_process_at': '2024-08-04T21:43:17Z', 'shipment_date': '2024-08-07T13:59:00Z',
#             'delivering_date': '2024-08-07T08:53:08Z', 'provider_status': '', 'delivery_price': '',
#             'cancellation': {'cancel_reason_id': 0, 'cancel_reason': '', 'cancellation_type': '',
#                              'cancelled_after_ship': False, 'affect_cancellation_rating': False,
#                              'cancellation_initiator': ''}, 'customer': None, 'addressee': None, 'products': [
#         {'price': '4422.0000', 'offer_id': 'DD-000019',
#          'name': 'Простая современная гостиная, обеденный стол в спальне, круглая люстра', 'sku': 1409453647,
#          'quantity': 1, 'mandatory_mark': [],
#          'dimensions': {'height': '625.00', 'length': '625.00', 'weight': '1900', 'width': '65.00'},
#          'currency_code': 'RUB'}], 'barcodes': None, 'analytics_data': None, 'financial_data': None,
#             'additional_data': [], 'is_express': False,
#             'requirements': {'products_requiring_gtd': [], 'products_requiring_country': [],
#                              'products_requiring_mandatory_mark': [], 'products_requiring_rnpt': [],
#                              'products_requiring_jw_uin': []}, 'product_exemplars': None, 'courier': None,
#             'parent_posting_number': '', 'related_postings': None, 'available_actions': [], 'multi_box_qty': 1,
#             'is_multibox': False, 'substatus': 'posting_in_pickup_point',
#             'previous_substatus': 'posting_on_way_to_city',
#             'prr_option': {'code': '', 'price': '', 'currency_code': 'RUB', 'floor': ''}}}


def get_order_info(headers, pn):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/get'
    data = {
        "posting_number": pn,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "product_exemplars": False,
            "translit": False
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        products = response.json()
    except Exception as e:
        logging.info(str(e))
        return None
    return products


def update_order_status(us_list):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for values in us_list:
        # 执行更新数据的操作
        update_query = "UPDATE b_order SET status = {status} WHERE order_number='{order_number}'".format(
            status=values[0],
            order_number=values[1])
        cursor.execute(update_query)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


# 示例代码
if __name__ == '__main__':
    import time

    status_dict = {
        "delivering": 0,
        "delivered": 1,
        "cancelled": 2
    }

    ozonIds = {
        "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
    }
    for store_name, ozon_auth in ozonIds.items():
        res = get_b_order(store_name)
        update_status_list = []
        for pn in res:
            import random

            random_number = random.randint(0, 15)
            time.sleep(random_number)

            of = get_order_info(ozon_auth, pn)
            s = of.get("result", {}).get("status", "delivering")
            print(pn, s)
            if s != "delivering":
                if status_dict.get(s, -1) != -1:
                    update_status_list.append((status_dict.get(s), pn))
                else:
                    print("[error status] ")
        if len(update_status_list) > 0:
            print(update_status_list)
            update_order_status(update_status_list)
