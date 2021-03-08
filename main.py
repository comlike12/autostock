# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QListWidgetItem
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

        self.kiwoomCall.set_login_callback(self.login_callback_fn)

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
        print("로그인 요청 콜백 상태1111111111 : " + str(n_err_code))
        if n_err_code == 0:
            self.logger.debug("로그인 성공 - 로그인 정보 가져오기")
            self.get_login_info()
        elif n_err_code == -100:
            self.logger.debug("사용자 정보교환 실패")
        elif n_err_code == -101:
            self.logger.debug("서버접속 실패")
        elif n_err_code == -102:
            self.logger.debug("버전처리 실패")

    # account click event
    def account_list_item_clicked(self):
        # get account info
        print(self.account_list.currentItem().text())
        view_id_info = const.view_ids[const.VIEW_DEPOSIT_ID]
        # self.kiwoom.dynamicCall('CommRqData("계좌예수금조회", "opw00001", "0", "화면번호")', "USER_ID")
        # self.kiwoom.dynamicCall("SetInputValue(QString, QString)", ["계좌번호", self.account_list.currentItem().text()])
        self.kiwoom_set_input_value("계좌번호", self.account_list.currentItem().text())
        self.kiwoom_comm_rq_data(view_id_info[const.VIEW_NAME], view_id_info[const.TR_ID],
                                 view_id_info[const.SEARCH_TYPE], view_id_info[const.VIEW_ID])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    autoStockWindow = AutoWindowClass()
    autoStockWindow.show()
    sys.exit(app.exec_())
