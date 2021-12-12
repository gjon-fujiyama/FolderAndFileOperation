from datetime import datetime

from db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./db.sqlite3"

class SettingMaster(Base):
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
    __tablename__ = 'SETTING_MASTER'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    type_section = Column('type_section', String(2))
    type_section_name = Column('type_section_name', String(256))
    doc_type_section = Column('doc_type_section', String(2))
    doc_type_section_name = Column('doc_type_section_name', String(256))
    set_import_path = Column('set_import_path', String(256))
    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                type_section: str,
                type_section_name: str,
                doc_type_section: str,
                doc_type_section_name: str,
                set_import_path: str,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.type_section = type_section
        self.type_section_name = type_section_name
        self.doc_type_section = doc_type_section
        self.doc_type_section_name = doc_type_section_name
        self.set_import_path = set_import_path
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd

    def __str__(self):
        return ' id -> ' + str(self.id) + \
               ', type_section -> ' + self.type_section + \
               ', type_section_name -> ' + self.type_section_name + \
               ', doc_type_section -> ' + self.doc_type_section + \
               ', doc_type_section_name -> ' + self.doc_type_section_name + \
               ', set_import_path -> ' + self.set_import_path + \
               ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', register_cd -> ' + self.register_cd + \
               ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', update_cd -> ' + self.update_cd

class FilePathTran(Base):
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
    更新日時:update_date
    更新者:update_cd
    """
    __tablename__ = 'FILE_PATH_TRAN'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    type_section = Column('type_section', String(2))
    type_section_name = Column('type_section_name', String(256))
    doc_type_section = Column('doc_type_section', String(2))
    doc_type_section_name = Column('doc_type_section_name', String(256))
    file_name = Column('file_name', String(256))
    fll_file_path = Column('fll_file_path', String(256))
    folder_path = Column('folder_path', String(256))
    register_date = Column(
        'register_date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
        )
    register_cd = Column(
        'register_cd',
        String(20),
        nullable=False,)
    update_date = Column(
        'update_date',
        DateTime,
        )
    update_cd = Column(
        'update_cd',
         String(20)
         )

    def __init__(self,
                type_section: str,
                type_section_name: str,
                doc_type_section: str,
                doc_type_section_name: str,
                file_name: str,
                fll_file_path: str,
                folder_path: str,
                register_date: datetime,
                register_cd: str,
                update_date: datetime,
                update_cd: str):
        self.type_section = type_section
        self.type_section_name = type_section_name
        self.doc_type_section = doc_type_section
        self.doc_type_section_name = doc_type_section_name
        self.file_name = file_name
        self.fll_file_path = fll_file_path
        self.folder_path = folder_path
        self.register_date = register_date
        self.register_cd = register_cd
        self.update_date = update_date
        self.update_cd = update_cd

    def __str__(self):
        return ' id -> ' + str(self.id) + \
               ', type_section -> ' + self.type_section + \
               ', type_section_name -> ' + self.type_section_name + \
               ', doc_type_section -> ' + self.doc_type_section + \
               ', doc_type_section_name -> ' + self.doc_type_section_name + \
               ', file_name -> ' + self.file_name + \
               ', fll_file_path -> ' + self.fll_file_path + \
               ', folder_path -> ' + self.folder_path + \
               ', register_date -> ' + self.register_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', register_cd -> ' + self.register_cd + \
               ', update_date -> ' + self.update_date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', update_cd -> ' + self.update_cd
