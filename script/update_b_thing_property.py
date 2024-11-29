import hashlib
from datetime import datetime

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
def update_b_thing_property(table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for data in table_data:
        sku = data.get("sku", "")
        available_qty = data.get("availableQty", 0)
        # 执行更新数据的操作
        update_query = "UPDATE b_thing SET property = %s WHERE sku=%s"
        values = (available_qty, sku)  # 替换为你要更新的值
        cursor.execute(update_query, values)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


def get_search_inventory():
    url = 'http://www.xxl-express.net/wms-main/api'
    api_key = 'A1C67A99AC0FBF5C0FA94ACC73F56D10'  # 替换为你的实际 API 密钥
    # 获取当前时间
    current_time = datetime.now()

    # 将当前时间按照指定格式进行格式化
    req_time = current_time.strftime('%Y-%m-%d %H:%M:%S')  # 示例请求时间
    method = 'searchInventory'  # 示例请求方法
    partner_code = 'O9880'  # 示例合作伙伴代码
    # req_body = {
    #     'warehouseCode': 'KIT05'
    # }  # 示例请求体

    req_body = '{"warehouseCode":"KIT05"}'

    # 构建签名字符串
    signature_string = f"{req_time}&{method}&{partner_code}&{api_key}&{req_body}"
    print(signature_string)

    # 计算签名
    signature = hashlib.md5(signature_string.encode()).hexdigest().upper()

    print(signature)

    # 构建请求参数
    payload = {
        'reqTime': req_time,
        'method': method,
        'partnerCode': partner_code,
        'reqBody': req_body,
        'sign': signature
    }

    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    # 发送 HTTP POST 请求
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

    # 打印响应内容
    return response.json().get("data", [])


if __name__ == '__main__':
    td = get_search_inventory()
    update_b_thing_property(td)
