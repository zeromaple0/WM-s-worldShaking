import json
import logging

from django.http import HttpResponse, JsonResponse
from .PythonBackend import get_and_print_prime_orders
from .PythonBackend import get_and_print_riven_orders


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# 获取logger实例
logger = logging.getLogger(__name__)

"""
请求方法POST ，json格式发送
{
    "prime_url_name_list": "akjagara_prime_receiver,wyrm_prime_blueprint",
    "search_online": "False"
}
"""


def getprimeprice(request):
    if request.method == 'POST':
        try:
            # 从POST请求体中获取数据
            # 首先检查请求体是否为空
            if not request.body:
                print(request.body)
                return JsonResponse({'error': 'Request body is empty'}, status=400)

            # 解码请求体
            body_str = request.body.decode('utf-8')

            # 解析JSON数据
            data = json.loads(body_str)

            # 获取参数
            prime_url_name_list = data.get('prime_url_name_list')
            search_online = data.get('search_online', 0)  # 默认值0，不进行在线查询
            # 打印接收到的参数
            logger.info("得到的prime_url_name_list为：%s", prime_url_name_list)
            logger.info("得到的search_online为：%s", search_online)

            # 开始处理订单
            price = get_and_print_prime_orders.PrimeOrdersProcess(prime_url_name_list, search_online)
            # 把price.prime_dict转为json
            json_data = json.dumps(price.prime_dict)
            # 返回JSON响应
            return HttpResponse(json_data)

        except json.JSONDecodeError as e:
            # 处理JSON解码错误
            logger.error("JSON Decode Error: %s", e)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except KeyError as e:
            # 处理缺失键的错误
            logger.error("Key Error: %s", e)
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        except Exception as e:
            # 处理其他可能的错误
            logger.error("General Error: %s", e)
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # 错误的方法类型
        return JsonResponse({'error': 'Invalid request method'}, status=405)

"""
请求方法POST
{
    "weapon_url_name_list": "magistar,quartakk",
    "days": 30,
    "count_orders": 3
}

"""
def getrivenprice(request):

    if request.method=='POST':
        try:
            # 从POST请求体中获取数据
            # 首先检查请求体是否为空
            if not request.body:
                print(request.body)
                return JsonResponse({'error': 'Request body is empty'}, status=400)
            body_str=request.body.decode('utf-8')
            data=json.loads(body_str)
            weapon_url_name_list=data.get('weapon_url_name_list')
            days = data.get('days')
            count_orders = data.get('count_orders')

            rivenprice = get_and_print_riven_orders.RivenOrdersProcess(weapon_url_name_list, days, count_orders)
            json_data = json.dumps(rivenprice.riven_dict)
            return HttpResponse(json_data)
        except Exception as e:
            print(e)
    else:
        return HttpResponse('Invalid request method', status=405)
