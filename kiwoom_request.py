from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *


class KiwoomRequest:
    def __init__(self):
        print("1")
        # kiwoom tr callback
        # self.kiwoom.OnReceiveTrData.connect(self.kiwoom_OnReceiveTrData)
        # login callback
        # self.__kiwoom.OnEventConnect.connect(self.kiwoom_login_callback)

    # 키움 api call
    def kiwoom_get_openapi(self):
        return self.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

    # 키움 api 로그인 되어있는지 확인
    def kiwoom_get_connect_state(self):
        # 1은 로그인 되어 있음, 0은 로그인 해야함
        print("***********************************")
        return self.kiwoom_get_openapi(self).dynamicCall("GetConnectState()")

    # 키움 api 로그인 호출
    def kiwoom_login_call(self):
        print("1235345344")
        self.__kiwoom.dynamicCall("CommConnect()")

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
            # self.get_login_info()
            print("zzzzz")
        elif n_err_code == -100:
            print("사용자 정보교환 실패")
        elif n_err_code == -101:
            print("서버접속 실패")
        elif n_err_code == -102:
            print("버전처리 실패")