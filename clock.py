from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import urllib.request,datetime
from linebot import LineBotApi
from linebot.models import *

line_bot_api = LineBotApi("Token")
sched = BlockingScheduler(timezone="Asia/Taipei")


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/6')
def scheduled_job():
    print('=====================================================================================================================')
    print('精力消耗中...')
    print(f'{datetime.datetime.now().ctime()}')
    url = "https://shelter0218-1.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)
        
    print('=====================================================================================================================')


class UserInfo:
    def __init__(self,_name ,_uid, _level):
        self._name = _name
        self._uid = _uid
        self._level = _level  

shelterID = "U592b42c3b3c662a0939c8939e36533aa"
control_centerID = "C5321cc529d55f1c8a05459818ecddd9a"

@sched.scheduled_job('cron',  hour=5,minute =0)
def scheduled_job():
    weathers=[]
    weatherUpdateTime=''
    answer=''
    url = "ㄈ/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-DAB53FF9-9641-4BAC-967D-5A0C704716CC&downloadType=WEB&format=JSON"
    data = requests.get(url)   # 取得 JSON 檔案的內容為文字
    data_json = data.json()    # 轉換成 JSON 格式
    location = data_json['cwbopendata']['dataset']['location']
    weatherUpdateTime = f"{data_json['cwbopendata']['sent']}"
    weatherUpdateTime = weatherUpdateTime.split('+')[0]
    for i in location:
        city = i['locationName']    # 縣市名稱
        wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']    # 天氣現象
        mint8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最低溫
        maxt8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最高溫
        ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
        pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率
        weathers.append(f'{wx8}，\n最高溫 {maxt8} 度，\n最低溫 {mint8} 度，\n舒適度為 {ci8} ，\n降雨機率 {pop8} %')
    line_bot_api.push_message(shelterID,TextSendMessage(text=f"現在時間洞五洞洞\n部隊起床!!!\n今日宜蘭天氣為{weathers[16]}\n更新時間:{weatherUpdateTime}，祝各位今日有美好的一天^^"),notification_disabled=True)
    #line_bot_api.push_message(control_centerID,TextSendMessage(text=f"現在時間洞五洞洞\n部隊起床!!!\n今日宜蘭天氣為{weathers[16]}\n更新時間:{weatherUpdateTime}，祝各位今日有美好的一天^^"),notification_disabled=True)
    

sched.start()