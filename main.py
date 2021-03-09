# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QListWidgetItem, QAbstractItemView, QTableWidgetItem
from auto_main import *
from kiwoom_api import KiwoomCall
from logger_common import *
import const


class AutoWindowClass(QMainWindow, Ui_autoMainForm):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logger = createLogger("main")
        self.kiwoomCall = KiwoomCall()

        # login button click event
        self.b_login_btn.clicked.connect(self.login_button_event)

        # account list click event
        self.account_list.itemClicked.connect(self.account_list_item_clicked)

        # login callback fn setting
        self.kiwoomCall.set_login_callback(self.login_callback_fn)

        # tr callback fn setting
        self.kiwoomCall.set_tr_callback(self.tr_callback_fn)

    # get user login info
    def get_login_info(self):
        try:
            self.logger.debug("로그인 정보 조회")
            self.l_login_id_txt.setText(self.kiwoomCall.kiwoom_get_user_info("USER_ID"))
            self.l_login_nm_txt.setText(self.kiwoomCall.kiwoom_get_user_info("USER_NAME"))
            self.l_account_cnt_txt.setText(self.kiwoomCall.kiwoom_get_user_info("ACCOUNT_CNT"))
            server_type = self.kiwoomCall.kiwoom_get_user_info("GetServerGubun")
            if server_type == "1":
                self.l_server_type_txt.setText("모의투자")
            else:
                self.l_server_type_txt.setText("실서버")
            self.b_login_btn.setText("완료")

            acc_list = self.kiwoomCall.kiwoom_get_user_info("ACCLIST")
            print(acc_list.split(";"))

            for acc_info in acc_list.split(";"):
                if acc_info != "":
                    add_info = QListWidgetItem(acc_info)
                    self.account_list.addItem(add_info)
        except Exception as e:
            print(e)

    # login event
    def login_button_event(self):
        try:
            login_check = self.kiwoomCall.kiwoom_dynamic_call("GetConnectState()")
            self.logger.debug("로그인 체크 : " + str(login_check))
            if login_check == 1:
                self.logger.debug("이미 로그인 상태")
                QMessageBox.question(self, '확인', '이미 로그인 되었습니다.', QMessageBox.Ok)
            else:
                self.logger.debug("로그인 시작")
                self.kiwoomCall.kiwoom_dynamic_call("CommConnect()")
        except Exception as e:
            print(e)

    def login_callback_fn(self, n_err_code):
        """로그인 결과 수신
            :param n_err_code: 0: 로그인 성공, 100: 사용자 정보교환 실패, 101: 서버접속 실패, 102: 버전처리 실패
            :return:
            "ACCOUNT_CNT" : 보유계좌 수를 반환합니다.
            "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
            "USER_ID" : 사용자 ID를 반환합니다.
            "USER_NAME" : 사용자 이름을 반환합니다.
            "KEY_BSECGB" : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
            "FIREW_SECGB" : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
            "GetServerGubun" : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실서버)
        """
        print("로그인 요청 콜백 상태 : " + str(n_err_code))
        if n_err_code == 0:
            self.logger.debug("로그인 성공 - 로그인 정보 가져오기")
            self.get_login_info()
        elif n_err_code == -100:
            self.logger.debug("사용자 정보교환 실패")
        elif n_err_code == -101:
            self.logger.debug("서버접속 실패")
        elif n_err_code == -102:
            self.logger.debug("버전처리 실패")

    def tr_callback_fn(self, sScrNo, sRQName, sTRCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage,
                           sSPlmMsg, **kwargs):
        """TR 요청에 대한 결과 수신
            데이터 얻어오기 위해 내부에서 GetCommData() 호출
              GetCommData(
              BSTR strTrCode,   // TR 이름
              BSTR strRecordName,   // 레코드이름
              long nIndex,      // TR반복부
              BSTR strItemName) // TR에서 얻어오려는 출력항목이름
            :param sScrNo: 화면번호
            :param sRQName: 사용자 구분명
            :param sTRCode: TR이름
            :param sRecordName: 레코드 이름
            :param sPreNext: 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 2:연속(추가조회) 데이터 있음
            :param nDataLength: 사용안함
            :param sErrorCode: 사용안함
            :param sMessage: 사용안함
            :param sSPlmMsg: 사용안함
            :param kwargs:
            :return:
        """
        try:
            view_id_info = const.view_ids[sTRCode]

            if const.VIEW_DEPOSIT_ID == sTRCode:  # 예수금상세조회
                """
                order_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "주문가능금액")
                money_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "예수금")
                ok_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "출금가능금액")
                """
                order_amt = self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, 0, "주문가능금액")
                money_amt = self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, 0, "예수금")
                ok_amt = self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, 0, "출금가능금액")
                self.l_order_amt_txt.setText(str(int(order_amt)))
                self.l_money_amt_txt.setText(str(int(money_amt)))
                self.l_ok_amt_txt.setText(str(int(ok_amt)))
            elif const.VIEW_ACCOUNT_HAVE_STOCK_ID == sTRCode:
                rows = self.kiwoomCall.kiwoom_get_repeat_cnt(sTRCode, sRQName)
                lists = []
                for i in range(rows):
                    from decimal import Decimal
                    info = {'종목번호': str(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "종목번호")),
                            '종목명': str(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "종목명")),
                            '수익율': Decimal(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "수익률(%)")),
                            '매입가': int(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "매입가")),
                            '보유수량': int(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "보유수량")),
                            '매매가능수량': int(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "매매가능수량")),
                            '현재가': int(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "현재가")),
                            '매입금액': int(self.kiwoomCall.kiwoom_get_comm_data(sTRCode, sRQName, i, "매입금액"))}
                    lists.append(info)

                self.set_have_stock_table(lists, rows)
        except Exception as e:
            print(e)

    # account click event
    def account_list_item_clicked(self):
        # get account info
        view_id_info = const.view_ids[const.VIEW_DEPOSIT_ID]
        # self.kiwoom.dynamicCall('CommRqData("계좌예수금조회", "opw00001", "0", "화면번호")', "USER_ID")
        # self.kiwoom.dynamicCall("SetInputValue(QString, QString)", ["계좌번호", self.account_list.currentItem().text()])
        self.kiwoomCall.kiwoom_set_input_value("계좌번호", self.account_list.currentItem().text())
        self.kiwoomCall.kiwoom_comm_rq_data(view_id_info[const.VIEW_NAME], view_id_info[const.TR_ID],
                                            view_id_info[const.SEARCH_TYPE], view_id_info[const.VIEW_ID])

        self.get_account_have_stock_list()

    def get_account_have_stock_list(self):
        view_id_info = const.view_ids[const.VIEW_ACCOUNT_HAVE_STOCK_ID]
        self.kiwoomCall.kiwoom_set_input_value("계좌번호", self.account_list.currentItem().text())
        self.kiwoomCall.kiwoom_comm_rq_data(view_id_info[const.VIEW_NAME], view_id_info[const.TR_ID],
                                            view_id_info[const.SEARCH_TYPE], view_id_info[const.VIEW_ID])

    def set_have_stock_table(self, lists, cnt):
        """
        self.logger.debug(const.have_stock_haeaders)
        self.have_stock_table.setHorizontalHeaderLabels(const.have_stock_haeaders)

        self.have_stock_table.resizeColumnsToContents()
        self.have_stock_table.resizeRowsToContents()
        """
        self.have_stock_table.setRowCount(cnt)
        self.have_stock_table.setColumnCount(len(const.have_stock_haeaders))
        self.have_stock_table.setHorizontalHeaderLabels(const.have_stock_haeaders)

        row_cnt = 0
        for info in lists:
            col_cnt = 0
            for headname in const.have_stock_haeaders:
                self.have_stock_table.setItem(row_cnt, col_cnt, QTableWidgetItem(str(info[headname])))
                col_cnt += 1
            row_cnt += 1

        self.have_stock_table.resizeColumnsToContents()
        self.have_stock_table.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    autoStockWindow = AutoWindowClass()
    autoStockWindow.show()
    sys.exit(app.exec_())
