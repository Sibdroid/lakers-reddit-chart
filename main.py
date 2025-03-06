import pandas as pd
from datetime import datetime


class SeasonData:


    def __init__(self, path: str) -> None:
        self.df = pd.read_excel(path, index_col = 0)


    def _ratio_to_percentage(self, ratio: str) -> float:
        wins, losses = map(lambda x: int(x), ratio.split("-"))


    def _format_date(self, date: str):
        date = datetime.strptime(date, "%a, %b %d")
        if date.month >= 10:
            date = date.replace(year = int(datetime.now().year) - 1)
        else:
            date = date.replace(year = int(datetime.now().year))
        return date


    def _date_to_int(self, date: str, start_date: str) -> float:
        date, start_date = (self._format_date(date),
                            self._format_date(start_date))
        print((date - start_date).days)


data = SeasonData("data.xlsx")
data._date_to_int("Sat, Oct 26", "Tue, Oct 22")

