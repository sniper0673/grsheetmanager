"""
GR Sheet Manager를 구동하는 서버 코드

API 종류:
------------
GET    /wishlist
       전체 wish list를 JSON(table) 형식으로 보내줍니다.
POST   /wishlist/<trader_name>
       특정 트레이더의 wish를 추가, 교체 또는 삭제합니다.
       body 예시 (application/json):
       {
           "mode": "add",          # add | replace | delete
           "stock_name": "삼성전자", # add/delete 모드에서 필요
           "stock_names": ["삼성전자", "LG화학"], # replace 모드에서 필요
           "wish": "머야"            # 기본값: "머야"
       }

실행 방식:
------------
$ python wishlist_server.py

* 개발 동안은 Flask 내장 서버로 가능
* 관리 환경은 Waitress 또는 Gunicorn + systemd 구조로 구성

필요 패키지:
------------
flask, pandas, gspread, google-auth, SpreadsheetManager 관련 패키지
"""

from flask import Flask, jsonify, request
from mygrsheetmanager.gr_sheet_manager import GRSheetManager

app = Flask(__name__)

grsheet = GRSheetManager()  # 싱글턴으로 사용

def _push_wish_to_sheet() -> None:
    """Google Sheet에 wish list를 복사합니다."""
    try:
        grsheet.post_wish_df()
    except Exception as exc:
        app.logger.exception("Google Sheet에 복사 실패")
        raise exc

@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    """GR 트레이더 전체의 wish list를 JSON(table) 형식으로 보내줍니다."""
    df = grsheet.wish_list.df
    return df.to_json(orient="table", force_ascii=False), 200, {"Content-Type": "application/json; charset=utf-8"}

@app.route("/wishlist/<trader_name>", methods=["GET"])
def get_trader_wish(trader_name):
    df = grsheet.wish_list.df
    if trader_name not in df.index:
        return jsonify({"error": f"{trader_name}의 wish list가 없습니다."}), 404
    return df.loc[[trader_name]].to_json(orient="table", force_ascii=False)

@app.route("/wishlist/<trader>", methods=["POST"])
def upsert_wish(trader: str):
    """GR 트레이더의 wish 추가 (add), 교체 (replace), 삭제 (delete)를 지원합니다."""
    data = request.get_json(force=True)
    mode: str = data.get("mode", "add")
    wish: str = data.get("wish", "매수")

    if mode == "add":
        stock = data.get("stock_name")
        if not stock:
            return jsonify({"error": "add 모드에서는 stock_name이 필요합니다."}), 400
        grsheet.wish_list.add_wish(trader, stock, wish)
    elif mode == "replace":
        # 빈 리스트도 허용
        stocks = data.get("stock_names")
        grsheet.wish_list.replace_wishes(trader, stocks, wish)
    elif mode == "delete":
        stock = data.get("stock_name")
        if not stock:
            return jsonify({"error": "delete 모드에서는 stock_name이 필요합니다."}), 400
        grsheet.wish_list.remove_wish(trader, stock)
    else:
        return jsonify({"error": f"알 수 없는 mode: {mode}"}), 400

    _push_wish_to_sheet()
    return jsonify({"status": "ok"})

"""
sell_list 코드
"""
def _push_sell_to_sheet() -> None:
    """Google Sheet에 sell list를 복사합니다."""
    try:
        grsheet.post_sell_df()
    except Exception as exc:
        app.logger.exception("Google Sheet에 복사 실패")
        raise exc

@app.route("/selllist", methods=["GET"])
def get_selllist():
    """GR 트레이더 전체의 sell list를 JSON(table) 형식으로 보내줍니다."""
    df = grsheet.sell_list.df
    return df.to_json(orient="table", force_ascii=False), 200, {"Content-Type": "application/json; charset=utf-8"}

@app.route("/selllist/<trader_name>", methods=["GET"])
def get_trader_sell(trader_name):
    df = grsheet.sell_list.df
    if trader_name not in df.index:
        return jsonify({"error": f"{trader_name}의 sell list가 없습니다."}), 404
    return df.loc[[trader_name]].to_json(orient="table", force_ascii=False)

@app.route("/selllist/<trader>", methods=["POST"])
def upsert_sell(trader: str):
    """GR 트레이더의 sell 추가 (add), 교체 (replace), 삭제 (delete)를 지원합니다."""
    data = request.get_json(force=True)
    mode: str = data.get("mode", "add")
    sell: str = data.get("sell", "매도")

    if mode == "add":
        stock = data.get("stock_name")
        if not stock:
            return jsonify({"error": "add 모드에서는 stock_name이 필요합니다."}), 400
        grsheet.sell_list.add_wish(trader, stock, sell)
    elif mode == "replace":
        # 빈 리스트도 허용
        stocks = data.get("stock_names")
        grsheet.sell_list.replace_wishes(trader, stocks, sell)
    elif mode == "delete":
        stock = data.get("stock_name")
        if not stock:
            return jsonify({"error": "delete 모드에서는 stock_name이 필요합니다."}), 400
        grsheet.sell_list.remove_wish(trader, stock)
    else:
        return jsonify({"error": f"알 수 없는 mode: {mode}"}), 400

    _push_sell_to_sheet()
    return jsonify({"status": "ok"})

@app.route("/")
def ping():
    return "OK"

if __name__ == "__main__":
    # host='0.0.0.0' 은 개방적인 접속을 위한 파라미터
    app.run(host="0.0.0.0", port=6009, debug=True)