# Create your views here.
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import connection
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.utils import dict_fetchall


def get_current_month_day():
    # 获取当前日期
    current_date = datetime.now()

    # 获取当月1号的日期
    first_day_of_month = datetime(current_date.year, current_date.month, 1)

    # 获取当天日期
    current_day = current_date
    return first_day_of_month, current_day


store_id_map = {
    "001": "a",
    "002": "b",
    "003": "c",
    "004": "d",
    "005": "e",
    "006": "f",
}


def format_currency(value):
    # 格式化为带货币符号的字符串
    return f"{value:,.2f}"


def calculate_daily_totals(data_list):
    # 初始化汇总数据
    summary = {
        "key": 0,
        "day": "汇总",
        "a": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "b": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "c": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "d": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "e": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "f": {"revenue": 0, "model_cost": 0, "search_cost": 0},
        "total_revenue": "0 ₽",
        "total_model_cost": "0 ₽",
        "total_search_cost": "0 ₽",
        "model_cost_ratio": "0%",
        "search_cost_ratio": "0%"
    }

    for entry in data_list:
        for key in ['a', 'b', 'c', 'd', 'e', 'f']:
            summary[key]['revenue'] += float(entry[key]['revenue'])
            summary[key]['model_cost'] += float(entry[key]['model_cost'])
            summary[key]['search_cost'] += float(entry[key]['search_cost'])

    # 计算总汇总
    summary['total_revenue'] = float(summary['a']['revenue'] + summary['b']['revenue'] +
                                     summary['c']['revenue'] + summary['d']['revenue'] +
                                     summary['e']['revenue'] + summary['f']['revenue'])
    summary['total_model_cost'] = float(summary['a']['model_cost'] + summary['b']['model_cost'] +
                                        summary['c']['model_cost'] + summary['d']['model_cost'] +
                                        summary['e']['model_cost'] + summary['f']['model_cost'])
    summary['total_search_cost'] = float(summary['a']['search_cost'] + summary['b']['search_cost'] +
                                         summary['c']['search_cost'] + summary['d']['search_cost'] +
                                         summary['e']['search_cost'] + summary['f']['search_cost'])

    model_cost_ratio = summary['total_model_cost'] / summary['total_revenue'] * 100
    summary["model_cost_ratio"] = format_currency(model_cost_ratio) + "%"

    search_cost_ratio = (summary['total_search_cost'] / summary['total_revenue'] * 100)

    summary["search_cost_ratio"] = format_currency(search_cost_ratio) + "%"

    return summary


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        data = []
        try:
            start_time_datetime, end_time_datetime = get_current_month_day()

            start_time_f = request.GET.get("start_time", '')
            end_time_f = request.GET.get("end_time", '')

            if start_time_f != '' and end_time_f != '':
                start_time_datetime = datetime.strptime(start_time_f, "%Y-%m-%d %H:%M:%S")
                end_time_datetime = datetime.strptime(end_time_f, "%Y-%m-%d %H:%M:%S")

            start_time = start_time_datetime.strftime('%Y-%m-%d')
            end_time = end_time_datetime.strftime('%Y-%m-%d')

            # 获取广告花费
            oc_infos_sql = """SELECT * FROM ozon_cost WHERE day >= '{start_time}' AND day <= '{end_time}' AND cost_type in (0,1) order by day desc;""".format(
                start_time=start_time,
                end_time=end_time)

            with connection.cursor() as cursor:
                cursor.execute(oc_infos_sql)
                oc_dict = dict_fetchall(cursor)

            # 获取营业额
            sm_info_sql = """SELECT revenue,day,store_name FROM b_seller_metrics WHERE  day >= '{start_time}' AND day <= '{end_time}' order by day desc;""".format(
                start_time=start_time,
                end_time=end_time)

            with connection.cursor() as cursor:
                cursor.execute(sm_info_sql)
                sm_dict = dict_fetchall(cursor)

            oc_dict_by_day_store = {}
            for oc_info in oc_dict:
                day = oc_info['day'].strftime("%Y-%m-%d")
                store_name = oc_info['store_name']
                cost_type = str(oc_info['cost_type'])
                oc_dict_by_day_store[store_name + day + cost_type] = oc_info['cost']

            sm_dict_by_day_store = {}
            for sm_info in sm_dict:
                store_name = sm_info['store_name']
                day = sm_info['day'].strftime("%Y-%m-%d")
                sm_dict_by_day_store[store_name + day] = sm_info['revenue']

            current_day = start_time_datetime
            while current_day <= end_time_datetime:
                current_day_str = current_day.strftime('%Y-%m-%d')
                data_info = {
                    "day": current_day_str,
                }
                total_revenue = 0
                total_model_cost = 0
                total_search_cost = 0
                for k, v in store_id_map.items():
                    revenue = sm_dict_by_day_store.get(k + current_day_str, Decimal('0.00'))
                    total_revenue += revenue
                    model_cost = oc_dict_by_day_store.get(k + current_day_str + "0", Decimal('0.00'))
                    total_model_cost += model_cost
                    search_cost = oc_dict_by_day_store.get(k + current_day_str + "1", Decimal('0.00'))
                    total_search_cost += search_cost
                    data_info[v] = {
                        "revenue": str(revenue),  # 单日营业额
                        "model_cost": str(model_cost),  # 单日模版广告
                        "search_cost": str(search_cost),  # 单日搜索广告
                    }

                data_info["total_revenue"] = str(total_revenue)
                data_info["total_model_cost"] = str(total_model_cost)
                data_info["total_search_cost"] = str(total_search_cost.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
                data_info["model_cost_ratio"] = "0%"
                data_info["search_cost_ratio"] = "0%"
                if total_revenue != 0:
                    model_cost_ratio = total_model_cost / total_revenue * 100
                    print(model_cost_ratio)
                    data_info["model_cost_ratio"] = str(model_cost_ratio.quantize(Decimal('0.00'),
                                                                                  rounding=ROUND_HALF_UP)) + "%"
                    search_cost_ratio = (total_search_cost / total_revenue * 100)
                    print(search_cost_ratio)

                    data_info["search_cost_ratio"] = str(search_cost_ratio.quantize(Decimal('0.00'),
                                                                                    rounding=ROUND_HALF_UP)) + "%"

                current_day += timedelta(days=1)
                data.append(data_info)
            summary_data = calculate_daily_totals(data)
            data.append(summary_data)
        except Exception as e:
            print(e)

        return APIResponse(code=0, msg='查询成功', data=data)
