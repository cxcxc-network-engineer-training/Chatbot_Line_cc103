
# coding: utf-8

# In[ ]:


#跟app.ipynb差在ip使用方式，跟檔案使用絕對路徑


# In[1]:


# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)
from urllib.parse import urlparse,parse_qs

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, MessageAction,ButtonsTemplate, URIAction,
    PostbackAction, DatetimePickerAction,PostbackEvent,
    FollowEvent,ButtonComponent,QuickReply, QuickReplyButton
)
from linebot.models import (
    MessageEvent, PostbackEvent, 
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction, 
)


# In[2]:


"""

    針對跟redis的連線

"""

import redis

#製作redis連線
redis = redis.Redis(
    #redis container的host name
    host='redis',
    port=6379,
    #預設沒密碼，成功之後設密碼
    password=None,
    #給格式
    charset="utf-8",
    #要解碼不然回傳的資料前面會多一個b
    decode_responses=True)

import os 

ip_location=os.environ.get('IPA_ENV')


# In[3]:


"""

    抓secret_key裡面的資料

"""
# 載入json處理套件
import json

# 載入基礎設定檔
secretFile=json.load(open("/home/jovyan/work/secret_key",'r'))
server_url=secretFile.get("server_url")


# channel_access_token是用於傳送封包去給line的認證使用類似這個是私鑰，而公鑰已經丟到line那邊，拿著這個就可以有VIP特權
# secret_key是用於當line傳送封包過來時確定line是否為本尊，沒有被仿冒
line_bot_api = LineBotApi(secretFile.get("channel_access_token"))
handler = WebhookHandler(secretFile.get("secret_key"))
menu_id = secretFile.get("rich_menu_id")


# In[4]:


'''

製作文字與圖片的教學訊息

'''
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# 消息清單
reply_message_list = [
TextSendMessage(text="CC103-Line考古題機器人。\n請按功能選單進行測驗")
]
    


# In[5]:


"""

  啟用伺服器基本樣板啟用伺服器基本 

"""

# 引用Web Server套件
from flask import Flask, request, abort , jsonify



# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)


# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "/home/jovyan/work/images/")


# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# In[6]:


'''

撰寫用戶關注事件發生時的動作

1. 取得用戶個資，並存回伺服器
2. 把先前製作好的自定義菜單，與用戶做綁定
3. 回應用戶，歡迎用的文字消息與圖片消息
4. 製作用戶的redis資料

'''


# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    ################### 須作例外處理
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
    # 將用戶資訊做成合適Json

    user_info = {  
        "user_open_id":user_profile.user_id,
        "user_nick_name":user_profile.display_name,
        "user_status" : "",
        "user_img" : user_profile.picture_url,
        "user_register_menu" : menu_id
    }
    #將json傳回API Server
    Endpoint='http://%s:5001/users' % (ip_location)
    #Endpoint='http://%s:5001/users' % (ip_location)   
    Header={'Content-Type':'application/json'}
    Response=requests.post(Endpoint,headers=Header,data=json.dumps(user_info))
    
    # 先暫時寫的，用來檢查錯誤情形，方便除錯
    print(Response)
    print(Response.text)
    
    # 將菜單綁定在用戶身上
    
    linkMenuEndpoint='https://api.line.me/v2/bot/user/%s/richmenu/%s' % (user_profile.user_id, menu_id)
    linkMenuRequestHeader={'Content-Type':'image/jpeg','Authorization':'Bearer %s' % secretFile["channel_access_token"]}
    lineLinkMenuResponse=requests.post(linkMenuEndpoint,headers=linkMenuRequestHeader)
    print(lineLinkMenuResponse)
    print(lineLinkMenuResponse.text)
    
    # 回覆文字消息與圖片消息
    line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text="請使用下方功能選單\n或是輸入下方字串\ndetail")
    )
    
    #再跟老師討論存在redis的值有沒有需要進去mysql
    redis.hmset(user_profile.user_id, {'result': 0,"total" : 0,"sa_qid" : 0,"dev_qid" : 0,"sys_qid" : 0})
    
    
    


# In[7]:


#寫一個函式是看正解給result使用
def true_answer(a,answer):
    if a['true_answer']==answer:
        return 'True'
    else:
        return 'False'


# In[9]:


"""

    使用客製化question id跟題庫拿資料並回傳
    並回傳quick reply 包含postback action 
    內裝data方便後續動作

"""
#做一個回傳考題的函式，擷取變數（考題類別,使用者id,考題id）
def test(questiontype,user_id,questionid):
    #由於只有100題，所以超過之後回傳一個訊息
    if (questionid==101):
        #並將它歸零
        redis.hset(user_id,questionid,0)
        #回覆訊息
        reply_message_list = [
        TextSendMessage(text="Congratulation!!!!\nYou already finish 100 question about %s" % (questiontype)),
        ]
        return reply_message_list
    #api server接口位置
    a = answer(questiontype,questionid)
    #這邊使用quick reply的方式
    quickreply = TextSendMessage(
                text='Choose your answer:',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            #使用postback action類似按鈕的概念
                            action=PostbackAction(label="A",
                                                  #這邊使用true_answer()來幫助result
                                                  data="type=answer&question_type=%s&question_id=%s&result=%s" % (questiontype,questionid,true_answer(a,'A')),
                                                  text='choose:A'
                                                 )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="B",
                                                  data="type=answer&question_type=%s&question_id=%s&result=%s" % (questiontype,a['question_id'],true_answer(a,'B')),
                                                  text='choose:B'
    
                                                 )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="C",
                                                  data="type=answer&question_type=%s&question_id=%s&result=%s" % (questiontype,a['question_id'],true_answer(a,'C')),
                                                  text='choose:C'
                                                 )
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="D",
                                                  data="type=answer&question_type=%s&question_id=%s&result=%s" % (questiontype,a['question_id'],true_answer(a,'D')),
                                                  text='choose:D'
                                                 )
                        )
                    ]))
    #全部回傳的list
    reply_message_list = [
        TextSendMessage(text=a["question_content"]),
        TextSendMessage(text=a["answer1_content"]+"\n\n"+a["answer2_content"]+"\n\n"+a["answer3_content"]+"\n\n"+a["answer4_content"]),
        #回傳quick reply選單
        quickreply    
    ]
    return reply_message_list


