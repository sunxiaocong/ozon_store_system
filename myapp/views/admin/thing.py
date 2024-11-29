# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Classification, Thing, Tag
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ThingSerializer, UpdateThingSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        c = request.GET.get("c", None)
        tag = request.GET.get("tag", None)
        if keyword:
            things = Thing.objects.filter(title__contains=keyword).order_by('-create_time')
        elif c:
            classification = Classification.objects.get(pk=c)
            things = classification.classification_thing.all()
        elif tag:
            tag = Tag.objects.get(id=tag)
            print(tag)
            things = tag.thing_set.all()
        else:
            things = Thing.objects.all().order_by('-create_time')
        serializer = ThingSerializer(things, many=True)

        return_data = serializer.data
        for item in return_data:
            price = item.get("price", 0)
            freight = item.get("freight", 0)  # 运费
            value_added_tax = item.get("value_added_tax", 0)  # 增值税
            tariff = item.get("tariff", 0)  # 关税
            shelf_cost = item.get("shelf_cost", 0)  # 上架费用
            all_cost = item.get("all_cost", 0)
            all_cost_property = round(float(all_cost) * float(item.get("property", 0)), 2)
            low_sell = all_cost * 14 * 4.5
            high_sell = all_cost * 14 * 6
            all_cost_detail = f"""采购价格: {price}<br />
增值税：{value_added_tax}<br />
运费：{freight}<br />
关税：{tariff}<br />
上架费用：{shelf_cost}<br />
总成本: {all_cost}<br />
最低售价(*4.5)：{low_sell} 卢布<br />
默认售价(*6)：{high_sell} 卢布<br />
在仓货值: <strong style="color: red;">{all_cost_property}</strong>"""

            length = item.get("length", 0)
            width = item.get("width", 0)
            height = item.get("height", 0)
            volume = item.get("volume", 0)

            volume_detail = f"{length}*{width}*{height}={volume}"
            item["all_cost_detail"] = all_cost_detail
            item["volume_detail"] = volume_detail
        return APIResponse(code=0, msg='查询成功', data=return_data)


@api_view(['GET'])
def detail(request):
    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')
    print(request.data)
    serializer = ThingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = UpdateThingSerializer(thing, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Thing.objects.filter(id__in=ids_arr).delete()
    except Thing.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')
