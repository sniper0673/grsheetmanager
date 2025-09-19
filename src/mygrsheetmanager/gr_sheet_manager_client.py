"""
GR 트레이더의 구글시트 매니저 – 클라이언트용
"""
import requests
import pandas as pd

# Essential imports
from mystockutil.server.get_available_server import get_available_server

# 로컬 호스트를 먼저 찾는다 > 데이터 절약하기 위해서
server_candidates = [
    'http://localhost:6019', # 백업서버
    'http://localhost:6009',
    'http://brstk2.iptime.org:6019',
    'http://brstk2.iptime.org:6009',
    'http://brstk.com:6019', # 백업서버
    'http://brstk.com:6009',
    'http://brstk.iptime.org:6009',
    'http://brstk.iptime.org:6019',
    ]

# SERVER_URL = "http://localhost:6009"
SERVER_URL = get_available_server(server_candidates=server_candidates)

# 안전한 API 호출을 위한 데코레이터
def safe_api_call(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[API 오류] {func.__name__} 실패: {e}")
            return None
    return wrapper



def add_wish(trader_name: str, stock_name: str, wish: str = "매수"):
    url = f"{SERVER_URL}/wishlist/{trader_name}"
    data = {
        "mode": "add",
        "stock_name": stock_name,
        "wish": wish,
    }
    return requests.post(url, json=data).json()

def replace_wishes(trader_name: str, stock_names: list, wish: str = "매수"):
    url = f"{SERVER_URL}/wishlist/{trader_name}"
    data = {
        "mode": "replace",
        "stock_names": stock_names,
        "wish": wish,
    }
    return requests.post(url, json=data).json()

def delete_wish(trader_name: str, stock_name: str):
    url = f"{SERVER_URL}/wishlist/{trader_name}"
    data = {
        "mode": "delete",
        "stock_name": stock_name,
    }
    return requests.post(url, json=data).json()

def get_all_wishlist():
    return requests.get(f"{SERVER_URL}/wishlist").json()

def get_trader_wishlist(trader_name: str):
    return requests.get(f"{SERVER_URL}/wishlist/{trader_name}").json()

"""
sell_list에 대해서 동일한 작업 수행
"""
def add_sell(trader_name: str, stock_name: str, wish: str = "매도"):
    url = f"{SERVER_URL}/selllist/{trader_name}"
    data = {
        "mode": "add",
        "stock_name": stock_name,
        "wish": wish,
    }
    return requests.post(url, json=data).json()

def replace_sells(trader_name: str, stock_names: list, wish: str = "매수"):
    url = f"{SERVER_URL}/selllist/{trader_name}"
    data = {
        "mode": "replace",
        "stock_names": stock_names,
        "wish": wish,
    }
    return requests.post(url, json=data).json()

def delete_sell(trader_name: str, stock_name: str):
    url = f"{SERVER_URL}/selllist/{trader_name}"
    data = {
        "mode": "delete",
        "stock_name": stock_name,
    }
    return requests.post(url, json=data).json()

def get_all_selllist():
    return requests.get(f"{SERVER_URL}/selllist").json()

def get_trader_selllist(trader_name: str):
    return requests.get(f"{SERVER_URL}/selllist/{trader_name}").json()

class SingleTraderWishListClient:
    """싱글 트레이더의 wish list를 관리하는 클라이언트 클래스"""

    def __init__(self, trader_name: str):
        self.trader_name = trader_name

    @safe_api_call
    def add_wish(self, stock_name: str, wish: str = "매수"):
        return add_wish(self.trader_name, stock_name, wish)
    @safe_api_call
    def replace_wishes(self, stock_names: list, wish: str = "매수"):
        return replace_wishes(self.trader_name, stock_names, wish)
    @safe_api_call
    def delete_wish(self, stock_name: str):
        return delete_wish(self.trader_name, stock_name)
    @safe_api_call
    def get_wishlist(self):# -> Any:
        data = get_trader_wishlist(self.trader_name)
        df = pd.DataFrame.from_records(data['data'])
        return df
    @safe_api_call
    def get_all_wishlist(self):
        data = get_all_wishlist()
        df = pd.DataFrame.from_records(data['data'])
        return df
    """
    selllist 코드
    """
    @safe_api_call
    def add_sell(self, stock_name: str, wish: str = "매도"):
        return add_sell(self.trader_name, stock_name, wish)
    @safe_api_call
    def replace_sells(self, stock_names: list, wish: str = "매도"):
        return replace_sells(self.trader_name, stock_names, wish)
    @safe_api_call
    def delete_sell(self, stock_name: str):
        return delete_sell(self.trader_name, stock_name)
    @safe_api_call
    def get_selllist(self):# -> Any:
        data = get_trader_selllist(self.trader_name)
        df = pd.DataFrame.from_records(data['data'])
        return df
    @safe_api_call
    def get_all_selllist(self):
        data = get_all_selllist()
        df = pd.DataFrame.from_records(data['data'])
        return df


if __name__ == "__main__":
    # 예시 사용법
    client = SingleTraderWishListClient("황금비1")
    print(client.add_wish("삼성전자", "매수"))
    print(client.get_wishlist())
    print(client.replace_wishes(["삼성전자", "LG전자"], "추매"))
    print(client.delete_wish("LG전자"))
    print(client.replace_wishes(["카카오", "네이버"], "매도"))
    print(client.get_wishlist())