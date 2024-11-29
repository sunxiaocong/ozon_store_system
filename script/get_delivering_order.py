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
def insert_b_order(store_name, table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()

    # 获取所有的订单
    query = "SELECT order_number,sku FROM b_order"
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()

    order_dict = dict()
    # 遍历结果
    for row in result:
        # 处理每一行数据
        order_dict[row[0] + "_" + row[1]] = 1
    for order in table_data["result"]["postings"]:
        order_number = order["posting_number"]
        order_time = order["in_process_at"].replace("T", " ").replace("Z", "")
        shipment_time = order["shipment_date"].replace("T", " ").replace("Z", "")

        for o in order["products"]:
            sku = get_sku_by_offer_id(o["offer_id"])

            if order_dict.get(order_number + "_" + sku, None) is None:
                count = o["quantity"]
                your_order_amount = float(o["price"]) * int(count)

                insert_sql = f"INSERT INTO `b_order` (`store_name`,`sku`, `order_amount`, `order_time`, `shipment_time`, `count`, `order_number`) VALUES ('{store_name}','{sku}', {your_order_amount}, '{order_time}', '{shipment_time}', {count}, '{order_number}')"
                try:
                    cursor.execute(insert_sql)
                except Exception as e:
                    logger.error(e)
                    pass
            else:
                logger.info("订单已存在" + order_number + sku)
    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


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
# {
#     "result": {
#         "postings": [],
#         "count": 0
#     }
# }
def get_awaiting_packaging(headers):
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
            "status": "delivering",
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


# 示例代码
if __name__ == '__main__':
    ozonIds = {
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
        "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
    }
    for ozon_name, ozon_auth in ozonIds.items():
        res = get_awaiting_packaging(ozon_auth)
        insert_b_order(ozon_name, res)
