# Create your views here.
from collections import defaultdict
from datetime import datetime

from django.db.models import Count
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Order


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        desc_key = request.GET.get("desc_key", '')
        if desc_key == '':
            desc_key = 'return_rate'

        start_time_f = request.GET.get("start_time", '')
        end_time_f = request.GET.get("end_time", '')
        if start_time_f != '' and end_time_f != '':
            start_time_datetime = datetime.strptime(start_time_f, "%Y-%m-%d %H:%M:%S")
            end_time_datetime = datetime.strptime(end_time_f, "%Y-%m-%d %H:%M:%S")
            order_counts = (
                Order.objects.filter(order_time__range=(start_time_datetime,
                                                        end_time_datetime)).
                    values('sku', 'status').annotate(
                    order_count=Count('id'))
            )
        else:
            order_counts = (
                Order.objects.values('sku', 'status')
                    .annotate(order_count=Count('id'))
            )  # 计算每组的订单数量
        # 创建一个默认字典来存储结果
        result = defaultdict(lambda: {'0_count': 0, '1_count': 0, '2_count': 0})

        # 遍历查询结果并填充字典
        for order in order_counts:
            sku = order['sku']
            status = order['status']
            count = order['order_count']

            if status == '0':
                result[sku]['0_count'] += count
            elif status == '1':
                result[sku]['1_count'] += count
            else:
                result[sku]['2_count'] += count

        # 将结果转换为所需的格式，并计算退货率
        final_result = []
        for sku, counts in result.items():
            if keyword not in sku:
                continue
            # 计算退货率，避免除以零
            if counts['1_count'] + counts['2_count'] > 0:
                return_rate = (counts['2_count'] / (counts['1_count'] + counts['2_count'])) * 100
            else:
                return_rate = 0  # 或者设置为 None，根据需求

            final_result.append({
                'sku': sku,
                '0_count': counts['0_count'],
                '1_count': counts['1_count'],
                '2_count': counts['2_count'],
                'return_rate': return_rate
            })

        # 降序排序
        final_result = sorted(final_result, key=lambda x: x[desc_key], reverse=True)

        # 打印结果
        return APIResponse(code=0, msg='查询成功', data=final_result)
