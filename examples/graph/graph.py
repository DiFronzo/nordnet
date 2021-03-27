import matplotlib.dates as dates

from datetime import datetime, timedelta, timezone
from nordnet import Nordnet
from matplotlib import pyplot as plt


nn = Nordnet()

x = []
y = []

instrument_id = nn.main_search("DNB")[1][0]['instrument_id']
data = nn.get_trades(instrument_id)[1][0]['trades']

for transaction in data:
    date = datetime.fromtimestamp(transaction['trade_timestamp'] / 1000.0, tz=timezone.utc)
    x.append(date + timedelta(hours=1))
    y.append(transaction['price'])

plt.plot(x, y)

plt.xlabel("Time")
plt.ylabel("NOK")
plt.title('DNB ({}) - {}'.format(instrument_id, datetime.now().date()))
plt.gcf().autofmt_xdate()
myFmt = dates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.show()
