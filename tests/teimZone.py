import pytz
from datetime import datetime as dt

now = dt.now(pytz.timezone("America/Mexico_City"))

# print(now.strftime('%d/%B/%Y %H:%M:%S')) #24-hour format
print(now.strftime('%d/%B/%Y %I:%M:%S')) #12-hour format