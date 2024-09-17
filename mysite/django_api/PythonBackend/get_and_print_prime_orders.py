import csv
import logging
import os
import sys

import requests


# 配置日志
def configure_logging(log_filename):
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
# os读取项目路径
project_path = os.path.dirname(os.path.abspath(__file__))


class PrimeOrdersProcess:
    """
    用于批量查询部件价格，可选在线查询和本地查询（true为在线查询）
    传入参数格式为 galatine_prime_handle,hystrix_prime_set,khora_prime_set 1
    参数1：部件列表 使用逗号分割查询部件
    参数2：是否在线查询，默认为False，可为空。
    返回一个字典，
    key为url_name，value为在线订单前三个价格列表
    {'galatine_prime_handle': '['galatine_prime_handle', '3', '4', '5']'}
    """

    def __init__(self, prime_url_name_list, search_online):
        self.prime_url_name_list = prime_url_name_list.split(',')
        # 是否查询在线订单
        self.search_online = search_online
        print("是否在线订单："+str(search_online))
        # 初始化一个字典，保存url_name，和三个最低价price1,price2,price3
        self.prime_dict = {}
        self.main(self.prime_url_name_list)

        # for key, value in self.prime_dict.items():
        #     print(f"{key}: {value}")

    def main(self, prime_url_name_list):

        for url_name in prime_url_name_list:
            # 是否查询在线订单
            if self.search_online:
                print(f"正在在线查询{url_name}")
                #得到该url_name的订单数据
                order_json = self.fetch_sell_orders(url_name)
                # 返回带有3个价格的订单列表
                price_list = self.extract_and_filter_orders(order_json)
            else:
                # 本地查询
                price_list = self.get_prime_prices_local(url_name)
            # 构造指定格式列表[url_name,price_list[0],price_list[1],price_list[2]]，添加到字典
            self.prime_dict[url_name] = [url_name] + price_list

    def fetch_sell_orders(self, url_name):
        url = f'https://api.warframe.market/v1/items/{url_name}/orders'
        try:
            response = requests.get(url)
            response.raise_for_status()  # 抛出HTTP错误
            return response.json()
        except requests.RequestException as e:
            logging.error(f"异常： {url}: {e}")
            return None

    def extract_and_filter_orders(self, orders_json):
        if orders_json is None:
            return []
        orders_data = orders_json['payload']['orders']
        # 筛选订单
        filtered_orders = [order for order in orders_data if
                           order['order_type'] == 'sell' and order['user']['status'] in ['ingame', 'online']]
        # 排序订单
        sorted_orders = sorted(filtered_orders, key=lambda x: x['platinum'])
        # 取前三条记录的价格
        top_prices = [str(order['platinum']) for order in sorted_orders[:3]]
        # 如果少于3条记录，则补充0
        while len(top_prices) < 3:
            top_prices.append('0')

        return top_prices

    # 本地查询
    def get_prime_prices_local(self, url_name):
        top_prices = []
        # 从本地读取primeprice.csv文件中的订单数据

        with open(f'{project_path}/static/primeprice.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # 创建一个字典阅读器
            for row in reader:  # 遍历每一行
                if row['url_name'] == url_name:
                    top_prices.append(row['platinum1'])
                    top_prices.append(row['platinum2'])
                    top_prices.append(row['platinum3'])
                    break  # 找到后停止搜索
        return top_prices


# if __name__ == "__main__":
#
#     if len(sys.argv) < 2:
#         print("Usage: python get_and_print_prime_orders.py [prime_url_list] online_search_defalut_is_0")
#     else:
#         # 使用从命令行接收的第一个参数
#         obj = PrimeOrdersProcess(sys.argv[1], sys.argv[2])
#         print(obj.prime_dict)
