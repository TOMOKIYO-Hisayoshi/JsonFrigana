import json
from urllib import request

class FuriganaAPI(object):

    __ヘッダ = {
            "Content-Type": "application/json",
            "User-Agent": "Yahoo AppID",
        }

    def __init__(self,appid):
        """
        コンストラクタ
        """
        self.__ヘッダ["User-Agent"]=  self.__ヘッダ["User-Agent"] = "Yahoo AppID: {}".format(appid)

    def __post(self,対象のテキスト,学年):
        URL = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana"

        引数 = {
            "id": "JsonFrigana",
            "jsonrpc": "2.0",
            "method": "jlp.furiganaservice.furigana",
            "params": {
                "q": 対象のテキスト,
                "grade": 1 if 学年 <= 0 else 学年
            }
        }

        エンコード引数 = json.dumps(引数).encode()
        req = request.Request(URL, エンコード引数, self.__ヘッダ)
        with request.urlopen(req) as res:
            body = res.read()
        return body.decode()


    def __ふりがな追記(self, レスポンス,学年):
        レスポンスjson = json.loads(レスポンス)
        単語リスト = レスポンスjson['result']['word']

        ふりがな付き = ''
        for 単語 in 単語リスト:
            if 学年 >= 1 :
                if 'subword' in 単語: # 漢字かな交じり単語 
                    for 詳細単語 in 単語['subword']:
                        ふりがな付き += self.__単語ふりがな結合(詳細単語)
                else :
                    ふりがな付き += self.__単語ふりがな結合(単語) 
            else:
                if 'furigana' in 単語:
                    ふりがな付き += 単語['furigana'] 
                else:
                    ふりがな付き += 単語['surface'] 
        
        return ふりがな付き


    def __単語ふりがな結合(self, 単語json ):
        単語表記 = 単語json['surface']
        ふりがな =''
        if 'furigana' in 単語json:
            ふりがな = 単語json['furigana']
        
        if 単語表記 == ふりがな or ふりがな == '':
            return 単語表記 
        else:
            return  単語表記  + '(' + ふりがな + ')'


    def ふりがなを付ける(self,対象のテキスト,学年):
        レスポンス = self.__post(対象のテキスト,学年)
        ふりがな = self.__ふりがな追記(レスポンス,学年)
        return  ふりがな
