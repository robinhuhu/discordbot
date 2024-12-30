import requests
import json
import random
import time
from datetime import datetime
# 目标频道 ID

channels=[
        "频道1",
        "频道2",
       
    ]


# 读取 user.json 文件
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 向频道发送消息的函数
def chat(user_data,channel_id):
    token = user_data['token']
    proxy = user_data['proxy']
    message = user_data['message']
    user_agent = user_data['user_agent']

    header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": user_agent
    }

    msg = {
        "content": message,  # 使用文件中的消息内容
        "tts": False
    }

    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        res = requests.post(url=url, headers=header, data=json.dumps(msg), proxies=proxies)
        res_data = res.json()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Message sent: Status Code: {res.status_code}, Content: {res_data['content']}")
    except Exception as e:
        print(f"Error sending message: {e}")

# 主函数
if __name__ == '__main__':
    user_data_list = read_user_data('user.json')
   
       # 每8小时执行一次
    while True:
        for user_data in user_data_list:
            for channel_id in channels:
                chat(user_data, channel_id)
                time.sleep(random.randint(1, 10))  # 添加随机延迟避免频繁请求
        print("Sleeping for 8 hours...")
        time.sleep(8 * 60 * 60)  # 休眠8小时
