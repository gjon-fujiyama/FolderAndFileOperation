# coding: utf-8
# *************************************************************************************
# Folder And File Operetion Application
#
# exe ファイルコマンド
# pyinstaller --clean .\FolderAndFileOperetion.spec
# *************************************************************************************
# *====================================================================================
# * インポートライブラリ
# *====================================================================================
#(pip install pysimplegui)
import PySimpleGUI as sg
import json
from distutils.util import strtobool

# ファイルの存在チェック用モジュール
import os
import errno
# +-----------------------------------------------------------------------------------+
# + SQliteDB　SettingEntityAccess
# +-----------------------------------------------------------------------------------+
from settingEntityAccess import SettingEntityAccess
from FilePathAccess import FilePathAccess
from FileOperation import FileOperation
from ConfigManager import ConfigManager
# +-----------------------------------------------------------------------------------+
# + ヘッダー表示リスト作成
# +-----------------------------------------------------------------------------------+
header =  ['No', 'Type', 'Doc Type', 'Import Folder Path', 'Register']
data_header =  ['No', 'Type', 'Doc Type', 'File Name', 'File Full Path']

# +-----------------------------------------------------------------------------------+
# + クラスインスタンス化
# +-----------------------------------------------------------------------------------+
settingEntityAccess = SettingEntityAccess()
filePathAccess = FilePathAccess()
fileOperation = FileOperation()
configManager = ConfigManager()

# +-----------------------------------------------------------------------------------+
# + 初期データリスト
# +-----------------------------------------------------------------------------------+
member_list = settingEntityAccess.entitySearchAll()
data_list = filePathAccess.entitySearchAll()

typeValues = configManager.getSectionValus('TYPE')
typeDefaultValue = configManager.getSectionDefaultValu('TYPE')

docTypeValues = configManager.getSectionValus('DOC_TYPE')
docTypeDefaultValue = configManager.getSectionDefaultValu('DOC_TYPE')

# ファイル名退避用
# 一覧再表示時に使用する
org_file_names_bk = []
to_file_names_bk = []

# +-----------------------------------------------------------------------------------+
# + 行番号振りなおし
# +-----------------------------------------------------------------------------------+
def renumbering():
    row_no = 1
    for row in member_list:
        row[0] = row_no
        row_no += 1

# +-----------------------------------------------------------------------------------+
# + レイアウト設定
# +-----------------------------------------------------------------------------------+
# ------ Menu Definition ------ #
menu_def = [['File', ['Open', ['File', 'Folder', ],'Quit'  ]],
            ['Setting', ['Reload', ['Reload FolderPath', 'Reload FilePath', ],'Setting Reflection'  ]],
            ['Help', 'About app...'], ]

# ------ Tab1 Definition ------ #
t1 = sg.Tab('SearchFileList' ,[[sg.Combo(typeValues, default_value=typeDefaultValue, key='-Data_Combo TYPE-', size=(10,1)),
                                sg.Combo(docTypeValues, default_value=docTypeDefaultValue, key='-Data_Combo DOC_TYPE-', size=(20,1)),
                                sg.InputText(key='Data_File_Path_Name'),
                                sg.Button('Search',key='Data_Search'),
                                sg.Button('Clear',key='Data_Search_Clear'),
                                sg.Button('Reload',key='Data_Reload', pad=((100, 0),(0,0)))],
                                [sg.Table(
                                    values=data_list,
                                    headings=data_header,
                                    auto_size_columns=False,
                                    col_widths=[5, 8, 8, 20, 70],
                                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                    justification='left',
                                    enable_events=True,
                                    text_color='#000000',
                                    background_color='#cccccc',
                                    alternating_row_color='#ffffff',
                                    header_text_color='#0000ff',
                                    header_background_color='#cccccc',
                                    key='_filestable_data_',
                                    size=(800, 10),)],
                                    [sg.Button('FileOpen',key='FileOpen'),sg.Button('FolderOpen',key='FolderOpen')]
                                    ])

