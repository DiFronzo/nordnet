import matplotlib.dates as dates

from matplotlib.lines import Line2D
from nordnet import Nordnet
from datetime import datetime
from matplotlib import pyplot as plt


def westerncandlestick(ax, quotes, width=0.5, colorup='k', colordown='r',
                       ochl=True, linewidth=0.5):
    """
    Plot the time, open, high, low, close as a vertical line ranging
    from low to high.  Use a rectangular bar to represent the
    open-close span.  If close >= open, use colorup to color the bar,
    otherwise use colordown
    Parameters
    ----------
    ax : `Axes`
        an Axes instance to plot to
    quotes : sequence of quote sequences
        data to plot.  time must be in float date format - see date2num
        (time, open, high, low, close, ...) vs
        (time, open, close, high, low, ...)
        set by `ochl`
    width : float
        fraction of a day for the open and close lines
    colorup : color
        the color of the lines close >= open
    colordown : color
         the color of the lines where close <  open
    ochl: bool
        argument to select between ochl and ohlc ordering of quotes
    linewidth: float
        linewidth of lines
    Returns
    -------
    ret : tuple
        returns (lines, openlines, closelines) where lines is a list of lines
        added
    """

    OFFSET = width / 2.0

    lines = []
    openlines = []
    closelines = []
    for q in quotes:
        if ochl:
            t, open, close, high, low = q[:5]
        else:
            t, open, high, low, close = q[:5]

        if close >= open:
            color = colorup
        else:
            color = colordown

        vline = Line2D(xdata=(t, t), ydata=(low, high),
                       color=color, linewidth=linewidth, antialiased=True)
        lines.append(vline)

        openline = Line2D(xdata=(t - OFFSET, t), ydata=(open, open),
                          color=color, linewidth=linewidth, antialiased=True)
        openlines.append(openline)

        closeline = Line2D(xdata=(t, t + OFFSET), ydata=(close, close),
                           color=color, linewidth=linewidth, antialiased=True)
        closelines.append(closeline)

        ax.add_line(vline)
        ax.add_line(openline)
        ax.add_line(closeline)

    ax.autoscale_view()

    return lines, openlines, closelines


nn = Nordnet()

long_data = []

instrument_id = nn.main_search("DNB")[1][0]['instrument_id']
data = nn.get_history(instrument_id, weeks=3)[1][0]['prices']

for periods in data:
    date = datetime.fromtimestamp(periods['time'] / 1000.0)
    long_data.append(
        [dates.date2num(date), periods['open'], periods['high'], periods['low'], periods['last']])

fig, ax = plt.subplots()
westerncandlestick(ax, long_data, width=0.9, linewidth=1.44, ochl=False)
ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=20, ha='right')
plt.xlabel("Time")
plt.ylabel("NOK")

plt.show()
