import logging

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


def get_fbo_stocks(headers):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v3/product/info/stocks'

    data = {
        "filter": {
            "visibility": "ALL"
        },
        "last_id": "",
        "limit": 500
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


def get_sku_by_offer_id(offer_id):
    sku = ""
    o_ids = offer_id.split("-")
    if len(o_ids) >= 2:
        sku = "O9880-" + o_ids[0] + "-" + o_ids[1]
    return sku


def get_fbo_stock_from_stocks(item_stocks):
    for s in item_stocks:
        if s.get("type") == "fbo":
            return s.get("present", 0)
    return 0


# 更新数据库库存
def update_b_thing_fbo_property(sku_stock_dict):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for sku, fbo_property in sku_stock_dict.items():
        # 执行更新数据的操作
        update_query = "UPDATE b_thing SET fbo_property = %s WHERE sku=%s"
        values = (fbo_property, sku)  # 替换为你要更新的值
        cursor.execute(update_query, values)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    sku_stock = {}
    ozonIds = {
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
    }
    # for date_str in now_date_list:
    for store_name, ozon_auth in ozonIds.items():
        res = get_fbo_stocks(ozon_auth)
        for item in res.get("result", {}).get("items", []):
            oid = item.get("offer_id", "")
            if oid:
                sku_tmp = get_sku_by_offer_id(oid)
                sku_stock_num = sku_stock.get(sku_tmp, 0) + get_fbo_stock_from_stocks(item.get("stocks"))
                if sku_stock_num != 0:
                    sku_stock[sku_tmp] = sku_stock_num
    update_b_thing_fbo_property(sku_stock)
    print(sku_stock)
