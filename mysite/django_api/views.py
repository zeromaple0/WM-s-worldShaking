import json

from django.http import HttpResponse, JsonResponse
from .PythonBackend import get_and_print_prime_orders
from .PythonBackend import get_and_print_riven_orders


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getprimeprice(request):  # 获得prime部件价格
    if request.method=='POST':
        try:
            #从post 中获取数据
            data=json.loads(request.body)
            prime_url_name_list = data.get('prime_url_name_list')
            search_online = data.get('search_online', False)
            # 打印接收到的参数
            print("得到的prime_url_name_list为：" + str(prime_url_name_list))
            print("得到的search_online为：" + str(search_online))

            # 开始处理订单
            price = get_and_print_prime_orders.PrimeOrdersProcess(prime_url_name_list, search_online)
            # 把price.prime_dict转为json
            json_data = json.dumps(price.prime_dict)

            # 返回JSON响应
            return JsonResponse(json_data, safe=False)
        except json.JSONDecodeError as e:
            # 处理JSON解码错误
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # 处理其他可能的错误
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # 错误的方法类型
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def getrivenprice(request):
    # 初始化列表weapon_url_name_list
    weapon_url_name_list = []
    weapon_url_name_list = request.GET.get('weapon_url_name_list')

    days = request.GET.get('days')
    count_orders = request.GET.get('count_orders')

    rivenprice = get_and_print_riven_orders.RivenOrdersProcess(weapon_url_name_list, days, count_orders)
    json_data = json.dumps(rivenprice.riven_dict)
    return HttpResponse(json_data)
