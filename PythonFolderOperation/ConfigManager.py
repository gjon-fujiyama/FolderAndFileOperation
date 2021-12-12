# coding: utf-8
import configparser
import json
from distutils.util import strtobool

# ファイルの存在チェック用モジュール
import os
import errno

class ConfigManager():

    # インスタンス化メソッド
    # 　を設定しない
    def __init__(self):
        # iniファイルの読み込み
        self.config_ini = configparser.ConfigParser()
        self.config_ini_path = 'config.ini'

        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(self.config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)

        # 設定ファイル読み込み
        self.config_ini.read(self.config_ini_path, encoding='utf-8')

        # タイプ配列初期設定
        self.typeSections = self.getSectionDicts('TYPE')
        self.docTypeSections = self.getSectionDicts('DOC_TYPE')


    # 値配列取得
    def getSectionValus(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        result_list = []
        for v in sectionItems.values():
            v_list = v.split(',')
            result_list.append(v_list[0])
        return result_list;

    # デフォルト値取得
    def getSectionDefaultValu(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        for v in sectionItems.values():
            v_list = v.split(',')
            if strtobool(v_list[2]):
                return v_list[0]

        return '';

    # 辞書作成
    def getSectionDicts(self, sectionName):

        sectionItems = dict(self.config_ini.items(sectionName))

        result_dict = {}
        for v in sectionItems.values():
            v_list = v.split(',')
            result_dict.setdefault(v_list[0], v_list[1])
        return result_dict;

    # タイプ値取得
    def getTypeSectionValue(self, key):
        return self.typeSections.get(key)

    # DOCタイプ値取得
    def getDocTypeSectionValue(self, key):
        return self.docTypeSections.get(key)
