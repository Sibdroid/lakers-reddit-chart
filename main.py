import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
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


COLORS = {"okc": "#70CBFF",
          "den": "#F6C479",
          "mem": "#B4AEC2",
          "lal": "#6938BC"}
START_DATE = "Tue, Oct 22"
END_DATE = "Sat, Mar 22"
DAYS_PASSED = round_to_base(date_difference(END_DATE, START_DATE))
print(DAYS_PASSED)


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
    ax.set_ylim([0, 102])
    ax.set_xlim([0, DAYS_PASSED])
    ax.set_xticks(np.linspace(0, DAYS_PASSED, 6))
    ax.set_xticklabels([date_since_the_date(START_DATE, i) for i in
                        np.linspace(0, DAYS_PASSED, 6)])
    ax.set_yticks(range(0, 125, 25))
    teams = ["okc", "den", "mem", "lal"]
    for team in teams:
        color = COLORS[team]
        linewidth = 3 if team == "lal" else 2
        data = SeasonData(f"data-{team}.xlsx")
        ax.plot(data.x, data.y, color = color, linewidth = linewidth)
    plt.show()


if __name__ == "__main__":
    main()
