import os
import requests
import json

# 获取当前项目路径
path = os.getcwd()
data_path = 'django_api\\PythonBackend\\data\\chats_data.json'
# 读取本地数据
print(os.path.join(path, data_path))


class Get_message:

    def __init__(self):
        self.local_chats_data = json.load(open(os.path.join(path, data_path), 'r', encoding='utf-8'))
        print(self.local_chats_data)
        self.back_response = {}
        self.main()
# 获取最新聊天消息
    def request_message(self):
        # 构造一个config.json的对象
        config_data = json.load(open(os.path.join(path, "django_api\\PythonBackend\\config.json")))

        url = "https://api.warframe.market/v1/im/chats"
        headers = {'Content-Type': 'application/json',
                   'Cookie': config_data['Cookie']
                   }

        return requests.get(url, headers=headers)


    # 检测是否有新消息
    def check_new_message(self,response):
        # 提取本地保存的所有聊天名称
        local_chat_names = [i['chat_name'] for i in self.local_chats_data.get('payload', {}).get('chats', [])]
        dict_data = {}
        list_data = []

        chats = []
        # 检测是否有新的用户发来消息
        for chat_item in response['payload']['chats']:
            dict_data = {}
            if chat_item['chat_name'] not in local_chat_names:
                print("新的用户:" + chat_item['chat_name'] + " 向您发来一条新消息")
                dict_data['message'] = "新的用户:" + chat_item['chat_name'] + " 向您发来一条新消息"
                list_data.append(dict_data)
        # 检测是否有旧用户发来的新消息
        for chat_item in response['payload']['chats']:
            dict_data = {}
            for local_chat in self.local_chats_data['payload']['chats']:
                if chat_item['chat_name'] == local_chat['chat_name']:
                    if chat_item['messages'] != local_chat['messages']:
                        print("用户:" + chat_item['chat_name'] + " 向您发来一条新消息")

                        print(chat_item['messages'][0]['message'])
                        dict_data['message'] = "用户:" + chat_item['chat_name'] + " 向您发来一条新消息" + \
                                               chat_item['messages'][0]['message']
                        list_data.append(dict_data)
                        continue
        # 返回消息
        self.back_response['message'] = list_data

    def save_response(self,response):
        try:
            json.dump(response, open(os.path.join(path, data_path), 'w', encoding='utf-8'), ensure_ascii=False)
        except Exception as e:
            print(e)

    def main(self):
        response = self.request_message().json()
        self.check_new_message(response)
        self.save_response(response)



# 保存接收到的response到本地

