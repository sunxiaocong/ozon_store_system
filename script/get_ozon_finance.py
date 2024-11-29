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


# 建立数据库连接
# 更新数据库库存
def insert_profit_statement(table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for data in table_data:
        # 执行更新数据的操作
        try:
            insert_sql = """INSERT INTO profit_statement (
                            store_name,
                            period,
                            commission_amount,
                            item_delivery_and_return_amount,
                            orders_amount,
                            returns_amount,
                            services_amount,
                            return_commission,
                            cost,
                            profit
                        ) VALUES (
                            %s,  -- store_name
                            %s,  -- period
                            %s,  -- commission_amount
                            %s,   -- item_delivery_and_return_amount
                            %s, -- orders_amount
                            %s,  -- returns_amount
                            %s,   -- services_amount
                            %s,  -- return_commission
                            %s,  -- cost
                            %s   -- profit
                        );"""
            print(insert_sql, data)
            cursor.execute(insert_sql, data)
        except Exception as e:
            print(e)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


def get_ozon_finance(headers):
    # 将时间格式化为字符串格式
    url = 'https://api-seller.ozon.ru/v1/finance/cash-flow-statement/list'
    data = {
        "date": {
            "from": "2024-09-30T00:00:00.000Z",
            "to": "2024-11-30T00:00:00.000Z"
        },
        "with_details": False,
        "page": 1,
        "page_size": 100
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        products = response.json()
        print(products)
    except Exception as e:
        logging.info(str(e))
        return None
    return products


# 示例代码
if __name__ == '__main__':
    ozonIds = {
        "003": {'Client-Id': '1659870', 'Api-Key': '5467d150-d18f-48fe-9604-32df39b7aeaa'},
        "006": {'Client-Id': '1740421', 'Api-Key': '7c3025e1-2653-4626-87fd-d312d7856280'},
        "001": {'Client-Id': '1659824', 'Api-Key': '10d6f5e8-819f-49bd-945b-c999ed5f7015'},
        "002": {'Client-Id': '1652544', 'Api-Key': 'ea51ff38-d3e3-4973-8f01-c4a2ab923187'},
        # "004": {'Client-Id': '1659812', 'Api-Key': 'bc0eea02-94ca-47a9-8083-8c489b456e69'},
        # "005": {'Client-Id': '1740428', 'Api-Key': 'e304eb6a-15ba-4d2b-94e7-b40c774adea7'},
    }
    table_infos = []
    for store_name, ozon_auth in ozonIds.items():
        all_profit = 0
        f_ps = get_ozon_finance(ozon_auth)
        for f_p in f_ps.get("result", {}).get("cash_flows", []):
            begin = f_p.get("period").get("begin")
            end = f_p.get("period").get("end")
            period = begin[0:10] + "至" + end[0:10]
            commission_amount = f_p.get("commission_amount")  # 佣金
            item_delivery_and_return_amount = f_p.get("item_delivery_and_return_amount")  # 运输费
            orders_amount = f_p.get("orders_amount")  # 签收
            returns_amount = f_p.get("returns_amount")  # 退货
            services_amount = f_p.get("services_amount")  # 服务费
            return_commission = -(orders_amount * 0.12)  # 提现手续费
            cost = -(orders_amount * 0.30)  # 成本
            profit = orders_amount * 0.58 + item_delivery_and_return_amount + commission_amount + services_amount + returns_amount

            # 计算比例
            commission_amount_rate = round((commission_amount / orders_amount) * 100, 2)
            item_delivery_and_return_amount_rate = round((item_delivery_and_return_amount / orders_amount) * 100, 2)
            returns_amount_rate = round((returns_amount / orders_amount) * 100, 2)
            services_amount_rate = round((services_amount / orders_amount) * 100, 2)
            profit_rate = round((profit / orders_amount) * 100, 2)

            all_profit += profit
            table_infos.append((store_name,
                                period,
                                str(int(commission_amount)) + "(" + str(commission_amount_rate) + "%)",
                                str(int(item_delivery_and_return_amount)) + "(" + str(
                                    item_delivery_and_return_amount_rate) + "%)",
                                str(int(orders_amount)),
                                str(int(returns_amount)) + "(" + str(returns_amount_rate) + "%)",
                                str(int(services_amount)) + "(" + str(services_amount_rate) + "%)",
                                str(int(return_commission)) + "(12%)",
                                str(int(cost)) + "(30%)",
                                str(int(profit)) + "(" + str(profit_rate) + "%)"))
    insert_profit_statement(table_infos)
