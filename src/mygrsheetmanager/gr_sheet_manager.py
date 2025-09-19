"""
트레이더 GR의 구글시트 매니저
구현 기능
1. 여러 GR 트레이더의 매수 희망 종목에 대해서 정리하여 관리
    wish_list라는 sheet에 트레이더별로 종목을 정리하여 관리한다.
    트레이더 클래스는 여러개 생성되어도, 이 클래스는 하나만 존재한다.
"""
from mygrsheetmanager.df_wish_list import DfWithWishList
from mystockutil.spreadsheet.spreadsheet_manager import SpreadsheetManager
from myutil.path import get_credentials_path

CRED_DIR = get_credentials_path()
CRED_JSON_PATH = CRED_DIR / 'vertical-album-400707-49b25aaf32d5.json'

SHEET_ID = "1iK7UY7g_fSRSAOpIEYrFR41p_qK68LhkcIfqr7NUxug"
# TRADER_NAMES = [
#     '황금비0', '황금비1', '황금비2', 
#     # '황금비3', '황금비4',
#     '황금비5', '황금비6', 
#     '황금비_test',
# ]
TRADER_NAMES = [
    '뉴황금비0', '뉴황금비1', 
    # '황금비2', 
    # '황금비3', '황금비4',
    # '황금비5', 
    '황금비6', 
    '황금비_test',
]

class _GRSheetManager:
    """
    self._df_wish_list: pd.DataFrame
        index: 트레이더 이름
        columns: 종목명
        values: 매수 희망 여부로, "매수" 등등의 문자열로 표현된다.
    """
    def __init__(self):
        self.sheet_manager = SpreadsheetManager(
            creds_json_path=CRED_JSON_PATH,
            sheet_id=SHEET_ID,
        )
        self.wish_sheet_name = 'wish_list'
        self.sell_sheet_name = 'sell_list'
        self.wish_list = DfWithWishList(trader_names=TRADER_NAMES[0:-1])
        # 매도리스트도 동일한 클래스로 생성해 준다. 
        self.sell_list = DfWithWishList(trader_names=TRADER_NAMES[0:-1])

class GRSheetManager_posting(_GRSheetManager):
    def post_wish_df(self) -> None:
        """
        wish_list 시트에 DataFrame을 업로드한다.
        :param df: 업로드할 DataFrame
        """
        self.sheet_manager.upload_df(self.wish_list.df, worksheet_name=self.wish_sheet_name, index=True)
    def post_sell_df(self) -> None:
        """
        sell_list 시트에 DataFrame을 업로드한다.
        :param df: 업로드할 DataFrame
        """
        self.sheet_manager.upload_df(self.sell_list.df, worksheet_name=self.sell_sheet_name, index=True)
        
class GRSheetManager(GRSheetManager_posting):
    pass

"""테스트용 코드"""
def test_add_single_wish():
    mgr = GRSheetManager_posting()
    mgr.wish_list.add_wish("황금비0", "삼성전자", "매수")
    df = mgr.wish_list.df
    assert df.loc["황금비0", "삼성전자"] == "매수"

def test_multiple_wishes():
    mgr = GRSheetManager_posting()
    mgr.wish_list.add_wish("황금비1", "LG화학", "관심")
    mgr.wish_list.add_wish("황금비1", "카카오", "매수")
    df = mgr.wish_list.df
    assert df.loc["황금비1", "LG화학"] == "관심"
    assert df.loc["황금비1", "카카오"] == "매수"

def test_replace_wishes():
    mgr = GRSheetManager_posting()
    mgr.wish_list.wish_list_dict["황금비2"].replace_wishes(["현대차", "기아"], wish="매수")
    df = mgr.wish_list.df
    assert df.loc["황금비2", "현대차"] == "매수"
    assert df.loc["황금비2", "기아"] == "매수"

def test_remove_wish():
    mgr = GRSheetManager_posting()
    mgr.wish_list.add_wish("황금비3", "셀트리온", "매수")
    mgr.wish_list.wish_list_dict["황금비3"].remove_wish("셀트리온")
    df = mgr.wish_list.df
    assert "셀트리온" not in df.columns or df.loc["황금비3", "셀트리온"] == ""

def run_test_case(title: str, func):
    print(f"\n[TEST] {title}")
    try:
        func()
        print("→ ✅ 성공")
    except Exception as e:
        print(f"→ ❌ 실패: {e}")

if __name__ == "__main__":
    run_test_case("단일 종목 추가", test_add_single_wish)
    run_test_case("다수 종목 추가", test_multiple_wishes)
    run_test_case("비어 있는 트레이더 포함", test_empty_wish_trader_included)
    run_test_case("일괄 종목 교체", test_replace_wishes)
    run_test_case("종목 삭제", test_remove_wish)
    print("\n모든 테스트 완료")
