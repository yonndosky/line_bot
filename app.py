import os,bs4,requests
from datetime import datetime,timezone,timedelta
from flask import Flask, request, abort ,render_template
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
app = Flask(__name__)
line_bot_api = LineBotApi("Token")
handler = WebhookHandler("Channel Secret")
@ app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']# get X-Line-Signature header value
    body = request.get_data(as_text=True)# get request body as text
    app.logger.info("Request body: " + body)  
    try:handler.handle(body, signature)# handle webhook body
    except InvalidSignatureError:abort(400)
    return 'OK'

@app.route("/")
def home():
    return render_template("home.html")
    
class UserInfo:
    def __init__(self,_name ,_uid, _level):
        self._name = _name
        self._uid = _uid
        self._level = _level  

a = UserInfo('a',"Uad9677ff7bae6883b4a778b2c7f5a524",2)
c = UserInfo('c',"U592b42c3b3c662a0939c8939e36533aa",0)
b = UserInfo('b',"U6feeaee239e98050d96c99af905d4ba1",1)

control_centerID = "C5321cc529d55f1c8a05459818ecddd9a"
room_zh_ys = "C8436763c6ca9b05c41950b4918a35c4b"

members=[c,b,a]

@ handler.add(FollowEvent) 
def getMessage_Follow(event):
    _msg = '【事件】新追蹤\n【UID】'+event.source.user_id+'\n【名字】'+str(line_bot_api.get_profile(event.source.user_id).display_name)
    line_bot_api.push_message(event.source.group_id, TextSendMessage(text='您好，第一次見面請多多指教^^'))
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)  

@ handler.add(UnfollowEvent)
def getMessage_Unfollow(event):
    _msg = '【事件】退追蹤\n【UID】:'+event.source.user_id+'\n【名字】:'+str(line_bot_api.get_profile(event.source.user_id).display_name)
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)

@ handler.add(JoinEvent)
def getMessage_JoinTeam(event):
    _msg = '【事件】加入群組\n【群組ID】'+event.source.group_id+'\n【群組名稱】'+line_bot_api.get_group_summary(event.source.group_id).group_name+'\n【群組屬性】'+event.source.type
    line_bot_api.push_message(event.source.group_id, TextSendMessage(text='大家好，第一次見面請多多指教^^'))
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)

@ handler.add(LeaveEvent)
def getMessage_LeaveTeam(event):
    _msg= '【事件】退出群組\n【群組ID】'+event.source.group_id+'\n【群組名稱】'+'\n【群組屬性】'+event.source.type
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)

@ handler.add(MemberJoinedEvent)
def getMessage_MemberLeaveTeam(event):
    _msg= '【事件】成員加入群組\n【UID】'+str(event.joined.members)+'\n【群組ID】'+event.source.group_id+'\n【群組名稱】'+line_bot_api.get_group_summary(event.source.group_id).group_name+'\n【群組屬性】'+event.source.type
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)

@ handler.add(MemberLeftEvent)
def getMessage_MemberLeaveTeam(event):
    _msg= '【事件】成員退出群組\n【UID】'+str(event.left.members)+'\n【群組ID】'+event.source.group_id+'\n【群組名稱】'+line_bot_api.get_group_summary(event.source.group_id).group_name+'\n【群組屬性】'+event.source.type
    line_bot_api.push_message(control_centerID,TextSendMessage(text=_msg),notification_disabled=True)

