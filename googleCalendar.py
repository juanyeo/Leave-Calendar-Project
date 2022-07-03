from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
import calendar
import dataStore as db
import eventParser as parser

'''
<구글캘린더 연동 함수들>
휴가 신청 내용 및 휴일 정보를 불러온다 / 구글캘린더 일정 색상을 바꾼다
'''

def connectGoogleCalendar():
    credentials = db.getToken()
    service = build('calendar', 'v3', credentials=credentials)
    return service

def getLeaveEvents(service, year, month):
    calendar_id = 'fpj5lcoac1e7s3i9i9io5mbu7s@group.calendar.google.com'
    first_day = datetime.datetime(year, month, 1).isoformat()[:-9]
    last_day_of_month = calendar.monthrange(year, month)[1]
    last_day = datetime.datetime(year, month, last_day_of_month).isoformat()[:-9]
    time_min = first_day + 'T00:00:00+09:00'
    time_max = last_day + 'T23:59:59+09:00'
    max_results = 250
    is_single_events = True
    orderby = 'startTime'

    event_list = service.events().list(calendarId = calendar_id, timeMin = time_min, timeMax = time_max,
    maxResults = max_results, singleEvents = is_single_events, orderBy = orderby).execute().get('items', [])

    return event_list

def getHolidayEvents(service, year, month):
    calendar_id = '86fngfntr6d71efbcoro83ja0k@group.calendar.google.com'
    first_day = datetime.datetime(year, month, 1).isoformat()[:-9]
    last_day_of_month = calendar.monthrange(year, month)[1]
    last_day = datetime.datetime(year, month, last_day_of_month).isoformat()[:-9]
    time_min = first_day + 'T00:00:00+09:00'
    time_max = last_day + 'T23:59:59+09:00'
    max_results = 250
    is_single_events = True
    orderby = 'startTime'

    holiday_list = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
    maxResults=max_results, singleEvents=is_single_events, orderBy=orderby).execute().get('items', [])

    return holiday_list

def changeColor(service, crystals):
    calendar_id = 'fpj5lcoac1e7s3i9i9io5mbu7s@group.calendar.google.com'

    colorchanged = db.getColorChanged()
    for cc in colorchanged:
        ccevent = service.events().get(calendarId=calendar_id, eventId=cc).execute()
        ccevent['colorId'] = '3' # changed color
        service.events().update(calendarId=calendar_id, eventId=ccevent['id'], body=ccevent).execute()

    for crystal in crystals:
        cevent = service.events().get(calendarId=calendar_id, eventId=crystal).execute()
        cevent['colorId'] = '8'
        service.events().update(calendarId=calendar_id, eventId=cevent['id'], body=cevent).execute()

def updateEvents(event_list, leave_dic, crystals, service):
    calendar_id = 'fpj5lcoac1e7s3i9i9io5mbu7s@group.calendar.google.com'

    for event in event_list:
        event_id = event['id']
        if event_id in crystals:
            event['colorId'] = '11'
        else:
            event['colorId'] = '10'
        event['description'] = leave_dic[event_id]['priority summary']
        service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