# ------ Tab2 Definition ------ #
t2 = sg.Tab('Setting' ,[[sg.Button('Quit',key='Quit'),sg.Button('Reload',key='Reload', pad=((640, 0),(0,0)))],
        [sg.Table(
            values=member_list,
            headings=header,
            auto_size_columns=False,
            col_widths=[5, 8, 15, 60, 8],
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            justification='left',
            enable_events=True,
            text_color='#000000',
            background_color='#cccccc',
            alternating_row_color='#ffffff',
            header_text_color='#0000ff',
            header_background_color='#cccccc',
            key='_filestable_',
            size=(800, 10),
            )],
            [sg.Button('Add',key='Add'),sg.Button('Del',key='Del'),sg.Button('Reflection', key='Ref', pad=((600, 0),(0,0)))],
            [sg.Text("Import Type         :"),sg.Combo(typeValues, default_value=typeDefaultValue, key='-SET_Combo TYPE-', size=(10,1))],
            [sg.Text("Import Doc Type   :"),sg.Combo(docTypeValues, default_value=docTypeDefaultValue, key='-SET_Combo DOC_TYPE-', size=(20,1))],
            [sg.Text("Import Folder Path:"),sg.Input(key='-IFP-'),sg.FolderBrowse('Select')]]
            )

# ------ Tab3 Definition ------ #
left_col = [[sg.Text('Org Folder'), sg.Input(size=(35,1), enable_events=True ,key='-ORG FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[],
             enable_events=True,
             select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
             size=(40,20),
             horizontal_scroll =True,
             key='-ORG FILE LIST-',
             highlight_background_color = '#87ceeb',
             highlight_text_color = '#000000')]]


center_col = [[sg.Button('>>',key='-File >>-')], [sg.Button('<<',key='-<< File-')]]

right_col = [[sg.Text('To Folder'), sg.Input(size=(35,1), enable_events=True ,key='-TO FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True,
            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            size=(40,20),
            key='-TO FILE LIST-',
            horizontal_scroll =True,
            highlight_background_color = '#87ceeb',
            highlight_text_color = '#000000')]]

t3 = sg.Tab('FileCopys' ,[[sg.Column(left_col),
                        sg.VSeperator(),
                        sg.Column(center_col),
                        sg.VSeperator(),
                        sg.Column(right_col)],
                        [sg.Button('Clear',key='-File Clear-', pad=((800, 0),(0,0)))],
                        [sg.Button('FileCopys',key='-File Copys-', pad=((800, 0),(0,0)))]])

Layout = [[sg.Menu(menu_def, key='menu1')],
         [sg.TabGroup([[t1 ,t2, t3]], size = (900, 470))]]
# +-----------------------------------------------------------------------------------+
# + ウィンドウ作成
# +-----------------------------------------------------------------------------------+
window = sg.Window('-- Folder & File Operation --', Layout, resizable=True, size=(930, 500))

