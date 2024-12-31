import requests
import json
import random
import time
from datetime import datetime
import threading
import logging
# 目标频道 ID
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

channels=[
        "改为目标频道ID"
       
       
    ]
def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_random_quote(quotes):
    random_index = random.randint(0, len(quotes) - 1)
    return quotes[random_index]['text']

# 读取 user.json 文件
def read_user_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def deleteMessage(channel_id,messageId,proxy,header):
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages/{messageId}'
    proxies = {
        "http": proxy,
        "https": proxy
    }
    try:
        #url = f"{self.base_url}/channels/{channel_id}/messages/{message_id}"
        response = requests.delete(url, headers=header,proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功，如果不成功则抛出异常
        return response.status_code
    except requests.RequestException as error:
        logging.error(f"Error deleting message in channel: {error}")
        raise

# 向频道发送消息的函数
def chat(user_data,channel_id,quotes):
    token = user_data['token']
    proxy = user_data['proxy']
    #message = user_data['message']
    message = get_random_quote(quotes)
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
        if 'content' in res_data:
            logging.info(f"Message sent: Status Code: {res.status_code}, Content: {res_data['content']}")
        else:
            logging.warning(f"Message sent but 'content' key is missing in response: {res_data}")

        #print(f"[{current_time}] Message sent: Status Code: {res.status_code}, Content: {res_data['content']}")
        messageId = res_data.get('id', None)
        time.sleep(random.randint(2, 7))
        if messageId:
            dele_state = deleteMessage(channel_id,messageId,proxy,header)
            logging.info(f"Deleted Message: {messageId} Status Code: {dele_state}")
        

    except Exception as e:
        print(f"Error sending message: {e}")

def user_thread(user_data):
    quotes = load_quotes('quotes-en.json')
    while True:
        for channel_id in channels:
            chat(user_data, channel_id, quotes)
            time.sleep(random.randint(32, 46))  # 添加随机延迟避免频繁请求

# 主函数
if __name__ == '__main__':
    user_data_list = read_user_data('user.json')
    threads = []
    
    for user_data in user_data_list:
        thread = threading.Thread(target=user_thread, args=(user_data,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
