import requests
import json

'''
<카카오톡 알림>
'''

# REST API KEY: 9ee8fab55cec81726b12be78e594e3fb
# Redirect URL: https://localhost.com
# Request URL: https://kauth.kakao.com/oauth/authorize?client_id=9ee8fab55cec81726b12be78e594e3fb&redirect_uri=https://localhost.com&response_type=code
# CODE: cHV-sMdRHKor5jFikUP95JB8BUzC0vMEY_yfM1SfZPYBo13lYqa-jB9AAsXDaNXnMLYtRgo9dZsAAAF1760iQA

def setupTalk():
    url = "https://kauth.kakao.com/oauth/token"
    
    data = {
        "grant_type" : "authorization_code",
        "client_id" : "9ee8fab55cec81726b12be78e594e3fb",
        "redirect_uri" : "https://localhost.com",
        "code" : "cHV-sMdRHKor5jFikUP95JB8BUzC0vMEY_yfM1SfZPYBo13lYqa-jB9AAsXDaNXnMLYtRgo9dZsAAAF1760iQA"
    }

    response = requests.post(url, data=data)
    tokens = response.json()

    print(tokens)

    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)

def refreshToken():
    url = "https://kauth.kakao.com/oauth/token"
    app_key = "9ee8fab55cec81726b12be78e594e3fb"
    with open("kakao_token.json", "r") as fp:
        tokens = json.load(fp)

    data = {
        "grant_type" : "refresh_token",
        "client_id" : app_key,
        "refresh_token" : tokens['refresh_token']
    }

    response = requests.post(url, data=data)
    new_tokens = response.json()

    print(new_tokens)

    with open("kakao_token.json", "w") as fp:
        json.dump(new_tokens, fp)

def connectKakaoTalk():
    with open("kakao_token.json", "r") as fp:
        token = json.load(fp)

    return token

def sendResultText(token, text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization" : "Bearer " + token['access_token']
    }

    data = {
        "template_object" : json.dumps({
            "object_type" : "text",
            "text" : text,
            "link" : {
                "web_url" : "https://calendar.google.com",
                "mobile_web_url" : "https://calendar.google.com"
            },
            "button_title" : "구글 캘린더로 보기"
        })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.content)

def sendWarningMessage(token, leave_dic, crystals):
    user = ""

    for crystal in crystals:
        if leave_dic[crystal]["name"] == "여주안":
            user = crystal
    
    if user == "":
        return

    text = "! 당신의 휴가가 위험합니다 !\n"
    text += leave_dic[user]["oristart"][-5:]+"~"+leave_dic[user]["oriend"][-5:]+" 우선순위: "+str(leave_dic[user]["priority"])+"위"

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization" : "Bearer " + token['access_token']
    }
    
    data = {
        "template_object" : json.dumps({
            "object_type" : "feed",
            "content" : {
                "title" : text,
                "description" : "다른 신청자를 매수하거나 후임을 조용히 방으로 부르세요.",
                "image_url" : "https://pds.joins.com/news/component/htmlphoto_mmdata/201808/23/htm_20180823235042256064.jpg",
                "image_width" : 550,
                "image_height" : 387,
                "link" : {
                    "web_url" : "https://calendar.google.com",
                    "mobile_web_url" : "https://calendar.google.com"
                }
            },
            "buttons" : [{
                "title" : "추천 휴가일",
                "link" : {
                    "web_url" : "https://naver.com",
                    "mobile_web_url" : "https://naver.com"
                }
            },{
                "title" : "캘린더 보기",
                "link" : {
                    "web_url" : "https://naver.com",
                    "mobile_web_url" : "https://naver.com"
                }
            }]
        })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.content)

def sendListMessage(token, leave_dic, event_by_name):
    users = event_by_name['중대원3']

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization" : "Bearer " + token['access_token']
    }

    data = {
        "template_object" : json.dumps({
            "object_type" : "list",
            "header_title" : "중대원3 휴가신청 현황",
            "header_link" : {
                "web_url" : "https://calendar.google.com",
                "mobile_web_url" : "https://calendar.google.com"
            },
            "contents" : [{
                
            },{

            },{

            }],
            "buttons" : [{
                "title" : "추천 휴가일",
                "link" : {
                    "web_url" : "https://naver.com",
                    "mobile_web_url" : "https://naver.com"
                }
            },{
                "title" : "캘린더 보기",
                "link" : {
                    "web_url" : "https://naver.com",
                    "mobile_web_url" : "https://naver.com"
                }
            }]
        })
    }



def getFriendsList(token):
    url = "https://kapi.kakao.com/v1/api/talk/friends"

    headers = {
        "Authorization" : "Bearer " + token['access_token']
    }

    response = json.loads(requests.get(url, headers=headers).text)
    print(response)
    print(response.get("elements"))

setupTalk()
