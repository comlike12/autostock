VIEW_ID = "view_id"
VIEW_NAME = "view_name"
TR_ID = "tr_id"
SEARCH_TYPE = "search_type"

VIEW_DEPOSIT_ID = "opw00001"  # 예수금상세조회 키움 id
VIEW_ACCOUNT_HAVE_STOCK_ID = "opw00018"

view_ids = {
    VIEW_DEPOSIT_ID: {VIEW_ID: "000", VIEW_NAME: "예수금상세조회", TR_ID: VIEW_DEPOSIT_ID, SEARCH_TYPE: "0"},
    VIEW_ACCOUNT_HAVE_STOCK_ID: {VIEW_ID: "001", VIEW_NAME: "계좌평가잔고내역요청", TR_ID: VIEW_ACCOUNT_HAVE_STOCK_ID, SEARCH_TYPE: "0"}
}

have_stock_haeaders = ['종목번호', '종목명', '수익율', '매입가', '보유수량', '매매가능수량', '현재가', '매입금액']
