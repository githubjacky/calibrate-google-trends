from loguru import logger
import os
from pathlib import Path
from pandas import DataFrame
from pymongo import MongoClient
from typing import List, Literal
from tqdm import tqdm

from .core import GTAB


class BaseTrendSearch:
    def __init__(self,
                 geo: str = "",
                 period: List[str] = ["2016-01-01", "2018-07-31"]):
        self.geo = geo
        self.period = period
        self.bad_keywords = []
        self.suffix = ""


    def setup(self, init_path: str = "gtab_config"):
        """Setup anchor banks."""

        timeframe = " ".join(self.period)
        anchor_dir = Path(f"{init_path}/output/google_anchorbanks")
        anchor_file = "_".join((
            f"google_anchorbank_geo={self.geo}",
            f"timeframe={timeframe}.tsv"
        ))
        anchor_path = anchor_dir / anchor_file

        t = GTAB(dir_path=init_path)
        if not anchor_path.exists():
            t.set_options(
                pytrends_config={
                    "geo": self.geo,
                    "timeframe": timeframe
                },
                conn_config={
                    "backoff_factor": 1.
                }
            )
            t.create_anchorbank()

        t.set_active_gtab(anchor_file)
        self.t = t


    def calibrate_instance(self, keyword: str) -> None:
        """Query the trends of the keyword.

        Note: store the data only if the data doesn't exist in the specified
        collection under specified mongodb database.
        """
        res = self.t.new_query(keyword)
        match res:
            case DataFrame():
                logger.info(f'query success: {keyword}')

                for i in range(len(res)):
                    date = res.index[i]
                    item  = {
                        'year': date.date().year,
                        'month': date.date().month,
                        'name': keyword.split(' "')[0],
                        'suffix': self.suffix,
                    }

                    if self.collection.count_documents(item) == 0:
                        item['max_ratio'] = res.at[date, 'max_ratio']
                        item['max_ratio_hi'] = res.at[date, 'max_ratio_hi']
                        item['max_ratio_lo'] = res.at[date, 'max_ratio_lo']
                        self.collection.insert_one(item)

            case int():
                logger.info(f'bad query: {keyword}')
                self.bad_keywords.append(keyword)


    def __continuous_calibrate(self, max_retry: int = 5) -> None:
        """Calibrate until all the bad keyword list is empty or the number of
        retries exceed the `max_retry`.
        """

        retry = 0
        while len(self.bad_keywords) != 0 and retry < max_retry:
            keywords = self.bad_keywords.copy()
            self.bad_keywords = []

            for keyword in tqdm(keywords, desc=f'calibrate bad keywods, {retry+1}th round'):
                self.calibrate_instance(keyword, self.collection)
            retry += 1

        if len(self.bad_keywords) != 0:
            print(f'bad keywords: {self.bad_keywords}')


    def calibrate_batch(self,
                        keywords: List[str],
                        db_name: str,
                        collection_name: str,
                        continuous_mode: Literal[True, False] = True,
                        max_retry: int = 5):
        logger.remove()
        logger.add(f'log/{db_name}/{collection_name}.log')

        client = MongoClient(os.environ['CONN_STR'])
        db = client[db_name]
        self.collection = db[collection_name]

        for keyword in keywords:
            self.calibrate_instance(keyword)

        if continuous_mode:
            self.__continuous_calibrate(max_retry)
