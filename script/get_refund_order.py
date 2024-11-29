from datetime import datetime
import hashlib
import requests
import json


def get_refund_order():
    url = 'http://www.xxl-express.net/wms-main/api'
    api_key = 'A1C67A99AC0FBF5C0FA94ACC73F56D10'  # 替换为你的实际 API 密钥
    # 获取当前时间
    current_time = datetime.now()

    # 将当前时间按照指定格式进行格式化
    req_time = current_time.strftime('%Y-%m-%d %H:%M:%S')  # 示例请求时间
    method = 'searchReturnOrder'  # 示例请求方法
    partner_code = 'O9880'  # 示例合作伙伴代码

    # 请求体内容
    req_body = {
        "startTime": "2024-09-01 00:00:00",
        "endTime": "2024-10-01 00:00:00",
        "pageSize": 100,
        "page": 1
    }

    # 将请求体转换为 URL 编码格式
    req_body_encoded = json.dumps(req_body)

    # 构建签名字符串
    signature_string = f"{req_time}&{method}&{partner_code}&{api_key}&{req_body_encoded}"
    print(signature_string)

    # 计算签名
    signature = hashlib.md5(signature_string.encode()).hexdigest().upper()
    print(signature)

    # 构建请求参数
    payload = {
        'reqTime': req_time,
        'method': method,
        'partnerCode': partner_code,
        'reqBody': req_body_encoded,  # 使用 URL 编码的请求体
        'sign': signature
    }
    print(payload)

    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    # 发送 HTTP POST 请求
    response = requests.post(url, data=payload, headers=headers)  # 使用 data 参数
    print(response.text)

    # 打印响应内容
    return response.json().get("data", [])



get_refund_order()
