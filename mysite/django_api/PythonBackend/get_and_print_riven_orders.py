from datetime import datetime, timedelta
import requests


class RivenOrdersProcess:
    """
      处理裂隙订单的类
        传入参数为： weapon_url列表，days,count_orders
        weapon_url:武器的url_name
        days:需要查询多少天内的订单
        count_orders：需要查询多少个订单
        数据保存在riven_dict字典中
        {'magistar': ['magistar', 450, 450, 479, 480], 'arca_titron': ['arca_titron', 150, 160, 160, 170], 'torid': ['torid', 500, 500, 540, 550]}
      """

    def __init__(self, weapon_url_list, days, count_orders):
        self.days = int(days)
        self.weapon_url_list = weapon_url_list.split(',')
        self.count_orders = int(count_orders)
        # 初始化一个字典，保存url_name，和count_orders数量的最低价
        self.riven_dict = {}
        self.main()
    def main(self):

        # 尝试获取订单JSON数据
        for weapon_url in self.weapon_url_list:
            # 保存每笔订单的价格 列表
            price_list = []
            try:
                orders_json = self.get_riven_price_(weapon_url)
            except Exception as e:
                print(f"错误：在获取订单JSON数据时发生错误: {e}")
                return

            if orders_json is not None:
                # 尝试提取并过滤订单
                try:
                    get_orders = self.extract_and_filter_orders(orders_json, self.count_orders, self.days)
                    for order in get_orders:
                        # 保存每一笔订单的价格
                        price_list.append(order['buyout_price'])
                except Exception as e:
                    print(f"错误：尝试提取过滤订单时出错，请检查传入的参数"+e)
                    return

            else:

                self.riven_dict[weapon_url] = [weapon_url] + price_list
            self.riven_dict[weapon_url] = [weapon_url] + price_list
        # 打印订单
        self.print_orders()

    #查找价格
    def get_riven_price_(self, weapon_url):
        try:
            RivenOrders = requests.get(
                url=f'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={weapon_url}&sort_by=price_asc')
            return RivenOrders.json()
        except requests.RequestException as e:

            return None

    # 对订单主要信息提取(默认保留days天内的前15个售卖订单)
    def extract_and_filter_orders(self, orders_json, count_orders, days=30):
        """
               提取并筛选订单数据。
               根据给定的时间范围和订单数量限制，从JSON订单数据中提取并筛选出符合条件的订单。
               该函数主要关注在指定天数内创建的直接购买订单（排除拍卖订单）。

               参数:
               orders_json : dict
                   包含订单数据的JSON格式字典。
               count_orders : int
                   需要返回的订单数量限制。
               days : int, optional
                   筛选订单的时间范围（以天为单位，默认为30天）。

               返回:
               list
                   筛选后的订单列表。
               """
        if orders_json is None:
            return []
        orders = orders_json['payload']['auctions']
        # 获取当前日期时间
        now = datetime.now()
        # 计算一个月前的日期
        one_month_ago = now - timedelta(days=days)
        #保存符合条件的订单列表
        filter_orders_res = []

        # 提取一个月内的售卖订单
        for order in orders:
            # 保存符合数量的订单就退出
            if len(filter_orders_res) == count_orders:

                break

            # 如果是拍卖订单直接跳过
            if order['starting_price'] != order['buyout_price']:
                continue
            create_time = datetime.fromisoformat(order['created'].replace("T", " ").replace("+00:00", ""))
            # 如果订单在指定天数内，就保存该订单
            if one_month_ago <= create_time:
                filter_orders_res.append(order)

        return filter_orders_res

    # 打印字典里面的内容
    def print_orders(self):
        print(self.riven_dict)


# if __name__ == '__main__':
#     wepon_url_list = ['magistar','arca_titron','torid']
#     rivenprice = RivenOrdersProcess(wepon_url_list, days=30, count_orders=4)
    # rivenprice.main()
