
import json
import time
import os
import pathlib
import sys

def jsonファイル読込(ファイルパス):
    with open(ファイルパス, 'r', encoding='utf-8') as ファイル:
        jsonデータ = json.load(ファイル)
        return jsonデータ

def jsonファイル書込み(ファイルパス, jsonデータ, isAsciiエスケープ):
    with open(ファイルパス, 'a', encoding='utf-8') as ファイル:
        json.dump(jsonデータ, ファイル, indent=4, ensure_ascii = isAsciiエスケープ)

def ふりがなを付ける(appid, 入力ファイル, 出力ファイル, 学年, isAsciiエスケープ):
    
    jsonデータ = jsonファイル読込(入力ファイル)
    総数 =  len(jsonデータ)

    from FuriganaAPI import FuriganaAPI
    furiganaAPI = FuriganaAPI(appid)

    回数 = 0
    前回の時刻 = 0
    for キー in jsonデータ:
        ふりがなナシ = jsonデータ[キー]

        # 1分で300回を超えた場合に制限がかかるので待ち
        待ち時間 = 0.2 - (time.time() - 前回の時刻)
        if 待ち時間 > 0:
            time.sleep(待ち時間)

        ふりがなアリ = furiganaAPI.ふりがなを付ける(ふりがなナシ , 学年)
        前回の時刻 = time.time()

        jsonデータ[キー] = ふりがなアリ

        回数 +=1 
        print(str(回数) + '/' +str(総数) + '：' + ふりがなアリ)

    jsonファイル書込み(出力ファイル, jsonデータ, isAsciiエスケープ)

def 入力待ち():
    print('************************************************************************************')
    print('jsonファイルの値にふりがなを付けます')
    print('')
    print('当アプリは、Yahoo! JAPANが提供するテキスト解析WebAPIのルビ振りを利用します。')
    print('利用者自身で、Yahoo! JAPAN Web APIのアプリケーションIDを取得する必要があります。')
    print('文字コードは UTF-8 のみの対応です。')
    print('')
    print('               Webサービス by Yahoo! JAPAN （https://developer.yahoo.co.jp/sitemap/）')
    print('************************************************************************************')
    print('')
    print('')
    while True:
        appid = input("Yahoo! JAPAN Web APIのアプリケーションIDを入力して下さい : ")
        print('')
        if not appid or appid.isspace():
            print('空白です。もう一度入力して下さい。')
            print('')
        else:
            # 確認
            try:
                from FuriganaAPI import FuriganaAPI
                furiganaAPI = FuriganaAPI(appid)
                furiganaAPI.ふりがなを付ける("漢字かな交じり文にふりがなを振ること。" , 0)

                break
            except Exception as e:
                print('Yahoo! JAPAN Web APIからエラーが返ってきました。もう一度入力して下さい。')
            
    while True:
        入力ファイル = input("ふりがなを付けるjsonファイルのパスを入力して下さい : ")
        print('')
        if not 入力ファイル or 入力ファイル.isspace():
            print('空白です。もう一度入力して下さい。')
            print('')
        elif not os.path.isfile(入力ファイル):
            print('jsonファイルが見つかりません。もう一度入力して下さい。')
            print('')
        else:
            入力ファイル = str(pathlib.Path(入力ファイル).resolve())
            break

    while True:
        出力ファイル = input("出力するjsonファイルのパスを入力して下さい : ")
        print('')
        if not 出力ファイル or 出力ファイル.isspace():
            print('空白です。もう一度入力して下さい。')
            print('')
        elif os.path.isfile(出力ファイル):
            print('jsonファイル既に存在します。もう一度入力して下さい。')
            print('')
        else:
            break

    学年説明リスト = {
            0: "漢字なし。漢字をひらがなに置き換えます。",
            1: "小学1年生向け。漢字にふりがなを付けます。",
            2: "小学2年生向け。1年生で習う漢字にはふりがなを付けません。",
            3: "小学3年生向け。1～2年生で習う漢字にはふりがを付けません。",
            4: "小学4年生向け。1～3年生で習う漢字にはふりがなを付けません。",
            5: "小学5年生向け。1～4年生で習う漢字にはふりがなを付けません。",
            6: "小学6年生向け。1～5年生で習う漢字にはふりがなを付けません。",
            7: "中学生以上向け。小学校で習う漢字にはふりがなを付けません。",
            8: "一般向け。常用漢字にはふりがなを付けません。"
            }
    print('0～8で学年を決めます')
    for キー in 学年説明リスト:
        print('　　'+ str(キー) +'：' + 学年説明リスト[キー])
    print('')
    while True:
        学年 = input("0～8で学年をしてください : ")
        print('')
        if not 学年 or 学年.isspace():
            print('空白です。もう一度入力して下さい。')
            print('')
        elif not 学年 in list(map(str,学年説明リスト.keys())):
            print('0～8以外です。もう一度入力して下さい。')
            print(list(map(str,学年説明リスト.keys())))
        else:
            学年 = int(学年)
            break

    print('')
    Unicodeエスケープ = input("Unicodeエスケープ[Y:する(デフォルト) / N:しない] : ")
    if Unicodeエスケープ in ['N','n']:
        Unicodeエスケープ = 'NO'
    else:
        Unicodeエスケープ = 'YES'

    # 入力値 処理時間の確認
    件数 = len(jsonファイル読込(入力ファイル))
    時間 = round((件数 * 0.25) / 60)

    print('------------------------------------------------------------------------------------')
    print('【引数の確認】')
    print('入力ファイル：' + 入力ファイル)
    print('出力ファイル：' + 出力ファイル)
    print('学年：' + str(学年) +' [' + 学年説明リスト[学年] +']')
    print('Unicodeエスケープ：' + Unicodeエスケープ)
    print('')
    print('【処理時間】')
    print('約'+ str(時間) + '分　'+ str(件数) + '件')
    print('------------------------------------------------------------------------------------')

    print('')
    while True:
        確認 = input("実行する場合は Y を、中止する場合は N を入力してください : ")
        if 確認 in ['Y','y']:
            break
        elif 確認 in ['N','n']:
            print('中止します。')   
            sys.exit()
            break
    
    return appid, 入力ファイル, 出力ファイル, 学年, Unicodeエスケープ

if __name__ == "__main__":
    ret = 入力待ち()
    appid = ret[0]
    入力ファイル = ret[1]
    出力ファイル = ret[2]
    学年 = ret[3]
    isAsciiエスケープ = True if ret[4] == 'YES' else  False
    ふりがなを付ける( appid, 入力ファイル, 出力ファイル, 学年, isAsciiエスケープ)
    
    print('終了しました')