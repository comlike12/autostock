# -*- coding: utf-8 -*-
import const
from PyQt5.QAxContainer import *

from logger_common import createLogger


class KiwoomCall:
    def __init__(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.logger = createLogger("kiwoom_api")

        # kiwoom tr callback
        # self.kiwoom.OnReceiveTrData.connect(self.on_receive_tr_data)

        # login callback
        # self.kiwoom.OnEventConnect.connect(self.login_callback)

    # 키움 api 반환
    def get_kiwoom_api(self):
        return self.kiwoom

    # 로그인 콜백 함수 지정
    def set_login_callback(self, callbackFnName):
        self.kiwoom.OnEventConnect.connect(callbackFnName)

    def set_tr_callback(self, callbackFnName):
        self.kiwoom.OnReceiveTrData.connect(callbackFnName)

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

    def kiwoom_get_repeat_cnt(self, tr_code, sRqName):
        return self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", tr_code, sRqName)