#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs
import os
import db

from  datetime import datetime as dt

from models import *


# 設定エンティティアクセスクラス
class SettingEntityAccess():

    # インスタンス化メソッド
    # 　を設定しない
    # def __init__(self):

    # 登録処理
    def entityInsert(self, member_list):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        self.member_list = member_list

        # 現在日時取得
        now = dt.now()

        db.session.query(SettingMaster).delete()
        db.session.commit()  # データベースコミット

        for settingMasterData in self.member_list:

            """
            設定マスタ:SETTING_MASTER

            id:id
            タイプ:type_section
            タイプ名:type_section_name
            ファイルタイプ:doc_type_section
            ファイルタイプ名:doc_type_section_name
            取込先パス設定:set_import_path
            登録日時:register_date
            登録者:register_cd
            更新日時:update_date
            更新者:update_cd
            """
            print(list(settingMasterData))
            print(settingMasterData[7])
            print(settingMasterData[2])
            # 設定マスタ　設定
            settingMaster = SettingMaster(settingMasterData[6]
                                        , settingMasterData[1]
                                        , settingMasterData[7]
                                        , settingMasterData[2]
                                        , settingMasterData[3]
                                        , now, "u0001", now,  "u0001")

            # 設定マスタ　データ登録
            db.session.add(settingMaster)  # 追加

        db.session.commit()  # データベースコミット

        db.session.close()  # セッションを閉じる

    # 全件取得処理
    def entitySearchAll(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 設定マスタを全取得
        settingMasters = db.session.query(SettingMaster).order_by(SettingMaster.id).all()
        #　データベース.セッションをクローズ
        db.session.close()

        result_list = []
        row_count = 1
        for settingMaster in settingMasters:
            """
            No ： row_count
            Type : type_name
            DocType : doc_type_name
            Import Folder Pat : set_import_path
            Import : 済　固定文字
            id : str(settingMaster.id)
            type_section : settingMaster.type_section
            doc_type_section : settingMaster.doc_type_section
            """
            result = [str(row_count), settingMaster.type_section_name, settingMaster.doc_type_section_name, settingMaster.set_import_path, '済', str(settingMaster.id), settingMaster.type_section, settingMaster.doc_type_section]
            row_count += 1
            result_list.append(result)

        return result_list;

# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    # エンティティ定義書読み取り処理
    settingEntityAccess = SettingEntityAccess()
    settingEntityAccess.entitySearchAll()
