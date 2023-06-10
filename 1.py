import requests
import random
import string
from configparser import ConfigParser
from urllib.parse import quote
import pyperclip
import subprocess

def generate_alias():
    characters = string.ascii_lowercase + string.digits
    alias = ''.join(random.choice(characters) for _ in range(8))
    return alias


def select_menu():
    print("1. 自定义别名 (需包含数字+字母，长度6位以上)")
    print("2. 随机生成别名")
    print("3. 开始收件")
    print("4. 退出")
    selection = input("请选择菜单项: ")
    return selection

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config

def write_config(config):
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def start_receiving():
    subprocess.run(['python', 'email_1.py'])

url = 'https://mailedit.hbtcm.edu.cn/Mail/AliasDataOK'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://mailedit.hbtcm.edu.cn/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

config = read_config()
token = config.get('Cookies', 'token')
cookies = {
    'MailWebUserId': quote(token + '%3d%3d')
}

while True:
    menu_choice = select_menu()

    if menu_choice == '1':
        alias = input("请输入alias: ")
    elif menu_choice == '2':
        alias = generate_alias()
    elif menu_choice == '3':
        start_receiving()
        continue
    elif menu_choice == '4':
        print("退出程序。")
        break
    else:
        print("无效的选择，请重新输入菜单项。")
        continue

    config.set('Cookies', 'token', token)
    config.set('Alias', 'alias', alias)
    write_config(config)

    data = {
        'alias': alias
    }

    response = requests.post(url, headers=headers, data=data, cookies=cookies)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        print(f"别名: {alias}@stmail.hbtcm.edu.cn")
        pyperclip.copy(f"{alias}@stmail.hbtcm.edu.cn")
        print("已将别名复制到剪贴板。")
    else:
        print('请求失败:', response.status_code)
