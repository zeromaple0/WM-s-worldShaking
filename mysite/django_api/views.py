import json
import logging

from django.http import HttpResponse, JsonResponse

from .PythonBackend import get_and_print_prime_orders
from .PythonBackend import get_and_print_riven_orders
from .PythonBackend import login
from .models import PrimePrice, RivenPrice
from .update_price import Update_prime_price, Update_riven_price


def api(request):
    # 展示所有api
    return JsonResponse({

        'endpoints': [
            '/api/update_prime_price/',
            '/api/getprimeprice/',
            '/api/getrivenprice/'
        ]
    })


# 获取logger实例
logger = logging.getLogger(__name__)

"""
更新本地数据库
传入参数
{
    "update_file_url": "C:\\Users\\cc\\Downloads\\price_091915.csv"
}
"""


def update_prime_price(request):
    if request.method == 'POST':
        try:
            # 解码请求体
            body_str = request.body.decode('utf-8')
            # 解析JSON数据
            data = json.loads(body_str)
            update_file_url = data.get('update_file_url')
            print("接受到的路径为：" + update_file_url)
            update = Update_prime_price(update_file_url)
            return JsonResponse({'message': f'prime price 价格更新成功,{update.count}条数据发生变化'})
        except Exception as e:
            print(e)

def update_riven_price(request):
    if request.method == 'POST':
        try:
            # 解码请求体
            body_str = request.body.decode('utf-8')
            # 解析JSON数据
            data = json.loads(body_str)
            update_file_url = data.get('update_file_url')
            print("接受到的路径为：" + update_file_url)
            update = Update_riven_price(update_file_url)
            return JsonResponse({'message': f'prime price 价格更新成功,{update.count}条数据发生变化'})
        except Exception as e:
            print(e)




"""
请求方法POST ，json格式发送
{
    "prime_url_name_list": "akjagara_prime_receiver,wyrm_prime_blueprint",
    "search_online": 0                     //0表示本地查询，1为在线查询，默认为0
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

            # 进行本地数据库查询
            if search_online == 0:
                print("开始本地数据库查询")
                # 初始化一个列表保存结果
                prime_price_list = []
                # 初始化一个字典用于转为json
                prime_price_dict = {}

                for url_name in prime_url_name_list.split(','):
                    print("正在查询:" + url_name)
                    primeprice = PrimePrice.objects.get_prime_price(url_name)

                    prime_price_list.append(primeprice)

                prime_price_dict['orders'] = prime_price_list
                return JsonResponse(prime_price_dict)
            # 进行在线查询
            if search_online == 1:
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
    "weapon_url_name_list":"quartakk,magistar",
    "days":30,
    "count_orders":3
}
"""


def getrivenprice(request):
    if request.method == 'POST':
        try:
            # 从POST请求体中获取数据
            # 首先检查请求体是否为空
            if not request.body:
                print(request.body)
                return JsonResponse({'error': 'Request body is empty'}, status=400)
            body_str = request.body.decode('utf-8')
            data = json.loads(body_str)
            weapon_url_name_list = data.get('weapon_url_name_list')
            days = data.get('days')
            count_orders = data.get('count_orders')
            # 本地查询
            if data.get('search_online') == 0:
                print("开始本地数据库查询")
                # 初始化一个列表保存结果
                riven_price_list = []
                # 初始化一个字典用于转为json
                riven_price_dict = {}

                for url_name in weapon_url_name_list.split(','):
                    print("正在查询:" + url_name)
                    rivenprice = RivenPrice.objects.get_riven_price(url_name)

                    riven_price_list.append(rivenprice)

                riven_price_dict['orders'] = riven_price_list
                return JsonResponse(riven_price_dict)


            rivenprice = get_and_print_riven_orders.RivenOrdersProcess(weapon_url_name_list, days, count_orders)
            json_data = json.dumps(rivenprice.orders_dict_to_json)
            return HttpResponse(json_data)
        except Exception as e:
            print(e)
    else:
        return HttpResponse('Invalid request method', status=405)


def login2wm(request):
    if request.method == 'POST':
        try:
            body_str = request.body.decode('utf-8')
            data = json.loads(body_str)
            email = data.get('email')
            password = data.get('password')
            device_id = data.get('device_id')
            login_obj = login.Login(email, password, device_id)
            return HttpResponse(login_obj.response)
        except Exception as e:
            print(e)


