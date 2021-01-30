# -*- coding: utf-8 -*-
import sys
import logging
import const
from auto_main import *
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

view_ids = {
    const.VIEW_DEPOSIT_ID: {const.VIEW_ID: "000", const.VIEW_NAME: "예수금상세조회", const.TR_ID: const.VIEW_DEPOSIT_ID,
                            const.SEARCH_TYPE: "0"}
}


class AutoWindowClass(QMainWindow, Ui_autoMainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # kiwoom tr callback
        self.kiwoom.OnReceiveTrData.connect(self.kiwoom_OnReceiveTrData)

        # login callback
        self.kiwoom.OnEventConnect.connect(self.kiwoom_login_callback)
        # login button click event
        self.b_login_btn.clicked.connect(self.login_button_event)
        # account list click event
        self.account_list.itemClicked.connect(self.account_list_item_clicked)

    # login event
    def login_button_event(self):
        login_check = self.kiwoom.dynamicCall("GetConnectState()")
        if login_check == 1:
            QMessageBox.question(self, '확인', '이미 로그인 되었습니다.', QMessageBox.Ok)
        else:
            self.kiwoom.dynamicCall("CommConnect()")

    # login event callback function
    def kiwoom_login_callback(self, n_err_code):
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
        if n_err_code == 0:
            self.get_login_info()
        elif n_err_code == -100:
            logger.debug("사용자 정보교환 실패")
        elif n_err_code == -101:
            logger.debug("서버접속 실패")
        elif n_err_code == -102:
            logger.debug("버전처리 실패")

    # get user login info
    def get_login_info(self):
        self.l_login_id_txt.setText(self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_ID"))
        self.l_login_nm_txt.setText(self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_NAME"))
        self.l_account_cnt_txt.setText(self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT"))
        server_type = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "GetServerGubun")
        if server_type == "1":
            self.l_server_type_txt.setText("모의투자")
        else:
            self.l_server_type_txt.setText("실서버")
        self.b_login_btn.setText("완료")

        try:
            acc_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCLIST")
            print(acc_list.split(";"))

            for acc_info in acc_list.split(";"):
                if acc_info != "":
                    add_info = QListWidgetItem(acc_info)
                    self.account_list.addItem(add_info)
        except Exception as e:
            print(e)

    # account click event
    def account_list_item_clicked(self):
        # get account info
        print(self.account_list.currentItem().text())
        view_id_info = view_ids[const.VIEW_DEPOSIT_ID]
        # self.kiwoom.dynamicCall('CommRqData("계좌예수금조회", "opw00001", "0", "화면번호")', "USER_ID")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", ["계좌번호", self.account_list.currentItem().text()])
        self.kiwoom.dynamicCall('CommRqData(QString, QString, QString, QString)',
                                view_id_info[const.VIEW_NAME],
                                view_id_info[const.TR_ID],
                                view_id_info[const.SEARCH_TYPE],
                                view_id_info[const.VIEW_ID])

    def kiwoom_OnReceiveTrData(self, sScrNo, sRQName, sTRCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage,
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
        if sRQName == "예수금상세조회":
            order_amt = int(self.kiwoom.dynamicCall("GetCommData(QString, QString, QString, QString)", [sTRCode, sRQName, 0, "주문가능금액"]))
            self.l_order_amt_txt.setText(str(order_amt))


if __name__ == '__main__':
    # 로그 파일 핸들러
    fh_log = TimedRotatingFileHandler('C:/logs/log', when='midnight', encoding='utf-8', backupCount=120)
    fh_log.setLevel(logging.DEBUG)

    # 콘솔 핸들러
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # 로깅 포멧 설정
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    fh_log.setFormatter(formatter)
    sh.setFormatter(formatter)

    # 로거 생성 및 핸들러 등록
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh_log)
    logger.addHandler(sh)

    app = QApplication(sys.argv)
    autoStockWindow = AutoWindowClass()
    autoStockWindow.show()
    sys.exit(app.exec_())
