import datetime
import calendar
import dataStore as db
import eventParser as parser
import googleCalendar as gc
import kakaoTalk as talk
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

'''
<휴가 신청 및 알림 main 함수>
내용: 휴가 정산 함수 (year, month)
구글캘린더에서 휴가 신청 정보를 불러와 우선순위별로 인원을 배치하고
휴가 수합 결과를 개인별로 카카오톡으로 전달한다
'''
def updateCalendar(year, month):
    service = gc.connectGoogleCalendar()
    event_list = gc.getLeaveEvents(service, year, month)
    
    leave_dic, new_namedate = parser.parseEventList(event_list, year, month)
    event_by_day, event_by_name = parser.setEventBy(leave_dic, year, month)
    ordered_event = parser.orderEvents(leave_dic, event_by_day, year, month)
    leave_dic = parser.appendSaturation(leave_dic, ordered_event)
    crystals = parser.depositSediments(ordered_event, 5)
    print_text = parser.printLeaveEvents(leave_dic, 2020, 12)

    gc.updateEvents(event_list, leave_dic, crystals, service)

    token = talk.connectKakaoTalk()
    talk.sendResultText(token, print_text)
    #talk.sendWarningMessage(token, leave_dic, crystals)
    
updateCalendar(2020, 12)

