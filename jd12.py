#!/usr/bin/python3
#-*- coding: utf-8 -*-
import os
import urllib
import requests
import time
import json
import random
import re
from urllib import parse
import urllib3
import sys
from datetime import datetime
from threading import Thread
urllib3.disable_warnings()

# 循环任务次数，可以多跑几次没事
task_times = 15
# 间隔时间，默认在任务所需的基础上加，一般设置5s左右就成，看自己
sleep_times = 5

inviteIds = ['ZXASTT01076whGUBOqgFjRWnqW7zB55awQ', 'ZXASTT0225KkcRB5P8FGBdRimkKFbcgFjRWnqW7zB55awQ']
inviteId_temp_list = []
#是否愿意为作者助力：True, False
help_author = True
# 是否自动提升等级：True, False
auto_raise_level = True


cookies = [
    #'pt_key=xxxx; pt_pin=xxxx;',
]

class Logger(object):
    def __init__(self, filename='app.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.terminal.flush()  # 不启动缓冲,实时输出
        self.log.flush()

    def flush(self):
        pass

today = datetime.now().strftime("%Y-%m-%d")
sys.stdout = Logger(f'./jd12-{today}.log', sys.stdout)
sys.stderr = Logger(f'./jd12-{today}.log', sys.stderr)


if cookies:
    pass
else:
    print('看看放cookie没，自动退出')
    sys.exit()

def get_user_name(headers):
    cookie = headers['Cookie'] if 'Cookie' in headers else 'None'
    try:
        r = re.compile(r"pt_pin=(.*?);")
        userName = r.findall(cookie)
        userName = parse.unquote(userName[0])
        return userName
    except Exception as e:
        r = re.compile(r"pin=(.*?);")
        userName = r.findall(cookie)
        userName = parse.unquote(userName[0])
        return userName

# 获取joytoken
def get_joytoken(headers):
    url = 'https://rjsb-token-m.jd.com/gettoken'
    data = "content={\"appname\":\"50168\",\"whwswswws\":\"\",\"jdkey\":\"a\",\"body\":{\"platform\":\"1\",\"sceneid\":\"CXJAssist_h5\",\"hs\":\"AAD71C9\",\"version\":\"w4.0.5\"}}"
    try:
        res = requests.post(url, headers=headers,
                            data=data, verify=False).json()
        joytoken = res.get('joyytoken')
        return joytoken
    except Exception as e:
        print(e)
        return None

print('\n\n欢迎使用jd脚本\n')

def get_secretp(headers):
    url = 'https://api.m.jd.com/client.action?advId=promote_getHomeData'
    data = 'functionId=promote_getHomeData&client=m&clientVersion=-1&appid=signed_wh5&body={}'
    try:
        res = requests.post(url, data=data, headers=headers,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            return res.get('data').get('result').get('homeMainInfo').get('secretp')
        else:
            print('初始化失败')
            return None
    except:
        return None

def get_ss():
    import random,string
    a = [''.join(random.sample(string.ascii_letters + string.digits, 8)),"-1"]
    return a

# 逛店
def guangdian(taskId, taskToken, itemId, headers,actionType):
    url = 'https://api.m.jd.com/client.action?advId=promote_collectScore'
    ss = get_log()
    body = {
        "taskId": taskId,
        "taskToken": taskToken,
        "actionType": actionType,
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body).replace(" ", "")
    data = 'functionId=promote_collectScore&client=m&clientVersion=-1&appid=signed_wh5&body=' + bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('进店成功')
            return res
        else:
            print(res.get('data').get('bizMsg'))
    except Exception as e:
        print(e)

# 打卡
def daka(taskId, taskToken, headers):
    url = 'https://api.m.jd.com/client.action?advId=promote_collectScore'
    ss = get_log()
    body = {
        "taskId": taskId,
        "taskToken": taskToken,
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body).replace(" ", "")
    data = 'functionId=promote_collectScore&client=m&clientVersion=-1&appid=signed_wh5&body=' + bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('任务成功')
            return res
        else:
            print(res.get('data').get('bizMsg'))
    except Exception as e:
        print(e)

# 领取
def lingqu(taskToken, headers):
    url = 'https://api.m.jd.com/client.action?functionId=qryViewkitCallbackResult&client=wh5'
    body = {
        'dataSource': "newshortAward",
        'method': "getTaskAward",
        'reqParams': "{\"taskToken\":\"%s\"}" % taskToken,
        'sdkVersion': "1.0.0",
        'clientLanguage': "zh",
    }
    bodys = json.dumps(body)
    data = {
        'body': bodys,
    }
    try:
        response = requests.post(url, headers=headers,
                                 data=data, verify=False, timeout=5).json()
        if response.get('code') == '0':
            print(response.get('toast').get('subTitle'))
        else:
            print('其他')
    except Exception as e:
        print(e)

# 加购
def getFeedDetail(taskId, headers):
    url = 'https://api.m.jd.com/client.action?functionId=promote_getFeedDetail'
    data = 'functionId=promote_getFeedDetail&client=m&clientVersion=-1&appid=signed_wh5&body={"taskId":"%s"}' % taskId
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        productInfoVos = res.get('data').get('result').get(
            'addProductVos')[0].get('productInfoVos')
        return productInfoVos
    except Exception as e:
        print(e)

# 加购
def getFeedDetail1(taskId, headers):
    url = 'https://api.m.jd.com/client.action?functionId=promote_getFeedDetail'
    data = 'functionId=promote_getFeedDetail&client=m&clientVersion=-1&appid=signed_wh5&body={"taskId":"%s"}' % taskId
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        productInfoVos = res.get('data').get(
            'result').get('taskVos')[0].get('browseShopVo')
        return productInfoVos
    except Exception as e:
        print(e)

# 任务奖励
def getBadgeWard(awardToken, headers):
    url = 'https://api.m.jd.com/client.action?functionId=promote_getBadgeAward'
    data = 'functionId=promote_getFeedDetail&client=m&clientVersion=-1&appid=signed_wh5&body={"awardToken":"%s"}' % awardToken
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        myAwardVo = res.get('data').get('result').get('myAwardVos')[0]
        return myAwardVo
    except Exception as e:
        print(e)


# 任务列表
def task_list(headers, data):
    global inviteId_temp_list
    url = "https://api.m.jd.com/client.action?functionId=promote_getTaskDetail"
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('code') == 0:
            taskVos = res.get('data').get('result')
            inviteId = taskVos.get("inviteId")
            if inviteId is not None and inviteId not in inviteId_temp_list:
                inviteId_temp_list.append(inviteId)
                print(f'账号：{get_user_name(headers)}，助力码：{inviteId}')
            if inviteId is not None and inviteId not in inviteIds:
                inviteIds.append(inviteId)
            return taskVos
        else:
            print(res.get('msg'))
    except Exception as e:
        print(e)


def vxtask_list(headers, data):
    try:
        taskVos = task_list(headers, data).get('taskVos')
        lists = []
        for i in taskVos:
            taskId = i.get('taskId')
            status = i.get('status')
            taskTitle = i.get('taskName')
            subTitleName = i.get('subTitleName', '')
            if status == 1:
                waitDuration = i.get('waitDuration')
                shoppingActivityVos = i.get('shoppingActivityVos', '')
                browseShopVos = i.get('browseShopVo', '')
                followShopVos = i.get('followShopVo', '')
                simpleRecordInfoVos = i.get('simpleRecordInfoVo', '')
                if taskId in [24, 28]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    taskToken = simpleRecordInfoVos.get('taskToken')
                    daka(taskId, taskToken, headers)

                # shoppingActivityVos 需领取
                if taskId in [3, 6, 8, 12, 33, 34, 35, 36, 61, 67]:  #
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    for shop in shoppingActivityVos:
                        shopstatus = shop.get('status')
                        taskToken = shop.get('taskToken')
                        shoptitle = shop.get('title')
                        itemId = shop.get('itemId')
                        if shopstatus == 1:
                            print('任务“%s”' % shoptitle)
                            guangdian(taskId, taskToken, itemId, headers,1)
                            print('等待%s秒' % (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                            lingqu(taskToken, headers)
                # shoppingActivityVos 无需领取
                if taskId in [2, 7, 9, 10, 11, 13, 30, 32, 37, 38, 39, 63, 64, 65]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    for shop in shoppingActivityVos:
                        shopstatus = shop.get('status')
                        taskToken = shop.get('taskToken')
                        shoptitle = shop.get('title')
                        itemId = shop.get('itemId')
                        if shopstatus == 1:
                            print('任务“%s”' % shoptitle)
                            guangdian(taskId, taskToken, itemId, headers,1)
                            print('等待%s秒' % (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                if taskId in [3]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    for browseShop in browseShopVos:
                        browsestatus = browseShop.get('status')
                        browsetaskToken = browseShop.get('taskToken')
                        shopName = browseShop.get('shopName')
                        shopId = browseShop.get('shopId')
                        if browsestatus == 1:
                            print('任务“%s”' % shopName)
                            guangdian(taskId, browsetaskToken, shopId, headers,1)
                            print('等待%s秒' % (waitDuration + sleep_times))
                            time.sleep(int(waitDuration + sleep_times))
                            lingqu(browsetaskToken, headers)
                # 加购
                if taskId in [16, 17, 18, 19, 20, 21, 22, 23]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    productInfoVos = getFeedDetail(taskId, headers)
                    for productInfoVo in productInfoVos:
                        itemId = productInfoVo.get('itemId')
                        taskToken = productInfoVo.get('taskToken')
                        skuName = productInfoVo.get('skuName')
                        status = productInfoVo.get('status')
                        if status == 1:
                            print('开始加购“%s”' % skuName)
                            ress = guangdian(
                                taskId, taskToken, itemId, headers,1)
                            times = ress.get('data').get('result').get('times')
                            if times == 4:
                                break
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
                if taskId in [4]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    browseShopVos = getFeedDetail1(taskId, headers)
                    for browseShopVo in browseShopVos:
                        itemId = browseShopVo.get('itemId')
                        taskToken = browseShopVo.get('taskToken')
                        status = browseShopVo.get('status')
                        shopName = browseShopVo.get('shopName')
                        if status == 1:
                            print('开始逛“%s”' % shopName)
                            ress = guangdian(
                                taskId, taskToken, itemId, headers,1)
                            times = ress.get('data').get('result').get('times')
                            if times == 5:
                                break
                            print('等待%s秒' % sleep_times)
                            time.sleep(sleep_times)
                # 逛店
                if taskId in [28, 61]:
                    print(f'>>>>>>[{get_user_name(headers)}]开始进行{taskTitle}任务')
                    taskToken = simpleRecordInfoVos.get('taskToken')
                    itemId = simpleRecordInfoVos.get('itemId')
                    guangdian(taskId, taskToken, itemId, headers,1)
                    print('等待%s秒' % (waitDuration + sleep_times))
                    time.sleep(int(waitDuration + sleep_times))
                    guangdian(taskId, taskToken, itemId, headers,'')
                if taskId == 5:
                    taskToken = i.get('simpleRecordInfoVo').get('taskToken')
                    ii = 0
                    while ii <= 4:
                        ress = guangdian(5, taskToken, '', headers,1)
                        ii += 1
                        time.sleep(sleep_times)

            if status == 2:
                print(taskTitle + '任务已完成')
        lotteryTaskVos = task_list(headers, data).get('lotteryTaskVos')
        if lotteryTaskVos is None:
            return
        badge_task_list = lotteryTaskVos[0].get("badgeAwardVos")
        for task in badge_task_list:
            if task.get('status') != 3:
                continue
            awardVo = getBadgeWard(task.get("awardToken"), headers)
            print(f"完成获取任务次数奖励：{awardVo.get('pointVo').get('score')}")
            print('等待%s秒' % (sleep_times))
    except Exception as e:
        print(e)

# 助力
def jd_zhuli(inviteId, headers):
    ss = get_log()
    url = 'https://api.m.jd.com/client.action?functionId=promote_collectScore'
    body = {
        "actionType": 0,
        "inviteId": "%s" % inviteId,
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body)
    data = 'functionId=promote_collectScore&client=m&clientVersion=-1&appid=signed_wh5&body=%s' % bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('助力成功')
        else:
            msg = res.get('data').get('bizMsg')
            print(msg)
            if '不需要助力' in msg:
                return True
    except Exception as ex:
        print('助力错误：' + str(ex))
    return False

#提升等级
def raise_level(headers):
    ss = get_log()
    url = 'https://api.m.jd.com/client.action?functionId=promote_raise'
    body = {
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body)
    data = 'functionId=promote_raise&client=m&clientVersion=-1&appid=signed_wh5&body=%s' % bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('提升等级成功')
            return True
        else:
            print(res.get('data').get('bizMsg'))
    except Exception as ex:
        print('提升等级错误：' + str(ex))
    return False

#签到
def sign_today(headers):
    ss = get_log()
    url = 'https://api.m.jd.com/client.action?functionId=promote_sign'
    body = {
        "scenceId": 3,
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body)
    data = 'functionId=promote_sign&client=m&clientVersion=-1&appid=signed_wh5&body=%s' % bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('签到成功，获得金币' + res.get('data').get('result').get("scoreResult").get("score"))
            return res
        else:
            print(res.get('data').get('bizMsg'))
    except Exception as ex:
        print('签到错误：' + str(ex))

#分享
def get_welfare_score(headers):
    ss = get_log()
    url = 'https://api.m.jd.com/client.action?functionId=promote_getWelfareScore'
    body = {
        "type": 1,
        "scenceId": 3,
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body)
    data = 'functionId=promote_getWelfareScore&client=m&clientVersion=-1&appid=signed_wh5&body=%s' % bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('分享成功，获得金币' + res.get('data').get('result').get("score"))
            return False
        else:
            print(res.get('data').get('bizMsg'))
            return True
    except Exception as ex:
        print('分享错误：' + str(ex))

#收集金币
def collect_auto_score(headers):
    ss = get_log()
    url = 'https://api.m.jd.com/client.action?functionId=promote_collectAutoScore'
    body = {
        "random": ss["random"],
        "log": ss["log"]
    }
    bodys = json.dumps(body)
    data = 'functionId=promote_collectAutoScore&client=m&clientVersion=-1&appid=signed_wh5&body=%s' % bodys
    try:
        res = requests.post(url, headers=headers, data=data,
                            verify=False, timeout=5).json()
        if res.get('data').get('bizCode') == 0:
            print('收集金币成功，获得金币' + res.get('data').get('result').get("produceScore"))
            return False
        else:
            print(res.get('data').get('bizMsg'))
            return True
    except Exception as ex:
        print('收集金币错误：' + str(ex))

def get_log():
    # url = 'http://127.0.0.1:5883/log'
    # try:
    #     res = requests.get(url, verify=False, timeout=10).json()
    #     return res
    # except Exception as ex:
    #     print('获取log错误：' + str(ex))
    return {
        'log': '1672029492839~161OYW6LXm4MDFKT1ZCbjAxMQ==.e3lhcF54dmJ1W3h/YjxXEn0hDDR4Dm4yEHtjFW4tZn0ocxB7MScBOGcVZXoHKQdhKFYwdyUNDCx8ZCYvNHx6cRA=.76540934~C,2~8552EE68AD7B0658A8BFC2526288958E6933BA0343066E274030D149DF4FA0F4~0e3k69u~C~QxcRXkcJOW8cQEFeVRJfaz4dQFMXXBICB0kRFkBACBJTAwcKAFcJVwZXDVECAwkCXRFJERVXVEAPEkxEEUQXVxdSRx4ST1AEEV8RBFREA0FETVEEEk8TElALEApjBFEfUB9TAxxVGQEUATgcQVsIFl8DHBpWFhFfEQdQBFdUAQ4CB1ZVBVBQAAoJXgMAVVFSUQAGVVMGDABWEk8TDERHCBJ0XAtGHRMDQF0UAlwaHEdEQQtTAlIAAAoMUQpXC1ELHEBfWxoKRx1TAQZWVQIBDQAEUF0eAQICAQ1RAQABBFRXBAMDBB0IUFNRUQdSUAMHUQQKBlNSAQdRVwAGVQ8HUAFUUVVRBlpQBQ8FRxxBVxJWRwgSSXYzHj8AWltTKgJaAEpdQyxTBAdXVnEaGUddExFYEHcNWldUVUV5DVJMFkkQXllDRwlHClUKCVAXHBpDBkJBCzkCUQIcCwNVbkkREF0SWG4Sbn8iHSJ9UgRHHhJZWwFBCloGEBxADBIUElQBTQFMAEceEgECXQpXEU4QA1QFAwoDVgZbAlMCXAEACxhRBVEAVQEGVAMGDwNTBlUCQBhHAxJlGUdaClJACBIEU1ZeVgNEFxNOFgRYEgIXEBFJEQFbElgXRwweVR5WE04WBlRvThdfEVUCQB4SAFESAhIXUQ1VDVlYQWdffQRAFX5AHhIPXxICa1UcUx1SaUkQUlRaAhFfEVMEB1AFAgEEUgRVAlRKVEFGVHQmWSBQFQd9Jn9aWmgjQjpbI00oVQ0FGzBfEXQ1ZHowY3V6YzMBB1czTDABZm4NI3YNYhhiACBUeHpmJ3NTVStgVEVgYGcdYCBEK0p0NGxed1kdYChwL1EhS31PYg1YTnUmQQckYXlBeyYEJ3QYdV1xSnVBIGUGeDNwWxt2Vwx1NWQuASpeUXR3CWxKeyd6I3xZK0V5eX09dlNoJ2EnfGZ5ZBJDNXA4d3sxQnZ7WD9qIncjATRgdm9jEmIKezZnYzpwdVl3J2k5fAV5HXRIT2MhcRFmLXAIBHBzYQcjcwB9I1hVd39scB9kD0MEfHYnWmJRAQR1D15NcR1jQHlNN1EgclZ3fA57Z3NzXUAiVg5nL2FDc3khXAZ4FVkHLndTfnUOCDZ1Jn0UdnJxfSNaPFAqYw1fGwYABgRSBgkEShweAUZLG3EbYCB8ciR0V29lVAkFeSR2BmR1fmwyXyRXOl56Km12XFIzdSZ3J3YCYWVqdCx2HXIBd2YzZ3RQdjF1MQUzYlRkRWpnNHojVCNxdSABZGpYLHolYAF3JHNhan0NcQFiMH96JHR5YXE3eQZ0JEwmd1dTYyREMHcjWnUHcHZcUSBHCGQ3ZQZXcVBCJHZVC19MABtTREleDBJPEw9HAhAKGhdJER1QEBAKQAUBREgTTFNeDQcAHEQWAw0dD0YWQlcPDVQAUxRTEBMf~025phdi',
        'random': 'sWgHaspM'
    }


def main_task(cookie):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'jdapp;android;11.0.4;;;appBuild/97892;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1666964882727%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22EG%3D%3D%22%2C%22ad%22%3A%22YzKyYzrrEJLuDNdwZtdwDq%3D%3D%22%2C%22od%22%3A%22%22%2C%22ov%22%3A%22Ctq%3D%22%2C%22ud%22%3A%22YzKyYzrrEJLuDNdwZtdwDq%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 9; TAS-AN00 Build/PQ3B.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046140 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://wbbny.m.jd.com',
        'Referer': 'https://wbbny.m.jd.com/',
        'Cookie': cookie
    }
    #joyToken = get_joytoken(headers)
    # cookie = cookie + ' __jdc=;  shshshfpb=iCYzgMuPxd0lWT0bD25ss3Q; shshshfpa=00eb2646-19ae-5a5f-6961-5aa1d5165af7-1659626436; __jdv=;   __jda=; shshshfp=16fb74bbcbfe6ac2788d637d0d8e3534; shshshsID=546a21f1fed27153f08f2ef39332bd2f_3_1666965134257; __jdb=; shshshfpv=; mba_sid=; joyytokem=; joyya=; mba_muid='
    headers['Cookie'] = cookie
    i = 0
    print(f'>>>>>>[{get_user_name(headers)}]开始进行任务')
    collect_auto_score(headers)
    sign_today(headers)
    time.sleep(sleep_times)
    for t in range(10):
        exit = get_welfare_score(headers)
        time.sleep(sleep_times)
        if exit:
            break
    # while i < task_times:
    #     # 京东app任务
    #     jddata = 'functionId=promote_getTaskDetail&client=m&clientVersion=-1&appid=signed_wh5&body={"appSign":1,"taskId":""}'
    #     vxtask_list(headers, jddata)
    #     i += 1

    if auto_raise_level:
        result = raise_level(headers)
        while result:
            time.sleep(sleep_times)
            result = raise_level(headers)
    
    if help_author:
        global inviteIds
        new_inviteIds = []
        for inviteId in inviteIds:
            full_count = jd_zhuli(inviteId, headers)
            if not full_count:
                new_inviteIds.append(inviteId)
            time.sleep(sleep_times)
        inviteIds = new_inviteIds
    


if __name__ == '__main__':

    threads = []
    for cookie in cookies:
        # thread = Thread(target=main_task, args=(cookie, ))
        # thread.start()
        # threads.append(thread)
        main_task(cookie)

    for t in threads:
        t.join()

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
