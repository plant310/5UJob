# 导入相应的文件
import time
import requests
import json
import pandas as pd

# 加入请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
}

# 获取cookies值
def get_cookie():
    # 原始网页的URL
    url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    return cookie


# 定义获取页数的函数
def get_page(url, params):
    #建立请求
    html = requests.post(url, data=params, headers=headers, cookies=get_cookie(), timeout=5)
    # 将网页的Html文件加载为json文件
    json_data = json.loads(html.text)
    # 解析json文件，后跟中括号为解析的路径
    total_Count = json_data['content']['positionResult']['totalCount']
    # 调用get_info函数，传入url和页数
    get_info(url, int(total_Count), params)


# 定义获取招聘信息函数
def get_info(url, page,params):
    filename = 'LaGou_' + params['kd'] + '.csv' #文件名
    Information=[]#保存总的岗位信息
    for pn in range(1, page + 1):#遍历每一页
        print(pn)
        # 获取信息 并捕获异常
        try:
            html = requests.post(url, data=params, headers=headers, cookies=get_cookie(), timeout=5)

            # 将网页的Html文件加载为json文件
            json_data = json.loads(html.text)
            # 解析json文件，后跟中括号为解析的路径
            results = json_data['content']['positionResult']['result']
            Information=Information+results
            time.sleep(2)
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            pass
    pd.DataFrame(Information).to_csv(filename,encoding="utf_8_sig")


# 主程序入口
if __name__ == '__main__':
    url = "https://www.lagou.com/jobs/positionAjax.json"
    # post请求参数
    params = {
        "first": "true",
        "pn": 1,
        "kd": "全国"
    }

    get_page(url, params)
