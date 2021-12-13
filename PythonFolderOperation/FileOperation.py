import sys, codecs
import os
import glob
import subprocess
import shutil


class FileOperation():

    # ファイルを開く
    def fileOpen(self, file_full_path):
        # print('---fileOpen:{}---'.format(file_full_path))
        if file_full_path:
            subprocess.Popen(['start', file_full_path], shell=True)

    # フォルダを開く
    def folderOpen(self, folder_path):
        # print('---folderOpen:{}---'.format(folder_path))
        if folder_path:
            subprocess.Popen(['explorer', folder_path])

    # フルファイルパスからディレクトリパスのみ取得する
    def getFolderPath(self, file_full_path):

        if file_full_path:
            dir_path = os.path.dirname(file_full_path)
        else:
            dir_path = ""

        return dir_path;

    # フォルダ内ファイル名取得
    def getFolderInFiles(self, Folder_full_path):

        # results = [p for p in glob.glob(r'{}/{}'.format(Folder_full_path,'**'), recursive=False) if os.path.isfile(p)]
        # フォルダパスよりファイル名(拡張子あり)取得
        files = os.listdir(Folder_full_path)
        files_file = [f for f in files if os.path.isfile(os.path.join(Folder_full_path, f))]

        return files_file;

    # フォルダ内ファイル名取得
    def copyFiles(self, org_Folder_full_path, to_Folder_full_path, to_file_names):

        # コピー先ファイル名分をコピー開始
        for to_file_name in to_file_names:
            # print('OR COPY:{} \n TO COPY:{}'.format('{}\{}'.format(org_Folder_full_path, to_file_name),'{}\{}'.format(to_Folder_full_path, to_file_name)))
            shutil.copy2('{}\{}'.format(org_Folder_full_path, to_file_name), '{}\{}'.format(to_Folder_full_path, to_file_name))


# クラス開始処理
#　Pythonファイル直接起動時に呼び出される
if __name__ == '__main__':

    args = sys.argv

    if 3 <= len(args):

        # ファイルパス読み取り処理
        fileOperation = FileOperation()

        if args[1].isdigit():
            if args[1] == '1':
                print('---{}---'.format(args[2]))
                # ファイルパスOPEN処理
                fileOperation.fileOpen(args[2])
            elif args[1] == '2':
                print('---{}---'.format(args[2]))
                # フォルダパス取得処理
                dir_path = fileOperation.getFolderPath(args[2])
                print('---Folder:[{}]---'.format(dir_path))
                # フォルダOPEN処理
                fileOperation.folderOpen(dir_path)
            else:
                # フォルダパス読み取り処理
                fileOperation.folderOpen(args[2])

        else:
            print('Argument is not digit')
    else:
        print('Arguments are too short')
