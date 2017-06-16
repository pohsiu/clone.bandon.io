# coding=UTF8
from django.shortcuts import render

from bandongo.models import Member
# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# TODO: Define Receiver



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    print type(event.message.text)
                    inputMsg = event.message.text
                    head = inputMsg[:4]
                    head2 = inputMsg[4:6]
                    compare1 = '我要註冊'.decode('utf-8')
                    compare2 = '我是'.decode('utf-8')
                    if(head == compare1 and  head2 == compare2):
                        combineName = inputMsg[6:len(inputMsg)]
                        allusers = Member.objects.all()
                        lock = False
                        print combineName
                        for each in allusers:
                        	each_combine = each.remark.name+each.name
                        	print each_combine
                        	if(each_combine == combineName):
                        		lock = True
                        		target = Member.objects.get(id=each.id)
                        		target.lineid = str(event.source.user_id)
                        		target.save()
                        		print "成功"
                        		break
                        
                        if(lock is False):
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='註冊失敗，請再次檢查重新輸入')
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='註冊成功，現在可以接收到最新消息囉^^')
                            )
                    else:
                        print "fail"
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )
                    

        return HttpResponse()
    else:
        print("this");
        return HttpResponseBadRequest()