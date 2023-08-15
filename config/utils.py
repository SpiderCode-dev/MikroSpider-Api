import datetime

def now_date():
  now = datetime.datetime.now()
  return now.strftime("%Y-%m-%d %H:%M:%S")