@ handler.add(MessageEvent, message=(TextMessage))# 處理訊息
def handle_message(event):
    userLevel = 999
    msg = event.message.text
    msg = msg.encode('utf-8')
    msg = []
    
    locationsInfo = [
        ['https://upload.wikimedia.org/wikipedia/commons/e/ea/%E5%8F%B0%E5%8C%97101%E3%80%8C%E9%BE%8D%E8%BA%8D%E9%9B%B2%E7%AB%AF%E3%80%8D%E5%99%B4%E6%B3%89.JPG','北部','激戦区',['臺北市','新北市','基隆市']],
        ['https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Washington_Dulles_International_Airport_at_Dusk.jpg/2560px-Washington_Dulles_International_Airport_at_Dusk.jpg','中部','夢の起源',['桃園市/新竹市','臺中市/彰化縣','南投縣/苗栗縣']],
        ['https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Kaohsiung_Taiwan_Ship-En-Cheng-01.jpg/2560px-Kaohsiung_Taiwan_Ship-En-Cheng-01.jpg','南部','鄉下',['嘉義市','臺南市','高雄市/屏東縣']],
        ['https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Taiwan_2009_HuaLien_Taroko_Gorge_Biking_PB160057.jpg/1024px-Taiwan_2009_HuaLien_Taroko_Gorge_Biking_PB160057.jpg','東部','好山好水好無聊',['宜蘭縣','花蓮縣','臺東縣']],
        ['https://upload.wikimedia.org/wikipedia/commons/0/05/Ching-tien_Hall_front.jpg','外島','海軍陸戰隊簽了吧',['澎湖縣','金門縣','連江縣']]
        ]  
    def getListenning():
        global groupName,groupID,roomID,userID,picture,message 
        groupName,groupID,roomID,userID = '不在群組內','無','不在房間內','不為使用者'
        if(event.source.type == 'room'):
            roomID,userID = event.source.room_id,event.source.user_id
            picture = line_bot_api.get_group_summary('C11656c51794c19e183262b6155f2e2c4').picture_url
            message='A message form:'+str(line_bot_api.get_room_member_profile(roomID, userID).display_name)+'From:Room'
            print('【Type】'+str(event.source.type)+'【UserID】'+str(userID)+'【RoomID】'+str(roomID)+'\n【UserName】'+str(line_bot_api.get_room_member_profile(roomID, userID).display_name)+'【Message】'+str(event.message.text))
        elif(event.source.type == 'group'):
            groupID,userID = event.source.group_id,event.source.user_id
            groupName = line_bot_api.get_group_summary(groupID).group_name
            picture = line_bot_api.get_group_summary(groupID).picture_url
            message='A message form:'+str(line_bot_api.get_group_member_profile(groupID, userID).display_name)+'GroupFrom:'+groupName
            print('【Type】'+str(event.source.type)+'【UserID】'+str(userID)+'【GroupID】'+str(groupID)+'\n【UserName】'+str(line_bot_api.get_group_member_profile(groupID, userID).display_name)+'【Message】'+str(event.message.text)+'【GroupName】'+str(groupName))
        else:
            userID = event.source.user_id
            picture=line_bot_api.get_profile(event.source.user_id).picture_url
            message='A message form:'+str(line_bot_api.get_profile(event.source.user_id).display_name)
            print('【Type】'+str(event.source.type)+'【UserID】:'+str(userID)+'\n【UserName】'+str(line_bot_api.get_profile(event.source.user_id).display_name)+'【Message】'+str(event.message.text))       
        getIgnoreList(userID,groupID,roomID,picture,message)
              
    def getWeather(key):
        weathers=[]
        weatherUpdateTime=''
        answer=''
        url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-DAB53FF9-9641-4BAC-967D-5A0C704716CC&downloadType=WEB&format=JSON"
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
            weathers.append(f'*{city}* 未來 8 小時{wx8}，\n最高溫 {maxt8} 度，\n最低溫 {mint8} 度，\n舒適度為 {ci8} ，\n降雨機率 {pop8} %')
        match key:
            case 0:answer = f'更新時間:{weatherUpdateTime}\n{weathers[key]}'
            case 1:answer = f'更新時間:{weatherUpdateTime}\n{weathers[key]}'
            case 2:answer = f'更新時間:{weatherUpdateTime}\n{weathers[6]}'
            case 3:answer = f'更新時間:{weatherUpdateTime}\n{weathers[2]}\n\n{weathers[8]}'
            case 4:answer = f'更新時間:{weatherUpdateTime}\n{weathers[3]}\n\n{weathers[10]}'
            case 5:answer = f'更新時間:{weatherUpdateTime}\n{weathers[11]}\n\n{weathers[9]}'
            case 6:answer = f'更新時間:{weatherUpdateTime}\n{weathers[14]}'
            case 7:answer = f'更新時間:{weatherUpdateTime}\n{weathers[4]}'
            case 8:answer = f'更新時間:{weatherUpdateTime}\n{weathers[5]}\n\n{weathers[15]}'
            case 9:answer = f'更新時間:{weatherUpdateTime}\n{weathers[16]}'
            case 10:answer = f'更新時間:{weatherUpdateTime}\n{weathers[17]}'
            case 11:answer = f'更新時間:{weatherUpdateTime}\n{weathers[18]}'
            case 12:answer = f'更新時間:{weatherUpdateTime}\n{weathers[19]}'
            case 13:answer = f'更新時間:{weatherUpdateTime}\n{weathers[20]}'
            case 14:answer = f'更新時間:{weatherUpdateTime}\n{weathers[21]}'
        return answer
    def getUserLevel():
        answer =''
        if userLevel <=10:
            answer = f'{userLevel}'
        else:
            answer = '無'
        return answer
    def getIgnoreList(UID,GID,RID,PIC,MSG):
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url=PIC,
                image_aspect_ratio='rectangle',
                image_size='contain',
                image_background_color='#FFFFFF',
                title=MSG,
                text=event.message.text,
                actions=[
                    PostbackAction(label='Group ID',display_text=GID,data='action=buy&itemid=1',),
                    PostbackAction(label='Room ID',display_text=RID,data='action=buy&itemid=2',),
                    PostbackAction(label='Account ID',display_text=UID,data='action=buy&itemid=3',),
                    ]
                )
            )
        if UID == c._uid:print('___') 
        elif GID == 'C99dcbd1770b1dbd13de9696badf863fc':print('__________') 
        else:line_bot_api.push_message(control_centerID,buttons_template_message,notification_disabled=True) 


    getListenning()
    
    isUnknown = True
    userID = event.source.user_id
    for menber in members:
        if isUnknown:
            if userID in menber._uid:
                userLevel = menber._level
                isUnknown =False
                break
            else: userLevel =147896325

    if userLevel <1:
        if "reply." in event.message.text:
            replyemessage = event.message.text.split(".", 2)
            returnmessage,member = replyemessage[1],replyemessage[2]
            line_bot_api.push_message(member, TextSendMessage(text=returnmessage))
        elif "leavegroup." in event.message.text:
            leavemessage = event.message.text.split(".", 1)  
            leavegroupid = (leavemessage[1]) 
            try:
                groupName = line_bot_api.get_group_summary(leavegroupid).group_name
                line_bot_api.leave_group(str(leavegroupid))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已退出'+groupName+'。'))
            except:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='退出失敗'))       
    if userLevel <=3:
        if event.message.text == "衛星雲圖":
            timeget = datetime.utcnow().replace(tzinfo=timezone.utc)
            now = timeget.astimezone(timezone(timedelta(hours=8))) 
            time_min = '30' if int(now.strftime("%M")) >= 30 else '00'
            picurl ='https://static.tenki.jp/static-images/satellite/'+now.strftime("%Y")+'/'+now.strftime("%m")+'/'+now.strftime("%d")+'/'+now.strftime("%H")+'/'+time_min+'/00/japan-near-large.jpg'
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=picurl,preview_image_url=picurl))
        elif event.message.text == "てんき：臺北市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(0)))
        elif event.message.text == "てんき：新北市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(1)))
        elif event.message.text == "てんき：基隆市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(2)))
        elif event.message.text == "てんき：桃園市/新竹市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(3)))
        elif event.message.text == "てんき：臺中市/彰化縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(4)))
        elif event.message.text == "てんき：南投縣/苗栗縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(5)))
        elif event.message.text == "てんき：嘉義市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(6)))
        elif event.message.text == "てんき：臺南市":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(7)))
        elif event.message.text == "てんき：高雄市/屏東縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(8)))
        elif event.message.text == "てんき：宜蘭縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(9)))
        elif event.message.text == "てんき：花蓮縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(10)))
        elif event.message.text == "てんき：臺東縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(11)))
        elif event.message.text == "てんき：澎湖縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(12)))
        elif event.message.text == "てんき：金門縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(13)))
        elif event.message.text == "てんき：連江縣":line_bot_api.reply_message(event.reply_token, TextSendMessage(text = getWeather(14)))
        elif "天氣" in event.message.text:  
            line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
                alt_text='Carousel template',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=locationsInfo[0][0],
                            title=locationsInfo[0][1],
                            text=str(locationsInfo[0][2]),
                            actions=[
                                MessageTemplateAction(label=locationsInfo[0][3][0],text=f'てんき：{locationsInfo[0][3][0]}'),
                                MessageTemplateAction(label=locationsInfo[0][3][1],text=f'てんき：{locationsInfo[0][3][1]}'),
                                MessageTemplateAction(label=locationsInfo[0][3][2],text=f'てんき：{locationsInfo[0][3][2]}'),
                                ] 
                            ),
                            CarouselColumn(
                                thumbnail_image_url=locationsInfo[1][0],
                                title=locationsInfo[1][1],
                                text=str(locationsInfo[1][2]),
                                actions=[
                                    MessageTemplateAction(label=locationsInfo[1][3][0],text=f'てんき：{locationsInfo[1][3][0]}'),
                                    MessageTemplateAction(label=locationsInfo[1][3][1],text=f'てんき：{locationsInfo[1][3][1]}'),
                                    MessageTemplateAction(label=locationsInfo[1][3][2],text=f'てんき：{locationsInfo[1][3][2]}'),
                                ] 
                            ),
                            CarouselColumn(
                                thumbnail_image_url=locationsInfo[2][0],
                                title=locationsInfo[2][1],
                                text=str(locationsInfo[2][2]),
                                actions=[
                                    MessageTemplateAction(label=locationsInfo[2][3][0],text=f'てんき：{locationsInfo[2][3][0]}'),
                                    MessageTemplateAction(label=locationsInfo[2][3][1],text=f'てんき：{locationsInfo[2][3][1]}'),
                                    MessageTemplateAction(label=locationsInfo[2][3][2],text=f'てんき：{locationsInfo[2][3][2]}'),
                                ] 
                            ),
                            CarouselColumn(
                                thumbnail_image_url=locationsInfo[3][0],
                                title=locationsInfo[3][1],
                                text=str(locationsInfo[3][2]),
                                actions=[
                                    MessageTemplateAction(label=locationsInfo[3][3][0],text=f'てんき：{locationsInfo[3][3][0]}'),
                                    MessageTemplateAction(label=locationsInfo[3][3][1],text=f'てんき：{locationsInfo[3][3][1]}'),
                                    MessageTemplateAction(label=locationsInfo[3][3][2],text=f'てんき：{locationsInfo[3][3][2]}'),
                                ] 
                            ),
                            CarouselColumn(
                                thumbnail_image_url=locationsInfo[4][0],
                                title=locationsInfo[4][1],
                                text=str(locationsInfo[4][2]),
                                actions=[
                                    MessageTemplateAction(label=locationsInfo[4][3][0],text=f'てんき：{locationsInfo[4][3][0]}'),
                                    MessageTemplateAction(label=locationsInfo[4][3][1],text=f'てんき：{locationsInfo[4][3][1]}'),
                                    MessageTemplateAction(label=locationsInfo[4][3][2],text=f'てんき：{locationsInfo[4][3][2]}'),
                                ] 
                            ),
                        ]
                    )
                )
            )
    if userLevel >=0:
        if event.message.text == "個人資訊" and roomID == '不在房間內' and groupID == '無':
            replylist = []
            replylist.append(TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url = line_bot_api.get_profile(userID).picture_url,
                        title = f'名字:{line_bot_api.get_profile(userID).display_name}',
                        text=f'使用的語言:{line_bot_api.get_profile(userID).language}\n個人簡介:{line_bot_api.get_profile(userID).status_message}\n階級:{getUserLevel()}',
                        actions=[
                            MessageTemplateAction(label='取得身分字號',text='身分字號'),
                            ]
                        )
                    )
                )
            line_bot_api.reply_message(event.reply_token,replylist) 
        elif event.message.text == '身分字號':line_bot_api.reply_message(event.reply_token, TextSendMessage(text = f'{line_bot_api.get_profile(userID).user_id}'))
    if not msg:# error handl...
        return
    line_bot_api.reply_message(event.reply_token, messages=msg[:5])
    return 'OK2'
#=============================================================#
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
