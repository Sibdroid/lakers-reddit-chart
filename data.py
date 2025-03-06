import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


class SeasonLog:


    def __init__(self, url: str) -> None:
        self.url = url
        self._get_soup()
        self._get_record()


    def _get_soup(self) -> None:
        page = urllib.request.Request(self.url,
                                      headers={'User-Agent': 'Mozilla/5.0'})
        infile = urllib.request.urlopen(page).read()
        data = infile.decode("ISO-8859-1")
        self.soup = BeautifulSoup(data, features="lxml")


    def _get_record(self) -> None:
        self.record = []
        table = self.soup.find("tbody", attrs={"class": "Table__TBODY"})
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 7:
                date, opponent, result, record, *other = tr.find_all("td")
                self.record += [[date.text, opponent.text,
                                result.text, record.text]]
            else:
                pass
        self.df = pd.DataFrame(self.record)
        self.df = self.df.rename(columns=self.df.iloc[0]).drop(self.df.index[0])


    def __str__(self) -> str:
        return self.df.to_string()


    def save(self, path) -> None:
        self.df.to_excel(path)


log = SeasonLog("https://www.espn.com/nba/team/schedule/_/name/lal/season/2025")
log.save("data.xlsx")

