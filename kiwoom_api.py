# -*- coding: utf-8 -*-
import const
from PyQt5.QAxContainer import *

from logger_common import createLogger


class KiwoomCall:
    def __init__(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.logger = createLogger("kiwoom_api")

        # kiwoom tr callback
        self.kiwoom.OnReceiveTrData.connect(self.on_receive_tr_data)

        # login callback
        # self.kiwoom.OnEventConnect.connect(self.login_callback)

    # 키움 api 반환
    def get_kiwoom_api(self):
        return self.kiwoom

    # 로그인 콜백 함수 지정
    def set_login_callback(self, callbackFn):
        self.kiwoom.OnEventConnect.connect(callbackFn)

    def kiwoom_dynamic_call(self, func_name):
        return self.kiwoom.dynamicCall(func_name)

    def kiwoom_get_user_info(self, name):
        return self.kiwoom.dynamicCall("GetLoginInfo(QString)", name)

    def kiwoom_set_input_value(self, sid, value):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", [sid, value])

    def kiwoom_comm_rq_data(self, view_name, tr_id, search_type, view_id):
        self.kiwoom.dynamicCall('CommRqData(QString, QString, QString, QString)',
                                [view_name, tr_id, search_type, view_id])

    def kiwoom_get_comm_data(self, tr_id, view_name, search_type, obj_name):
        return self.kiwoom.dynamicCall("GetCommData(QString, QString, QString, QString)",
                                       [tr_id, view_name, search_type, obj_name])

    def login_callback(self, n_err_code):
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
            # self.kiwoom.get_login_info()
        elif n_err_code == -100:
            self.logger.debug("사용자 정보교환 실패")
        elif n_err_code == -101:
            self.logger.debug("서버접속 실패")
        elif n_err_code == -102:
            self.logger.debug("버전처리 실패")

    def on_receive_tr_data(self, sScrNo, sRQName, sTRCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage,
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
                order_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "주문가능금액")
                money_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "예수금")
                ok_amt = self.kiwoom_get_comm_data(sTRCode, sRQName, 0, "출금가능금액")
                self.l_order_amt_txt.setText(str(int(order_amt)))
                self.l_money_amt_txt.setText(str(int(order_amt)))
                self.l_ok_amt_txt.setText(str(int(order_amt)))
        except Exception as e:
            print(e)