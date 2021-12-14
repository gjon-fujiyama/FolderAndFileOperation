#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs
import os
import glob
import db

import datetime
from sqlalchemy import distinct
from sqlalchemy import and_, or_, not_

from models import *

# ファイルパス エンティティアクセスクラス
class FilePathAccess():

    # ファイルパス　エンティティ　INSERT処理
    def entityImport(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 現在日時取得
        now = datetime.now()

        # 設定マスタを全取得
        settingMasters = db.session.query(SettingMaster).order_by(SettingMaster.id).all()

        # ファイルパステーブル　全削除
        db.session.query(FilePathTran).delete()
        # db.session.close()

        # 設定マスタ全件ループ
        result_list = []
        for settingMaster in settingMasters:
            results = [p for p in glob.glob(r'{}/{}'.format(settingMaster.set_import_path,'**'), recursive=True) if os.path.isfile(p)]

            basenames = []
            dirnames = []
            for result in results:
                # 拡張子なしファイル名
                # basename = os.path.splitext(os.path.basename(result))[0]
                basename = os.path.basename(result)
                # パス
                dirname = os.path.dirname(result)

                """
                ファイルパス:FILE_PATH_TRAN

                id:id
                タイプ:type_section
                タイプ名:type_section_name
                ファイルタイプ:doc_type_section
                ファイルタイプ名:doc_type_section_name
                ファイル名：file_name
                フルファイルパス:fll_file_path
                フォルダパス:folder_path
                登録日時:register_date
                登録者:register_cd
                更新日時:update_date.type_section, settingMaster.type_section_name,
                更新者:update_cd
                """
                filePathTran = FilePathTran(settingMaster.type_section,
                                            settingMaster.type_section_name,
                                            settingMaster.doc_type_section,
                                            settingMaster.doc_type_section_name,
                                            basename,
                                            result,
                                            dirname, now, "u0001", now,  "u0001")

                # ファイルパス　データ登録
                db.session.add(filePathTran)  # 追加

            # print(str(len(basenames)))
            # print(str(len(dirnames)))

        db.session.commit()  # データベースコミット

        db.session.close()  # セッションを閉じる

        # 登録データ数を戻す
        return str(len(result_list));

    # 全件取得処理
    def entitySearchAll(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 設定マスタを全取得
        filePathTrans = db.session.query(FilePathTran).order_by(FilePathTran.id).all()
        #　データベース.セッションをクローズ
        db.session.close()

        result_list = []
        row_count = 1
        for filePathTran in filePathTrans:
            """
            No ： row_count
                id:id
                タイプ:type_section
                タイプ名:type_section_name
                ファイル名：file_name
                フルファイルパス:fll_file_path
                フォルダパス:folder_path
            """
            result = [str(row_count), filePathTran.type_section_name, filePathTran.doc_type_section_name, filePathTran.file_name, filePathTran.fll_file_path, filePathTran.id, filePathTran.type_section, filePathTran.doc_type_section, filePathTran.folder_path]
            row_count += 1
            result_list.append(result)

        return result_list;

    # 検索取得処理
    def entitySearch(self, type_section_name, doc_type_section_name, file_name, configManager):

        # fileter設定
        if type_section_name:

            type_section = configManager.getTypeSectionValue(type_section_name)
            if doc_type_section_name:
                doc_type_section = configManager.getDocTypeSectionValue(doc_type_section_name)
                if file_name:
                    filePathTrans = db.session.query(FilePathTran).filter(and_(FilePathTran.type_section == type_section, FilePathTran.doc_type_section == doc_type_section, FilePathTran.file_name.like("%{0}%".format(file_name)))).order_by(FilePathTran.id).all()
                else:
                    filePathTrans = db.session.query(FilePathTran).filter(FilePathTran.type_section == type_section, FilePathTran.doc_type_section == doc_type_section).order_by(FilePathTran.id).all()
            else:
                if file_name:
                    filePathTrans = db.session.query(FilePathTran).filter(and_(FilePathTran.type_section == type_section, FilePathTran.file_name.like("%{0}%".format(file_name)))).order_by(FilePathTran.id).all()
                else:
                    filePathTrans = db.session.query(FilePathTran).filter(FilePathTran.type_section == type_section).order_by(FilePathTran.id).all()
        else:
            if doc_type_section_name:
                doc_type_section = configManager.getDocTypeSectionValue(doc_type_section_name)
                if file_name:
                    filePathTrans = db.session.query(FilePathTran).filter(FilePathTran.doc_type_section == doc_type_section, FilePathTran.file_name.like("%{0}%".format(file_name))).order_by(FilePathTran.id).all()
                else:
                    filePathTrans = db.session.query(FilePathTran).filter(FilePathTran.doc_type_section == doc_type_section).order_by(FilePathTran.id).all()
            else:
                if file_name:
                    filePathTrans = db.session.query(FilePathTran).filter(FilePathTran.file_name.like("%{0}%".format(file_name))).order_by(FilePathTran.id).all()
                else:
                    filePathTrans = db.session.query(FilePathTran).order_by(FilePathTran.id).all()

        # 検索実行
        #　データベース.セッションをクローズ
        db.session.close()

        result_list = []
        row_count = 1
        for filePathTran in filePathTrans:
            """
            No ： row_count
                id:id
                タイプ:type_section
                タイプ名:type_section_name
                ファイル名：file_name
                フルファイルパス:fll_file_path
                フォルダパス:folder_path
            """
            result = [str(row_count), filePathTran.type_section_name, filePathTran.doc_type_section_name, filePathTran.file_name, filePathTran.fll_file_path, filePathTran.id, filePathTran.type_section, filePathTran.doc_type_section, filePathTran.folder_path]
            result_list.append(result)
            row_count +=1

        return result_list;


    # DISTINC取得処理
    def entityDistinctSearchAll(self):
        path = SQLITE3_NAME
        if not os.path.isfile(path):

            # テーブルを作成する
            Base.metadata.create_all(db.engine)

        # 設定マスタを全取得
        # filePathTrans = db.session.query(FilePathTran).distinct(FilePathTran.type_section_name).all()
        sql = "select distinct(type_section_name) as type_section_name from file_path_tran"
        filePathTrans = db.session.execute(sql)

        # 取り出し例
        # for v in filePathTrans:
        #    print(v.type_section_name)

        result_list = [""]
        row_count = 1
        for filePathTran in filePathTrans:
            """
            No ： row_count
                id:id
                タイプ:type_section
                タイプ名:type_section_name
                ファイル名：file_name
                フルファイルパス:fll_file_path
                フォルダパス:folder_path
            """
            result = filePathTran.type_section_name
            row_count += 1
            result_list.append(result)

        return result_list;

    # DISTINC取得処理
    def entityDistinctTupleAll(self):

        # 設定マスタを全取得
        sql = "select distinct(type_section_name) as type_section_name, type_section from file_path_tran"
        filePathTrans = db.session.execute(sql)

        # 取り出し例
        # for v in filePathTrans:
        #    print(v.type_section_name)

        result_list = {}
        row_count = 1
        for filePathTran in filePathTrans:
            """
            No ： row_count
                id:id
                タイプ:type_section
                タイプ名:type_section_name
                ファイル名：file_name
                フルファイルパス:fll_file_path
                フォルダパス:folder_path
            """
            result_list.setdefault(filePathTran.type_section_name, filePathTran.type_section)

        return result_list;

# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    # ファイルパス読み取り処理
    filePathAccess = FilePathAccess()
    filePathAccess.entityImport()
