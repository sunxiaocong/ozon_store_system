# Create your views here.
import datetime
import locale
import platform
import time
from multiprocessing import cpu_count

import psutil
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.utils import dict_fetchall


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def count(request):
    if request.method == 'GET':
        now = datetime.datetime.now()

        # 查看当前商品总数
        sql_thing_all = "select count(1) as thing_all from b_thing "
        with connection.cursor() as cursor:
            cursor.execute(sql_thing_all)
            thing_all_dict = dict_fetchall(cursor)

        sql_thing_selling = "select count(1) as thing_selling from b_thing where  property != 0"
        with connection.cursor() as cursor:
            cursor.execute(sql_thing_selling)
            thing_selling_dict = dict_fetchall(cursor)

        sql_thing_clean = "select count(1) as thing_clean from b_thing where property = 0"
        with connection.cursor() as cursor:
            cursor.execute(sql_thing_clean)
            thing_clean_dict = dict_fetchall(cursor)

        sql_thing_assets = "SELECT SUM(all_cost * property) AS thing_assets,SUM(all_cost * fbo_property) AS thing_fbo_assets FROM b_thing;"
        with connection.cursor() as cursor:
            cursor.execute(sql_thing_assets)
            thing_assets_dict = dict_fetchall(cursor)

        sql_finance_assets = "SELECT ROUND(SUM(CASE WHEN type = 0 THEN money ELSE -money END), 2) AS finance_assets FROM b_finance"
        with connection.cursor() as cursor:
            cursor.execute(sql_finance_assets)
            finance_assets_dict = dict_fetchall(cursor)

        sql_order_delivering = "SELECT SUM(order_amount) AS total_amount, SUM(count) AS total_count FROM b_order WHERE status = 0;"
        with connection.cursor() as cursor:
            cursor.execute(sql_order_delivering)
            order_delivering_dict = dict_fetchall(cursor)

        sql_order_delivered = "SELECT SUM(order_amount) AS total_amount, SUM(count) AS total_count FROM b_order WHERE status = 1;"
        with connection.cursor() as cursor:
            cursor.execute(sql_order_delivered)
            order_delivered_dict = dict_fetchall(cursor)

        sql_order_cancel = "SELECT SUM(order_amount) AS total_amount, SUM(count) AS total_count FROM b_order WHERE status in (2, 99);"
        with connection.cursor() as cursor:
            cursor.execute(sql_order_cancel)
            order_cancel_dict = dict_fetchall(cursor)

        sql_order_rank = "select sku as title, SUM(count) as count from b_order group by title order by count desc limit 15;"
        with connection.cursor() as cursor:
            cursor.execute(sql_order_rank)
            order_rank_data = dict_fetchall(cursor)

        # # 统计排名(sql语句)
        # sql_str = "select id, title, pv as count from b_thing  order by pv desc limit 10 "
        # with connection.cursor() as cursor:
        #     cursor.execute(sql_str)
        #     order_rank_data = dict_fetchall(cursor)
        #
        # # 统计分类比例(sql语句)
        # sql_str = "select B.title, count(B.title) as count from b_thing A join B_classification B on " \
        #           "A.classification_id = B.id group by B.title order by count desc limit 5; "
        # with connection.cursor() as cursor:
        #     cursor.execute(sql_str)
        #     classification_rank_data = dict_fetchall(cursor)
        #
        # # 统计最近一周访问量(sql语句)
        # visit_data = []
        # week_days = utils.getWeekDays()
        # for day in week_days:
        #     sql_str = "select re_ip, count(re_ip) as count from b_op_log where re_time like '" + day + "%' group by re_ip"
        #     with connection.cursor() as cursor:
        #         cursor.execute(sql_str)
        #         ip_data = dict_fetchall(cursor)
        #         uv = len(ip_data)
        #         pv = 0
        #         for item in ip_data:
        #             pv = pv + item['count']
        #         visit_data.append({
        #             "day": day,
        #             "uv": uv + random.randint(1, 20),
        #             "pv": pv + random.randint(20, 100)
        #         })
        thing_assets = thing_assets_dict[0].get("thing_assets", 0)
        thing_fbo_assets = thing_assets_dict[0].get("thing_fbo_assets", 0)
        finance_assets = finance_assets_dict[0].get("finance_assets", 0)
        total_assets = thing_assets + finance_assets + thing_fbo_assets
        data = {
            'thing_all': thing_all_dict[0].get("thing_all", 0),
            'thing_selling': thing_selling_dict[0].get("thing_selling", 0),
            'thing_clean': thing_clean_dict[0].get("thing_clean", 0),
            'thing_assets': round(thing_assets, 3),
            'finance_assets': round(finance_assets, 3),
            'thing_fbo_assets': round(thing_fbo_assets, 3),
            'total_assets': round(total_assets, 3),
            'order_delivering_count': order_delivering_dict[0].get("total_count", 0),
            'order_delivering_price': order_delivering_dict[0].get("total_amount", 0),
            'order_delived_count': order_delivered_dict[0].get("total_count", 0),
            'order_delived_price': order_delivered_dict[0].get("total_amount", 0),
            'order_cancel_count': order_cancel_dict[0].get("total_count", 0),
            'order_cancel_price': order_cancel_dict[0].get("total_amount", 0),

            'order_rank_data': order_rank_data,
            'classification_rank_data': [],
            'visit_data': []
        }

        return APIResponse(code=0, msg='查询成功', data=data)


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def sysInfo(request):
    if request.method == 'GET':
        pyVersion = platform.python_version()
        osBuild = platform.architecture()
        node = platform.node()
        pf = platform.platform()
        processor = platform.processor()
        pyComp = platform.python_compiler()
        osName = platform.system()
        memory = psutil.virtual_memory()

        data = {
            'sysName': '后台管理平台',
            'versionName': '1.1.0',
            'osName': osName,
            'pyVersion': pyVersion,
            'osBuild': osBuild,
            'node': node,
            'pf': pf,
            'processor': processor,
            'cpuCount': cpu_count(),
            'pyComp': pyComp,
            'cpuLoad': round((psutil.cpu_percent(1)), 2),
            'memory': round((float(memory.total) / 1024 / 1024 / 1024), 2),
            'usedMemory': round((float(memory.used) / 1024 / 1024 / 1024), 2),
            'percentMemory': round((float(memory.used) / float(memory.total) * 100), 2),
            'sysLan': locale.getdefaultlocale(),
            'sysZone': time.strftime('%Z', time.localtime())
        }

        return APIResponse(code=0, msg='查询成功', data=data)
