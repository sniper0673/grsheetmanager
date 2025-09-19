"""
싱글 트레이더의 매수 희망 종목 리스트를 관리하는 클래스입니다.
"""
import pandas as pd

class _SingleDfWishList:
    def __init__(self, trader_name):
        self.trader_name = trader_name
        self.wish_list = pd.Series() # index: 종목명, values: 매수 희망 여부로, "매수" 등등의 문자열로 표현된다.
class SingleDfWishList(_SingleDfWishList):
    def add_wish(self, stock_name: str, wish: str="매수") -> None:
        """
        매수 희망 종목을 추가한다.
        :param stock_name: 종목명
        :param wish: 매수 희망 여부 (예: "매수", "관심")
        """
        self.wish_list[stock_name] = wish
    def remove_wish(self, stock_name: str) -> None:
        """
        매수 희망 종목을 제거한다.
        :param stock_name: 제거할 종목명
        """
        if stock_name in self.wish_list:
            del self.wish_list[stock_name]
    def replace_wishes(self, stock_names: list, wish: str="매수") -> None:
        """
        매수 희망 종목을 일괄적으로 교체한다.
        :param stock_names: 종목명 리스트
        :param wish: 매수 희망 여부 (예: "매수", "관심")
        """
        self.wish_list = pd.Series(index=stock_names, data=wish)