

import pandas as pd

# 读取 Excel 文件
file_path = '2024-10-14.xlsx'
df = pd.read_excel(file_path)

# 显示 DataFrame 的前几行
print(df.head())
print(df.keys())


amount_summary = df.groupby('科目')['金额'].sum().reset_index()

# 打印结果
print(amount_summary)

# 筛选出科目为“操作费”的所有明细数据
operating_fee_details = df[df['科目'] == '操作费']

# 打印结果
# 遍历并打印每一条记录
for index, row in operating_fee_details.iterrows():
    print(f"记录 {index}:")
    print(f"类型: {row['类型']}, 客户: {row['客户']}, 订单号: {row['订单号']}, 科目: {row['科目']}, "
          f"金额: {row['金额']}, 币种代码: {row['币种代码']}, 当前余额: {row['当前余额']}, "
          f"时间: {row['时间']}, 参考号: {row['参考号']}, 跟踪号: {row['跟踪号']}, "
          f"转单号: {row['转单号']}, 仓库: {row['仓库']}, 收件人国家: {row['收件人国家']}, "
          f"收件人邮编: {row['收件人邮编']}, 重量: {row['重量']}, 发货方式: {row['发货方式']}, "
          f"备注: {row['备注']}")


operating_fee_details = df[(df['科目'] == '运费') & (df['金额'] != 0)]

# 打印结果
# 遍历并打印每一条记录
for index, row in operating_fee_details.iterrows():
    print(f"记录 {index}:")
    print(f"类型: {row['类型']}, 客户: {row['客户']}, 订单号: {row['订单号']}, 科目: {row['科目']}, "
          f"金额: {row['金额']}, 币种代码: {row['币种代码']}, 当前余额: {row['当前余额']}, "
          f"时间: {row['时间']}, 参考号: {row['参考号']}, 跟踪号: {row['跟踪号']}, "
          f"转单号: {row['转单号']}, 仓库: {row['仓库']}, 收件人国家: {row['收件人国家']}, "
          f"收件人邮编: {row['收件人邮编']}, 重量: {row['重量']}, 发货方式: {row['发货方式']}, "
          f"备注: {row['备注']}")