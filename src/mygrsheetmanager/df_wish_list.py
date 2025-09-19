"""
여러 트레이더들의 wish list를 관리하는 DataFrame을 생성하는 모듈입니다.
"""

import pandas as pd
from mygrsheetmanager.single_trader_wish_list import SingleDfWishList

class _DfWithWishList:
    def __init__(self, trader_names: list):
        """
        트레이더 이름 리스트를 받아서 DataFrame을 초기화합니다.
        :param trader_names: 트레이더 이름의 리스트
        """
        self.trader_names = trader_names
        # self.df_wish_list = pd.DataFrame(index=trader_names)  # index: 트레이더 이름, columns: 종목명, values: 매수 희망 여부
        self.wish_list_dict = {name: SingleDfWishList(trader_name=name) for name in trader_names}
    @property
    def df(self) -> pd.DataFrame:
        """
        트레이더들의 매수 희망 종목 리스트를 DataFrame 형태로 반환합니다.
        :return: DataFrame 
            index: 트레이더 이름, columns: 종목명, values: 매수 희망 여부
        """
        # DataFrame을 생성할 때, 각 트레이더의 wish_list를 합칩니다.
        dfs = []
        for trader_name in self.trader_names:
            s = self.wish_list_dict[trader_name].wish_list

            # 비어 있는 경우라도 빈 DataFrame을 넣어줌
            if s.empty:
                dfs.append(pd.DataFrame(index=[trader_name]))  # 빈 row만 있는 DataFrame
            else:
                df = s.to_frame().T
                df.index = [trader_name]
                dfs.append(df)

        df_merged = pd.concat(dfs, axis=0).fillna("")
        df_merged.index.name = "trader"
        return df_merged.reindex(index=self.trader_names).sort_index(axis=1)

class DfWithWishList_manage_single(_DfWithWishList):
    def add_wish(self, trader_name: str, stock_name: str, wish: str = "매수") -> None:
        """
        특정 트레이더의 매수 희망 종목을 추가합니다.
        :param trader_name: 트레이더 이름
        :param stock_name: 종목명
        :param wish: 매수 희망 여부 (예: "매수", "관심")
        """
        if trader_name in self.wish_list_dict:
            self.wish_list_dict[trader_name].add_wish(stock_name, wish)
    def add_wishes(self, trader_name: str, stock_names: list, wish: str = "매수") -> None:
        """
        특정 트레이더의 매수 희망 종목을 일괄적으로 추가합니다.
        :param trader_name: 트레이더 이름
        :param stock_names: 종목명 리스트
        :param wish: 매수 희망 여부 (예: "매수", "관심")
        """
        if trader_name in self.wish_list_dict:
            for stock_name in stock_names:
                self.wish_list_dict[trader_name].add_wish(stock_name, wish)
    def remove_wish(self, trader_name: str, stock_name: str) -> None:
        """
        특정 트레이더의 매수 희망 종목을 제거합니다.
        :param trader_name: 트레이더 이름
        :param stock_name: 제거할 종목명
        """
        if trader_name in self.wish_list_dict:
            self.wish_list_dict[trader_name].remove_wish(stock_name)
    def replace_wishes(self, trader_name: str, stock_names: list, wish: str = "매수") -> None:
        """
        특정 트레이더의 매수 희망 종목을 일괄적으로 교체합니다.
        :param trader_name: 트레이더 이름
        :param stock_names: 종목명 리스트
        :param wish: 매수 희망 여부 (예: "매수", "관심")
        """
        if trader_name in self.wish_list_dict:
            self.wish_list_dict[trader_name].replace_wishes(stock_names, wish)
class DfWithWishList(DfWithWishList_manage_single):
    pass