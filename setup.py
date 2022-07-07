from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datetime

# scopes = ["https://www.googleapis.com/auth/calendar"]
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

# credentials = flow.run_local_server(port=0)
# pickle.dump(credentials, open("token.pkl", "wb"))

credentials = pickle.load(open("token.pkl", "rb"))

service = build('calendar', 'v3', credentials=credentials)

calendar_id = 'fpj5lcoac1e7s3i9i9io5mbu7s@group.calendar.google.com'
today = datetime.date.today().isoformat()
time_min = today + 'T00:00:00+09:00'
time_max = today + 'T23:59:59+09:00'
max_results = 1
is_single_events = True
orderby = 'startTime'

event_result = service.events().list(calendarId = calendar_id, timeMin = time_min, timeMax = time_max,
maxResults = max_results, singleEvents = is_single_events, orderBy = orderby).execute()

print("Welcome to Setup.py")
print(event_result.get('items', [])[0]['summary'])
