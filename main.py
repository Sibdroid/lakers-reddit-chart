import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


def format_date(date: str):
    date = datetime.strptime(date, "%a, %b %d")
    if date.month >= 10:
        date = date.replace(year = int(datetime.now().year) - 1)
    else:
        date = date.replace(year = int(datetime.now().year))
    return date


def date_difference(date1: str, date2: str):
    return (format_date(date1)-format_date(date2)).days


def date_since_the_date(date: str,
                        days: int,
                        date_format: str = "%d/%m"):
    date = format_date(date)
    date += timedelta(days=days)
    return date.strftime(date_format)


def round_to_base(x, base = 5):
    return base * round(x/base)


def logical_or(cond1, cond2, cond3):
    return np.logical_or(np.logical_or(cond1, cond2), cond3)


COLORS = {"okc": "#70CBFF",
          "den": "#F5B478",
          "mem": "#B4AEC2",
          "lal": "#6938BC"}
START_DATE = "Tue, Oct 22"
END_DATE = "Wed, Mar 5"
DAYS_PASSED = round_to_base(date_difference(END_DATE, START_DATE))


class SeasonData:


    def __init__(self, path: str) -> None:
        self.df = pd.read_excel(path, index_col = 0)
        self.x = self.df["DATE"].apply(lambda x: self._date_to_int(x,
                                                                   START_DATE))
        self.y = self.df["W-L"].apply(lambda x: self._ratio_to_percentage(x))
        self.x_labels = self.df["DATE"].apply(lambda x: self._shorten_date(x))


    def _ratio_to_percentage(self, ratio: str) -> float:
        wins, losses = map(lambda x: int(x), ratio.split("-"))
        return round(wins/(wins+losses)*100, 2)


    def _date_to_int(self, date: str, start_date: str) -> float:
        date, start_date = (format_date(date),
                            format_date(start_date))
        return (date-start_date).days


    def _shorten_date(self, date: str) -> str:
        return date.split(", ")[1]


    def __repr__(self):
        return "A class containing season data"


def main() -> None:
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots()
    ax.set_ylim([0, 101])
    ax.set_xlim([0, DAYS_PASSED])
    ax.set_xticks(np.linspace(0, 135, 6))
    ax.set_xticklabels([date_since_the_date(START_DATE, i) for i in
                        np.linspace(0, 135, 6)])
    ax.set_yticks(range(0, 125, 25))
    ax.set_yticklabels(["", "25", "50", "75", "100"])
    teams = ["okc", "den", "mem", "lal"]
    for team in teams:
        color = COLORS[team]
        linewidth = 3.5 if team == "lal" else 2
        data = SeasonData(f"data-{team}.xlsx")
        if team == "lal":
            do_markers = np.where(logical_or(data.y == min(data.y),
                                             data.x == max(data.x),
                                             data.x == 111),
                                  True, False)
            ax.plot(data.x, data.y, color = color, linewidth = linewidth,
                    marker="o", fillstyle="full", mfc="#F0F0F0", mew=2,
                    markevery = do_markers)
        else:
            ax.plot(data.x, data.y, color = color, linewidth = linewidth)
    #ax.add_patch(Rectangle((0, 0), 19, 102, fill=True,
    #                       color='#CCCCCC',
    #                       alpha=0.95, zorder=100,
    #                       figure=fig))
    plt.savefig("chart.png", dpi = 600)


if __name__ == "__main__":
    main()