# In[10]:


"""

    比對答覆跟正解

"""
def answer(qtype,qid):
    url =  "http://%s:5001/question/%s" % (ip_location,qtype)
    #url =  "http://%s:5001/question/%s" % (ip_location,qtype)
    #裝query string的部份
    payload = {'question_id' : qid}
    #傳送封包
    a = requests.get(url,params=payload)
    #將回傳結果取出
    a=a.json()
    return a


# In[11]:


def result(questiontype,data,user_profile):
    #去API取得考題資訊
    a = answer(questiontype,data['question_id'][0])
    #預設為錯誤的reply
    reply = "Error\nAns:%s" %a["true_answer"]
    #假如正確的話回一個正確的reply
    if (data['result']==['True']):
    #每答對一題，redis的result增加一
        redis.hincrby(user_profile,"result") 
        reply = 'Correct!!'
    #製作一個回覆list
    reply_message_list = [
        TextSendMessage(text=reply),
        TextSendMessage(text=a["true_answer_decribe_content"]+"\n\n"),
        TextSendMessage(text=a["external_link"])
        ]
    #進行回覆
    
    return reply_message_list


# In[12]:


"""
    
    收到按鈕（postback）的封包後
    1. 先看是哪種按鈕（question(考試),answer(答覆)）
    2. 看是哪種類別（sa,sysops,develop）
    3. 執行所需動作
    4. 回覆訊息

"""

#用戶點擊button後，觸發postback event，對其回傳做相對應處理
@handler.add(PostbackEvent)
def handle_post_message(event):
    #抓取user資料
    user_profile = event.source.user_id
    #抓取postback action的data
    data = event.postback.data
    #用query string 解析data
    data=parse_qs(data)
    #出考題
    if (data['type']==['question']):
        #每要求出題後，redis 的total增加一
        redis.hincrby(user_profile,"total")
        if (data['question_type']==['sysops']):
            #每次出一題sysops增加一個sys_qid
            redis.hincrby(user_profile,"sys_qid")
            #從redis擷取出來
            questionid = redis.hget(user_profile,"sys_qid")
            #回覆一組回覆串
            line_bot_api.reply_message(
            event.reply_token,
            test('sysops',user_profile,questionid))
        elif (data['question_type']==['develop']):
            redis.hincrby(user_profile,"dev_qid")
            questionid = redis.hget(user_profile,"dev_qid")
            line_bot_api.reply_message(
            event.reply_token,
            test('devlop',user_profile,questionid))
        elif (data['question_type']==['sa']):
            redis.hincrby(user_profile,"sa_qid")
            questionid = redis.hget(user_profile,"sa_qid")
            line_bot_api.reply_message(
            event.reply_token,
            test('sa',user_profile,questionid))
    #給按了答案的回覆
    elif (data['type']==['answer']):
        if (data['question_type']==['sysops']):
            #進行回覆
            line_bot_api.reply_message(
                event.reply_token,
                result('sysops',data,user_profile)
            )
        elif (data['question_type']==['devlop']):
            #進行回覆
            line_bot_api.reply_message(
                event.reply_token,
                result('devlop',data,user_profile)
            )
        elif (data['question_type']==['sa']):
            line_bot_api.reply_message(
                event.reply_token,
                result('sa',data,user_profile)
            )
      
    else:
        pass


# In[13]:


'''

    當用戶發出文字消息時，判斷文字內容是否包含一些關鍵，
    若有，則回傳客製化訊息
    若無，則回傳預設訊息。

'''

# 用戶發出文字消息時， 按條件內容, 回傳文字消息
@handler.add(MessageEvent, message=TextMessage)
#將這次event的參數抓進來
def handle_message(event):
    user_profile = event.source.user_id
    if (event.message.text.find('choose:')!= -1):
        pass
    elif (event.message.text.find('detail')!= -1):
        sa_qid = redis.hget(user_profile,"sa_qid")
        sys_qid = redis.hget(user_profile,"sys_qid")
        dev_qid = redis.hget(user_profile,"dev_qid")
        #總答對題數
        correct = redis.hget(user_profile,"result")
        #總回答題數
        total = redis.hget(user_profile,"total")
        reply_list = [
            TextSendMessage(text="各類回答紀錄\nsa:%s/100\ndeveloper:%s/100\nsysops:%s/100" % (sa_qid,sys_qid,dev_qid) ),
            TextSendMessage(text="總共答對 (%s)題\n總共回答 (%s)題" % (correct,total))
        ]
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )
        
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請使用下方功能選單\n或是輸入下方字串\ndetail"))


# In[ ]:


'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

