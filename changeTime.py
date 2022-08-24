import datetime
from datetime import datetime, tzinfo
from datetime import date
from datetime import time
from time import timezone
import tzlocal
import pytz
from pytz import timezone

date_format='%m/%d/%Y %H:%M:%S'


date = datetime.now(tz=pytz.utc)

print('Current date & time is:' + date.strftime(date_format))
date = date.astimezone(timezone('US/Pacific'))
print('Local date & time is  :', date.strftime(date_format))






timestamp = "2022-06-26T01:30:17+0000"
d = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")

print(d.strftime(date_format))
d = d.astimezone(timezone('US/Pacific'))
print(d.strftime(date_format))





"""

timestamp = "2022-06-26T01:30:17+0000"
d = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")

new = d.strftime("%m/%d/%Y %H:%M:%S")
print(new)

new = new.astimezone(timezone('US/Pacific'))
print(new)
"""



"""
print(stripped)





print(stripped)



print(new)
"""




"""
updatedTimestamp = timestamp[:-5]

print(timestamp)
print(updatedTimestamp)


###Stripping the timestsamp string and turning it into a datetime object; telling datetime how it's formatted
stripped = datetime.strptime(updatedTimestamp, "%Y-%m-%dT%H:%M:%S%z")
print(stripped)




newTZ = datetime.timezone("-timedelta(hours=7)",stripped)
print(newTZ)

###Reformatting the timestamp into a new format, telling datetime how we want it formatted
boom = stripped.strftime("%m/%d/%Y %H:%M:%S")
print(boom)
"""


