# Create your views here.

from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Thing
from myapp.serializers import ThingSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", '')
        if keyword:
            things = Thing.objects.filter(sku__contains=keyword).order_by('-sku')
        else:
            things = Thing.objects.all().order_by('-sku')
        # 打印结果
        serializer = ThingSerializer(things, many=True)

        r_data = []
        s_data = serializer.data
        for item in s_data:
            if float(item.get("property", 0)) > float(item.get("purchase", 0)) * 0.9:
                r_data.append(item)
        return APIResponse(code=0, msg='查询成功', data=r_data)
