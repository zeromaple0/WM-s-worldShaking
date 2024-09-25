import requests
import json
import os

# 获取项目路径
project_directory = os.path.dirname(os.path.abspath(__file__))


class Login:
    def __init__(self, email, password, device_id):
        self.email = email
        self.password = password
        self.device_id = device_id
        self.response = {}
        self.main()

    def main(self):
        # 定义请求的URL
        url = "https://api.warframe.market/v1/auth/signin"
        # 构造请求体的数据
        data = {
            "auth_type": "cookie",
            "email": self.email,
            "password": self.password,
            "device_id": "ru-789abc-123def-456ghi-789jkl"
        }

        # 将字典转换为JSON字符串
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'ru-789abc-123def-456ghi-789jkl'
                   }

        # 发送POST请求
        self.response = requests.post(url, data=json.dumps(data), headers=headers)

        # 检查响应状态码
        if self.response.status_code == 200:
            print("请求成功！")
            print("响应内容:", self.response.json())
            # 打印请求头
            print("请求头:", self.response.headers)
            # 保存response.headers的Set-Cookie到config.json配置文件中的cookie字段中
            response_headers = self.response.headers
            # 读取配置文件
            config_path = 'config.json'
            with open(os.path.join(project_directory, config_path), 'r') as f:
                config_data = json.load(f)
            config_data['Cookie'] = response_headers['Set-Cookie']
            config_data['ingame_name'] = self.response.json()['payload']['user']['ingame_name']
            config_data['id'] = self.response.json()['payload']['user']['id']
            # 写入配置文件
            with open(os.path.join(project_directory, config_path), 'w') as f:
                json.dump(config_data, f)
            self.response["message"] = "登陆成功"
        else:
            print(f"请求失败，状态码: {self.response.status_code}")
            print("返回内容:", self.response.json())
            self.response = {"message": "登陆失败"}
