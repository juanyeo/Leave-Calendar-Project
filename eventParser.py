import calendar
import datetime
import dataStore as db

'''
<일정 처리 함수들>
불러온 휴가 정보 객체를 parse 하고 우선순위에 맞춰 신청자를 배열한다
처리한 결과를 집계해 출력한다
'''

def parseEventList(event_list, year, month):
    leave_dic = {}
    namedate = db.getNameDate()

    for oevent in event_list:
        columns = {}

        name = oevent['summary'].split(" ")[0]
        columns['name'] = name
        columns['oristart'] = oevent['start']['date']
        columns['oriend'] = oevent['end']['date']
        columns['startdate'] = int(oevent['start']['date'][-2:])
        columns['enddate'] = int(oevent['end']['date'][-2:])-1
        columns['fromlm'] = 0
        month1 = int(oevent['start']['date'][-5:-3])
        month2 = int(oevent['end']['date'][-5:-3])
        if month1 != month:
            columns['fromlm'] = 1
            columns['startdate'] = 1
        if month2 != month:
            last_day_of_month = calendar.monthrange(year, month)[1]
            columns['enddate'] = int(last_day_of_month)
        columns['description'] = oevent['description']
        columns['lastvac'] = namedate[name]['lastvac']
        namedate[name]['lastvac'] = oevent['end']['date']
        columns['ets'] = namedate[name]['ets']
        columns['saturation'] = 0
        columns['priority'] = 0
        columns['priority summary'] = ""

        leave_dic[oevent['id']] = columns

    return leave_dic, namedate

def setEventBy(leave_dic, year, month):
    event_by_day = {}
    last_day_of_month = int(calendar.monthrange(year, month)[1])
    for day in range(1,last_day_of_month+1):
        event_by_day[day] = []

    event_by_name = {}
    namedate = db.getNameDate()
    for key in namedate:
        event_by_name[key] = []
    
    for eid in leave_dic:
        leave = leave_dic[eid]
        for day in range(leave['startdate'], leave['enddate']+1):
            event_by_day[day] += [eid]
        
        event_by_name[leave['name']] += [eid]

    return event_by_day, event_by_name

'''
def appendSaturation(leave_dic, event_by_day):
    for day in event_by_day:
        eid_list = event_by_day[day]
        number_of_events = len(eid_list)
        for eid in eid_list:
            leave_dic[eid]['saturation'] = max(number_of_events, leave_dic[eid]['saturation'])
    
    return leave_dic
'''

def appendSaturation(leave_dic, ordered_event):
    for day in ordered_event:
        eid_list = ordered_event[day]
        number_of_events = len(eid_list)
        for i in range(len(eid_list)):
            if i+1 > leave_dic[eid_list[i]]['priority']:
                leave_dic[eid_list[i]]['priority'] = i+1
                leave_dic[eid_list[i]]['saturation'] = number_of_events

            summary_message = leave_dic[eid_list[i]]['priority summary'] 
            if summary_message != "":
                summary_message += " "
            summary_message += str(day) + "일(" + str(i+1) + ")"
            leave_dic[eid_list[i]]['priority summary'] = summary_message

    return leave_dic


def orderEvents(leave_dic, event_by_day, year, month):
    for day in event_by_day:
        #ordered_list = sorted(event_by_day[day], key=lambda x: (leave_dic[x]['lastvac'], leave_dic[x]['ets']))
        ordered_list = sorted(event_by_day[day], key=lambda x: (leave_dic[x]['lastvac']))
        '''
        for eid in ordered_list:
            mal_date = datetime.datetime(year, month, 1) + datetime.timedelta(days=60)
            ets_date = datetime.datetime.strptime(leave_dic[eid]['ets'], '%Y-%m-%d')
            if ets_date <= mal_date:
                ordered_list.insert(0, ordered_list.pop(ordered_list.index(eid)))
        '''
        event_by_day[day] = ordered_list
    
    return event_by_day

def depositSediments(ordered_event, dropnum):
    crystals = []
    for day in ordered_event:
        requests = ordered_event[day]
        '''
        for crystal in crystals:
            if crystal in requests:
                requests.remove(crystal)'''
        if len(requests) > dropnum:
            for i in range(len(requests)-dropnum):
                drop = requests[dropnum+i]
                crystals.append(drop)

    return crystals 

def printEventByDay(leave_dic, event_by_day, crystals):
    for day in event_by_day:
        if len(event_by_day[day]) == 0:
            continue

        for eid in event_by_day[day]:
            rstring = "{0:0=2d}".format(day)+": "+leave_dic[eid]['name']+" LAST "+leave_dic[eid]['lastvac']+" ETS "+leave_dic[eid]['ets']
            print(rstring)

def printLeaveEvents(leave_dic, year, month):

    text = str(year)+"년"+str(month)+"월 "+"휴가수합\n\n"
    for eid in leave_dic:
        pevent = leave_dic[eid]
        text += pevent['oristart'][-2:]+"-"+pevent['oriend'][-2:]+"\t"
        #text += pevent['oriend'][-5:-3]+"월"+pevent['oriend'][-2:]+"일 "
        text += pevent['name']+" "
        #text += pevent['description']+" "
        text += str(pevent['priority'])+"/"+str(pevent['saturation'])+"\n"
    
    text += "\n\n\n이상"

    return text

        

