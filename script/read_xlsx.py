import mysql.connector
import pandas as pd

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
def update_b_thing(table_data):
    cnx = mysql.connector.connect(
        host=DATABASES.get("default").get("HOST"),
        user=DATABASES.get("default").get("USER"),
        password=DATABASES.get("default").get("PASSWORD"),
        database=DATABASES.get("default").get("NAME")
    )

    # 创建游标对象
    cursor = cnx.cursor()
    for data in table_data:
        sku = data[0]
        price = data[1]
        length = data[2]
        width = data[3]
        height = data[4]
        weight = data[5]
        packing_quantity = data[6]
        # 运费 体积m3*1500
        freight = data[7]
        # 最低报关金额
        low_tariff_price = data[8]
        # 关税 （运费+最低报关金额）*0.12
        tariff = data[9]
        # 增值税 (运费+成本+关税) * 0.2
        value_added_tax = data[10]
        # 上架费用
        shelf_cost = data[11]
        # 总成本
        all_cost = data[12]
        volume = data[13]
        update_query = """
            UPDATE b_thing 
            SET 
                price = {price}, 
                length = {length}, 
                width = {width}, 
                height = {height}, 
                weight = {weight}, 
                packing_quantity = {packing_quantity}, 
                freight = {freight}, 
                low_tariff_price = {low_tariff_price},
                tariff = {tariff}, 
                value_added_tax = {value_added_tax},
                shelf_cost={shelf_cost},
                all_cost={all_cost},
                sku='{sku}',
                volume={volume}
            WHERE sku = '{sku}'
            """.format(
            sku=sku,
            price=price,
            length=length,
            width=width,
            height=height,
            weight=weight,
            packing_quantity=packing_quantity,
            freight=freight,
            low_tariff_price=low_tariff_price,
            tariff=tariff,
            value_added_tax=value_added_tax,
            shelf_cost=shelf_cost,
            all_cost=all_cost,
            volume=volume
        )
        print(update_query)
        cursor.execute(update_query)

    # 提交更改
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()


# 读取 Excel 文件
df = pd.read_excel('sku2.xls')

update_list = []
# 遍历每一行
for index, row in df.iterrows():
    try:
        if index == 0:
            print("第一行数据")
            continue
        if str(row.values[0]):

            sku = "O9880-"+str(row.values[0]).strip()
            if sku in ("O9880-DM-000048"):
                continue
            price = float(row.values[5])
            length = float(row.values[6])
            width = float(row.values[7])
            height = float(row.values[8])
            weight = float(row.values[10])
            packing_quantity = int(row.values[11])

            # 运费 体积m3*1500
            freight = (length * width * height) / 1000000 * 1500
            # 最低报关金额
            low_tariff_price = weight * 4.5 * 7.3
            # 关税 （运费+最低报关金额）*0.12
            tariff = (freight + low_tariff_price) * 0.12

            # 增值税 (运费+成本+关税) * 0.2
            value_added_tax = (low_tariff_price + freight + tariff) * 0.2
            # 上架费用
            shelf_cost = weight * 3
            # 总成本 = 上架费用 + 增值税 + 关税 + 采购价格 + 运费
            all_cost = shelf_cost + value_added_tax + tariff + price + freight
            volume = (length * width * height) / 1000000
            print((sku, price, length, width, height, weight))
            update_list.append(
                (sku, price, length, width, height, weight, packing_quantity, round(freight, 3),
                 round(low_tariff_price, 3),
                 round(tariff, 3),
                 round(value_added_tax, 3), round(shelf_cost, 3), round(all_cost, 3), volume))
    except Exception as e:
        print(e)

update_b_thing(update_list)
