import pandas as pd
from datetime import datetime


class SeasonData:


    def __init__(self, path: str) -> None:
        self.df = pd.read_excel(path, index_col = 0)
        self.START_DATE = self.df["DATE"].iloc[0]
        self.x = self.df["DATE"].apply(lambda x: self._date_to_int(x, self.START_DATE))
        self.y = self.df["W-L"].apply(lambda x: self._ratio_to_percentage(x))
        self.x_labels = self.df["DATE"].apply(


    def _ratio_to_percentage(self, ratio: str) -> float:
        wins, losses = map(lambda x: int(x), ratio.split("-"))
        return round(wins/(wins+losses)*100, 2)


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
        return (date-start_date).days


    def _shorten_date(self, date: str) -> str:
        ...


data = SeasonData("data.xlsx")
print(data.x)
print(data.y)
