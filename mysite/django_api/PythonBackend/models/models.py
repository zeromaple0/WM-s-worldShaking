# 用于序列化订单
class RivenOrders:
    def __init__(self, weapon_url,prices):
        self.weapon_url = weapon_url
        self.prices = prices
class Chats:
    def __init__(self,chat_name,messages):
        self.chat_name = chat_name
        self.messages = messages