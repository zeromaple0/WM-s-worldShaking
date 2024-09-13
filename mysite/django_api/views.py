import json

from django.http import HttpResponse
from .PythonBackend import get_and_print_prime_orders


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getprimeprice(request):  # 获得prime部件价格
    # 解析request.GET
    search_online = False
    prime_url_name_list = request.GET.get('prime_url_name_list')
    print("得到的prime_url_name_list为："+prime_url_name_list)
    if request.GET.get('search_online') != None:
        search_online = request.GET.get('search_online')
        print("得到的search_online为："+search_online)
    price = get_and_print_prime_orders.PrimeOrdersProcess(prime_url_name_list, search_online)
    # 把price.prime_dict转为json
    json_data = json.dumps(price.prime_dict)

    print(json_data)
    return HttpResponse(json_data)
