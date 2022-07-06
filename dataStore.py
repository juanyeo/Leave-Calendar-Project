import pickle
import datetime

def setToken(credentials):
    pickle.dump(credentials, open("token.pkl", "wb"))

def setNameDate(namedate):
    pickle.dump(namedate, open("namedate.pkl", "wb"))

def setColorChanged(crystals):
    pickle.dump(crystals, open("colorchanged.pkl", "wb"))

def getToken():
    credentials = pickle.load(open("token.pkl", "rb"))
    return credentials

def getNameDate():
    namedate = pickle.load(open("namedate.pkl", "rb"))
    return namedate

def getColorChanged():
    colorchanged = pickle.load(open("colorchanged.pkl", "rb"))
    return colorchanged

#{'name': {'lastvac': '2020-10-25', 'ets': '2021-02-03'}}

namedate = {'중대원1': {'lastvac': '2020-10-25', 'ets': '2021-06-03'},
            '중대원1': {'lastvac': '2020-11-26', 'ets': '2021-01-04'},
            '중대원2': {'lastvac': '2020-09-09', 'ets': '2021-04-04'},
            '중대원3': {'lastvac': '2019-11-18', 'ets': '2022-03-06'},
            '중대원4': {'lastvac': '2020-09-09', 'ets': '2021-05-05'},
            '중대원5': {'lastvac': '2020-07-27', 'ets': '2021-02-23'},
            '중대원6': {'lastvac': '2020-06-16', 'ets': '2021-02-23'},
            '중대원7': {'lastvac': '2020-10-11', 'ets': '2021-02-23'}}

#setNameDate(namedate)
