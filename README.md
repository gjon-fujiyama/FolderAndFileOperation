# FolderandFileOperation Version 1.01  
  
設定したフォルダ内のファイルを素早く検索し、フォルダもしくはファイルを開きます。  
  
# DEMO  
  
![demo](https://user-images.githubusercontent.com/95132992/148064114-95d9e6be-14e1-4edd-9de3-3276a1d3226a.gif)
  
# Features
  
①ファイルとフォルダを素早く開く！  
設定したフォルダ内のファイルを検索し、素早くファイルを開くことが出来ます。  
また、ファイルが存在するフォルダを開きます。  
  
②複数のファイルを選択し、一括コピーします！  
コピー元のフォルダ内のファイルを複数選択し、コピー先のフォルダへファイルをコピーできます。  
  
# Requirement
  
python 3.10.0  
PySimpleGUI 4.55.1  
pyinstaller 4.7  
SQLAlchemy 1.4.26  
  
  
# Usage
  
■【リソースの使用方法】  
1)　任意の場所に FolderAndFileOperetion.exe　と同階層に config.ini を配置してください。  
2)　config.ini　は、ファイル検索時に区分属性を2種類設定可能で、それぞれので区分を任意に複数設定可能です。  
  
　　＜＜初期設定＞＞  
　　　[TYPE]  
　　　TYPE0 = ,00,True　←属性区分初期表示（defaultは空白）  
　　　TYPE1 = 標準,01,False  
　　　・  
　　　・  
　　　TYPEX = 区分名,区分値,初期表示設定（True or False)  
  
　　　[DOC_TYPE]  
　　　DOC_TYPE0 = ,00,True　←属性区分初期表示（defaultは空白）  
　　　DOC_TYPE1 = 基本設計,01,False  
　　　・  
　　　・  
　　　DOC_TYPEX = 区分名,区分値,初期表示設定（True or False)  
  
3)　FolderAndFileOperetion.exeをクリック後、起動し、SearchFileListタブもしくは、  
　　Settingタブにて登録・検索・Reload（再呼び込み）を実施すると、
　　同階層にSqliteのDBファイルが自動的に作成されます。  
　　存在しない場合は、自動で新規のDBファイルを作成します。  
  
■【SearchFileListとSettingの使用方法】  
1)　Settingタブにて取り込みたいファイル群をフォルダー単位で指定、かつ属性を指定。  
　　「Add」ボタン押下後、一覧に一時登録します。  
  
2)　一時登録中のデータは、Settingタブ上の一覧には反映が「未済」となっています。  
　　※この時点では、SQLite未登録状態です。  
  
3)　設定タブのフォルダパスを登録するためには、「Reflection」ボタンを押下してください。  
　　※SQLiteに一覧の取込先フォルダパス情報が登録され、反映が「済」となります。  
  
4)　SearchFileListタブを選択し、「Reload」ボタンを押下するとSettingタブにて設定した  
　　フォルダ配下にある全て（サブフォルダ含む）のファイルを検索し、検索結果のファイルを  
　　リスト表示します。  
　　※この時点でSQLiteにファイルリストの情報が自動登録されます。  
  
5)　一覧は、属性およびファイル名（曖昧検索可）で絞って、検索表示させることが可能です。  
  
6)　一覧行を選択後、「FileOpen」ボタンを押下すると選択行のファイルを開きに行きます。  
　　※拡張子をアプリ起動に紐づけ選択してない場合は、起動アプリ選択プロンプトにて起動アプリを選択してください。  
  
7) 一覧行を選択後、「FolderOpen」ボタンを押下すると選択行のファイルが配置されているフォルダがExplorerにて起動し、開きます。  
  
■【FileCopys使用方法】  
1)　FileCopysタブは、左側がコピー元になり、右がコピー先になります。  
2)　左Folderを指定すると右下部のテキストエリアにフォルダ配下のファイル名一覧が表示されます。  
3)　コピー元ファイルを選択（選択したファイルは背景色が水色になります）中央の「＞＞」押下でコピー先のテキストエリアにファイル名が配置されます。  
4)　コピー先フォルダを指定後、「FileCopys」ボタンを押下するとコピー先テキストエリアにあるファイル名で指定したコピー先フォルダにファイルコピーが実行されます。  
  
Copyright (c) 2021 G-jon FujiYama  
  
The OS used is Windows only  
  
# Author

* 作成者 G-jon fujiyama  
* 所属 Script Edite.  

# License

Folderandfileoperation is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

## ////改修履歴/////////  
2021/12/14 Version 1.01  
・検索タブにクリアボタン追加  
・検索タブの検索結果時のナンバリング不具合改修  
・設定タブの削除ボタン不具合改修  
・コピータブのピー元未設定の不具合改修  
・コピータブにクリアボタン追加  
2021/12/20  
・FolderAndFileOperetion.spec commit  
2022/01/04  
・DEMO 動画 COMMIT  