# *====================================================================================
# * プログラム開始
# *====================================================================================
# +-----------------------------------------------------------------------------------+
# + GUIループ
# +-----------------------------------------------------------------------------------+
while True:
    # イベントの読み取り（イベント待ち）
    event, values = window.read()
    # 終了条件（None:クローズボタン）
    if event in (sg.WIN_CLOSED, 'Quit'):
        break
    if event == '_filestable_':
        gen = (i for i in values['_filestable_'])
        for num in gen:
            print(member_list[num][4])

    # 仮登録
    elif event == 'Add':
        # print(len(member_list))
        # 最大行を取得する
        max_row = len(member_list) + 1

        # 選択された取込先フォルダパスを取得する
        folder_path = values['-IFP-']
        typeSectionKey = values['-SET_Combo TYPE-']
        docTypeSectionKey =values['-SET_Combo DOC_TYPE-']
        # 取込先フォルダパスが設定されていれば、行追加
        if typeSectionKey and docTypeSectionKey and folder_path:
            typeSectionValue = configManager.getTypeSectionValue(typeSectionKey)
            docTypeSectionValue = configManager.getDocTypeSectionValue(docTypeSectionKey)
            print(typeSectionValue)
            print(docTypeSectionValue)
            # 新規行を追加　⇒一時仮設定のため、Id（自動採番のため）はNoneとしておく
            member_list.append([str(max_row), typeSectionKey, docTypeSectionKey, folder_path.replace('/', '\\'), '未済', None, typeSectionValue, docTypeSectionValue])
        else:
            # フォルダ未設定の場合は、選択を即すメッセージをポップアップ表示
            sg.popup_error('タイプもしくは、フォルダを選択してください。',title = 'error')
        # Windowウィジェットに対してデータ配列を再設定
        window['_filestable_'].update(values=member_list)

    # 削除処理
    elif event == 'Del':
        # 行選択判定
        if values['_filestable_']:

            # 選択行のセルデータを取得（ジェネレータ）
            gen = (i for i in values['_filestable_'])
            for num in gen:
                # 登録済みの場合、確認後、削除
                if member_list[num][4]:
                    # 削除確認
                    mess = sg.popup_ok_cancel('登録済みのデータですが、No.{}を削除しますか？'.format(member_list[num][0]),title = 'delete confirm')
                    if mess == "OK":
                        print("---選択行:{}----".format(member_list[num][0]))
                        type_name = member_list[num][1]
                        del member_list[num]
                        # 設定リストのNoを再振り直し
                        renumbering()
                        sg.popup_ok('Type={}を削除しました。'.format(type_name),title = 'delete confirm');
                        window['_filestable_'].update(values=member_list)
                    else:
                        break;

                # 未登録の場合、即削除
                else:
                    print("---選択行:{}----".format(member_list[num][0]))
                    type_name = member_list[num][1]
                    del member_list[num]
                    renumbering()
                    sg.popup_ok('Type={}を削除しました。'.format(type_name),title = 'delete results');
                    window['_filestable_'].update(values=member_list)

        # 行未選択の場合、選択メッセージを表示
        else:
            sg.popup_error('削除行を選択してください。',title = 'error')

    # DB反映処理
    elif event == 'Ref' or values['menu1'] == 'Setting Reflection':
        if len(member_list) < 1:
            sg.popup_error('登録データがありません。',title = 'error')

        else:
            mess = sg.popup_ok_cancel('反映処理を実施しますか？',title = 'Reflection confirm')
            if mess == "OK":
                # 設定情報の登録処理
                settingEntityAccess.entityInsert(member_list)
                sg.popup_ok('{}件 正常に反映処理が終了しました。'.format(str(len(member_list))),title = 'Reflection results')
                # 設定エンティティ全件取得
                member_list = settingEntityAccess.entitySearchAll()
                # windowsウィジェット再設定
                window['_filestable_'].update(values=member_list)
            else:
                sg.popup_ok('反映処理を中止しました。',title = 'Reflection stop')

    # 再読み込み処理
    elif event == 'Reload' or values['menu1'] == 'Reload FolderPath':
        #再読み込み実施
        if len(member_list) > 0:
            # 設定エンティティ全件取得
            member_list = settingEntityAccess.entitySearchAll()
            # windowsウィジェット再設定
            window['_filestable_'].update(values=member_list)
            sg.popup_ok('再設定読み込み件数 {}件です。'.format(str(len(member_list))),title='reload results')
        else:
            sg.popup_ok('再設定読み込み件数 0件です。',title = 'reload results')

    # 再ファイルパス読み込み処理
    elif event == 'Data_Reload' or values['menu1'] == 'Reload FilePath':
        #再読み込み実施
        # if len(member_list) > 0:
        row_count = filePathAccess.entityImport()
        # ファイルパスエンティティ全件取得
        data_list = filePathAccess.entitySearchAll()
        # windowsウィジェット再設定
        window['_filestable_data_'].update(values=data_list)

        # DistinctSQL実施　⇒ タイプ区分設定（コンボボックスへ）再設定処理
        # values = filePathAccess.entityDistinctSearchAll()
        typeValues = configManager.getSectionValus('TYPE')
        docTypeValues = configManager.getSectionValus('DOC_TYPE')
        # window['-Data_Combo TYPE-'].update(values=values)
        window['-Data_Combo TYPE-'].update(values=typeValues)
        window['-Data_Combo DOC_TYPE-'].update(values=docTypeValues)
        # sg.popup_ok('再読み込み:{}件／区分設定:{}件 です。'.format(str(len(data_list)-1), str(len(values))),title = 'reloade results')
        sg.popup_ok('再読み込み:{}件 です。'.format(str(len(data_list))),title = 'reloade results')

    # 検索処理
    elif event == 'Data_Search':
        # 条件コンボボックス項目値
        type_section = values['-Data_Combo TYPE-']
        # 条件コンボボックス項目値
        doc_type_section = values['-Data_Combo DOC_TYPE-']
        # 条件ファイル名項目値
        data_file_path_name = values['Data_File_Path_Name']

        # ファイルパスエンティティ検索処理
        data_list = filePathAccess.entitySearch(type_section, doc_type_section, data_file_path_name, configManager)

        window['_filestable_data_'].update(values=data_list)
        sg.popup_ok('検索結果:{}件です'.format(len(data_list)),title = 'search results')

    # 検索クリア処理
    elif event == 'Data_Search_Clear':
        window['-Data_Combo TYPE-'].update("")
        window['-Data_Combo DOC_TYPE-'].update("")
        window['Data_File_Path_Name'].update("")

    # ファイルオープン処理
    elif event == 'FileOpen' or values['menu1'] == 'File':
        # 行選択判定
        if values['_filestable_data_']:

            # 選択行のセルデータを取得（ジェネレータオブジェクト）
            gen = (i for i in values['_filestable_data_'])
            for num in gen:
                # ファイルフルパスを取得
                file_full_path = data_list[num][4]
                # ファイルOPEN確認
                mess = sg.popup_ok_cancel('ファイル：{}を開きますか？'.format(file_full_path),title = 'Confirm to open the file')
                if mess == "OK":
                    print("---選択行:{}----".format(data_list[num][0]))
                    fileOperation.fileOpen(file_full_path)
                else:
                    break;

        # 行未選択の場合、選択メッセージを表示
        else:
            sg.popup_error('行を選択してください。',title = 'error')

    # フォルダオープン処理
    elif event == 'FolderOpen' or values['menu1'] == 'Folder':
        # 行選択判定
        if values['_filestable_data_']:

            # 選択行のセルデータを取得（ジェネレータオブジェクト）
            gen = (i for i in values['_filestable_data_'])
            for num in gen:
                # ファイルフルパスを取得
                file_full_path = data_list[num][4]
                # フルパスよりディレクトリパスを取得
                dir_path = fileOperation.getFolderPath(file_full_path)
                # フォルダOPEN確認
                mess = sg.popup_ok_cancel('フォルダ：{}を開きますか？'.format(dir_path),title = 'Confirm to open the Folder')
                if mess == "OK":
                    print("---選択行:{}----".format(data_list[num][0]))
                    # フォルダOPEN処理
                    fileOperation.folderOpen(dir_path)
                else:
                    break;

        # 行未選択の場合、選択メッセージを表示
        else:
            sg.popup_error('行を選択してください。',title = 'error')

    # ファイルコピー元フォルダが変更されたタイミングで
    # 指定フォルダ内のファイルを取得後、リストボックスに表示
    elif event == '-ORG FOLDER-':
        # コピー元フォルダパス取得
        org_Folder_full_path = values['-ORG FOLDER-']

        # コピー元フォルダ選択判定
        if org_Folder_full_path:
            # コピー元ファイル名配列を取得後、コピー元ファイル名配列（退避）に設定
            org_file_names_bk = fileOperation.getFolderInFiles(Folder_full_path=org_Folder_full_path)

            # Windowウィジェットに対してファイル名配列（退避）を再設定
            window['-ORG FILE LIST-'].update(values=org_file_names_bk)

        else:
            sg.popup_error('コピー元フォルダを選択して下さい',title = 'error')

    # コピー元ファイル ⇒ コピー先ファイル
    elif event == '-File >>-':
        # コピー先ファイル（選択された）を取得⇒退避に格納
        to_file_names_bk = values['-ORG FILE LIST-']

        # コピー先ファイル名リストに設定
        if len(to_file_names_bk) > 0:
            # windowsウィジェットに対して、コピー先ファイル名を退避配列で再設定
            window['-TO FILE LIST-'].update(values=to_file_names_bk)

        else:
            sg.popup_error('コピー元ファイルを選択して下さい',title = 'error')

    # コピー元ファイルを削除
    elif event == '-<< File-':
        # コピー先ファイル名配列取得
        to_files_names = values['-TO FILE LIST-']

        # コピー先を削除するファイル件数判定
        if len(to_files_names) > 0:
            # コピー先リスト分を削除
            for file_name in to_files_names:
                # 退避コピー先ファイル名配列から指定ファイルを削除
                to_file_names_bk.remove(file_name)

            # windowsウィジェットに対して、コピー先ファイル名を退避配列で再設定
            window['-TO FILE LIST-'].update(values=to_file_names_bk)

        else:
            sg.popup_error('コピー先ファイルを選択して下さい',title = 'error')

    # ファイルコピー処理を実施
    elif event == '-File Copys-':
        # コピー元フォルダパス取得
        org_Folder_full_path = values['-ORG FOLDER-']
        # コピー先フォルダパス取得
        to_folder_full_path = values['-TO FOLDER-']

        # コピー先フォルダ設定判定
        if to_folder_full_path:
            # コピー先ファイル（退避）設定判定;
            if len(to_file_names_bk) > 0:

                # 確認ポップアップメッセージ構築
                path_mess = ""
                for Folder_title in [['【コピー元】',org_Folder_full_path],['【コピー先】',to_folder_full_path]]:
                    path_mess = path_mess + '{} \n'.format(Folder_title[0])
                    for to_file_name in to_file_names_bk:
                        path_mess = path_mess + '{}\{}'.format(Folder_title[1], to_file_name) + ' \n'
                    path_mess = path_mess + '\n'

                # ファイルコピー確認ポップアップ表示
                mess = sg.popup_ok_cancel('以下のファイルをコピーしますがよろしいですか？\n {}'.format(path_mess),title = 'to copy file')
                if mess == "OK":
                    # ファイルコピー実行
                    fileOperation.copyFiles(org_Folder_full_path=org_Folder_full_path, to_Folder_full_path=to_folder_full_path, to_file_names=to_file_names_bk)
                    # 完了メッセージ表示
                    sg.popup_ok('{}件のファイルをコピーが完了しました。'.format(str(len(to_file_names_bk))),title = 'file copy completion')
                else:
                    pass
            else:
                sg.popup_error('コピー先ファイルを選択して下さい',title = 'error')
        else:
            sg.popup_error('コピー先フォルダを選択して下さい',title = 'error')

    # ファイルクリア処理を実施
    elif event == '-File Clear-':

        org_file_names_bk.clear()
        to_file_names_bk.clear()

        window['-ORG FOLDER-'].update("")
        window['-TO FOLDER-'].update("")
        # Windowウィジェットに対してファイル名配列（退避）を再設定
        window['-ORG FILE LIST-'].update(values=org_file_names_bk)
        # windowsウィジェットに対して、コピー先ファイル名を退避配列で再設定
        window['-TO FILE LIST-'].update(values=to_file_names_bk)



    # このアプリについて
    elif values['menu1'] == 'About app...':

        sg.popup_ok('＜MIT License＞\n\nFolder & File Operation version 1.01 \n\nCopyright (c) 2021 G-jon FujiYama\n\nThe OS used is Windows only\n',title = 'About app...')
