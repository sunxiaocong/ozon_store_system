# Create your views here.
import re

from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import ProfitStatement
from myapp.serializers import ProfitStatementSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        if keyword:
            ps = ProfitStatement.objects.filter(store_name=keyword).order_by('-period')
        else:
            ps = ProfitStatement.objects.all().order_by('-period')
        # 打印结果
        serializer = ProfitStatementSerializer(ps, many=True)

        # 计算汇总数据
        def extract_value(value_str):
            # 使用正则表达式提取数值部分
            match = re.match(r'([-+]?\d*\.?\d+)', value_str)
            return float(match.group(1)) if match else 0.0

        total_commission_amount = sum(extract_value(item['commission_amount']) for item in serializer.data)
        total_item_delivery_and_return_amount = sum(
            extract_value(item['item_delivery_and_return_amount']) for item in serializer.data)
        total_orders_amount = sum(extract_value(item['orders_amount']) for item in serializer.data)
        total_returns_amount = sum(extract_value(item['returns_amount']) for item in serializer.data)
        total_services_amount = sum(extract_value(item['services_amount']) for item in serializer.data)
        total_return_commission = sum(extract_value(item['return_commission']) for item in serializer.data)
        total_cost = sum(extract_value(item['cost']) for item in serializer.data)
        total_profit = sum(extract_value(item['profit']) for item in serializer.data)

        # 添加汇总数据
        summary_data = {
            'store_name': '总计',
            'period': '',
            'commission_amount': f"{total_commission_amount}({(total_commission_amount / total_orders_amount * 100) if total_orders_amount else 0:.2f}%)",
            'item_delivery_and_return_amount': f"{total_item_delivery_and_return_amount}({(total_item_delivery_and_return_amount / total_orders_amount * 100) if total_orders_amount else 0:.2f}%)",
            'orders_amount': total_orders_amount,
            'returns_amount': total_returns_amount,
            'services_amount': total_services_amount,
            'return_commission': f"{total_return_commission}({(total_return_commission / total_orders_amount * 100) if total_orders_amount else 0:.2f}%)",
            'cost': total_cost,
            'profit': total_profit,
        }

        # 将汇总数据添加到序列化数据中
        response_data = serializer.data
        response_data.append(summary_data)

        return APIResponse(code=0, msg='查询成功', data=response_data)
