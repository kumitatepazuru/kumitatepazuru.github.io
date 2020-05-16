# libscipsのプログラムレベルのお話①(α0.0.1)

今回は、自分が作っているライブラリlibscipsについて説明しようと思う。

## 作成経緯

僕達zyo_senチームはこれまでagent2d(gliders2d)を使っていた。しかし、agent2dはC++で僕達の専門(?)はpythonなので解読が大変だった。そして、もとAI教室のチームということもあり、AIで戦わせたかった。でもC++の情報は少ない...さてどうしよう。

そんなときに思いついたのがこのライブラリだった。

agent2dがベースとして使っているのはlibrcscと言うサーバーとの通信等をやってくれているライブラリ。それを自分たちで作ればいいのではないかと思い作ったものだ。幸い、昔にagent2dベースではない手法を使っていたこともあり、それを参考にしながら作成していった。そしてできたのが

**lib**
**s**occer
**c**ommunicate
**i**n
**p**ython
**s**ystem
で**libscips**

だった。

このライブラリは

> 全体の90%以上をサッカーの計算等のプログラムにする

と言うことを目標にしてやっていく予定だ。

## player.pyを見る。

まず、player.pyを見てもらおう。

```python
import json
from socket import socket, AF_INET, SOCK_DGRAM


class analysis:
    def __init__(self, error, analysis_log):
        self.error = error
        self.analysis_log = analysis_log

    def msg_analysis(self, text, log_show=None):
        text = text[0]
        if text[0] == "error":
            text = text[1].replace("_", " ")
            log = "\033[38;5;1m[ERR]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[4m" + text + "\033[0m"
            r = {"type": "error", "value": str(self.error.get(text) + (self.error.get(text) is None))}
        elif text[0] == "init":
            self.no = text[2]
            log = "\033[38;5;10m[OK]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10minit msg.\t\033[4m" + "\033[38;5;11mleft team" * (
                          text[1] == "l") + \
                  "\033[38;5;1mright team" * (text[1] == "r") + "\033[0m\033[38;5;6m no \033[4m" + text[2] + "\033[0m"
            r = {"type": "init", "value": text[:-2]}
        elif text[0] == "server_param" or text[0] == "player_param" or text[0] == "player_type":
            log = "\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10m" + text[0] + " msg.\033[0m"
            r = {"type": text[0], "value": text[1:]}
        elif text[0] == "see" or text[0] == "sense_body":
            log = "\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10m" + text[0] + " msg. \033[38;5;9mtime \033[4m" + text[
                      1] + "\033[0m"
            r = {"type": text[0], "time": int(text[1]), "value": text[2:]}
        elif text[0] == "hear":
            log = "\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10mhear msg. \033[38;5;9mtime \033[4m" + text[1] + "\033[0m " + \
                  "\033[38;5;6mspeaker \033[4m" + text[2] + "\033[0m " + "\033[38;5;13mcontents \033[4m" + text[3] + \
                  "\033[0m"
            r = {"type": "hear", "time": int(text[1]), "speaker": text[2], "contents": text[3]}
        elif text[0] == "change_player_type":
            log = "\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10mhear msg. \033[0m"
            r = {"type": "change_player_type", "value": text[1]}
        else:
            log = "\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10mUnknown return value \033[0m\033[4m" + str(text) + "\033[0m"
            r = {"type": "unknown", "value": text}
        if log_show is None:
            log_show = r["type"] in self.analysis_log
        if log_show:
            print(log)
        return r

    def see_analysis(self, text, hit, log_show=None):
        if type(hit) == str:
            hit = [hit]
        text = text[0]
        for i in text[2:]:
            if i[0] == hit:
                if log_show is None:
                    log_show = hit in self.analysis_log or hit[0] in self.analysis_log
                if log_show:
                    print("\033[38;5;12m[INFO]\t\033[38;5;10mThere was a " + str(
                        hit) + " in the visual information.\033[0m")
                return i[1:]
        if log_show:
            print("\033[38;5;12m[INFO]\t\033[38;5;10mThere was no " + str(hit) + " in the visual information.\033[0m")
        return None


class player_signal(analysis):
    def __init__(self, ADDRESS="127.0.0.1", HOST="", send_log=False, recieve_log=False, analysis_log=("unknown",
                                                                                                      "init", "error")):
        self.ADDRESS = ADDRESS
        self.s = socket(AF_INET, SOCK_DGRAM)
        ok = 0
        i = 0
        print("\033[38;5;12m[INFO]\t\033[38;5;13mSearching for available ports ...\033[0m")
        while ok == 0:
            try:
                self.s.bind((HOST, 1000 + i))
                ok = 1
            except OSError:
                i += 1
        self.recieve_port = 1000 + i
        self.recieve_log = recieve_log
        self.send_log = send_log
        self.analysis_log = analysis_log
        self.no = ""
        self.player_port = 0
        self.error = {"no more player or goalie or illegal client version": 0}
        super().__init__(self.error, self.analysis_log)

    def __del__(self):
        self.s.close()

    def send_msg(self, text, PORT=6000, log=None):
        self.s.sendto((text + "\0").encode(), (self.ADDRESS, PORT))
        self.send_logging(text, PORT, log=log)

    def send_logging(self, text, PORT, log=None):
        if log is None:
            log = self.send_log
        if log:
            print("\033[38;5;12m[INFO]\t" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (self.no != "") + "\033[38;5;10mSend msg.\t" +
                  "\033[38;5;9mPORT \033[4m" + str(self.recieve_port) + "\033[0m\033[38;5;9m → \033[4m" + str(PORT) +
                  "\033[0m\t\033[38;5;6mTEXT \033[4m" + text + "\033[0m")

    def send_init(self, name, goalie=False, version=15, log=None):
        msg = "(init " + name + " (goalie)" * goalie + " (version " + str(version) + "))"
        self.send_msg(msg, log=log)
        r = self.recieve_msg(log=log)
        self.player_port = r[1][1]
        return r

    def send_move(self, x, y, log=None):
        msg = "(move " + str(x) + " " + str(y) + ")"
        self.send_msg(msg, self.player_port, log=log)

    def send_dash(self, power, log=None):
        msg = "(dash " + str(power) + ")"
        self.send_msg(msg, self.player_port, log=log)

    def send_turn(self, moment, log=None):
        msg = "(turn " + str(moment) + ")"
        self.send_msg(msg, self.player_port, log=log)

    def send_turn_neck(self, angle, log=None):
        msg = "(turn_neck " + str(angle) + ")"
        self.send_msg(msg, self.player_port, log=log)

    def send_kick(self, power, direction, log=None):
        msg = "(kick " + str(power) + " " + str(direction) + ")"
        self.send_msg(msg, self.player_port, log=log)

    def recieve_msg(self, log=None):
        msg, address = self.s.recvfrom(8192)
        if log is None:
            log = self.recieve_log
        if log:
            print("\033[38;5;12m[INFO]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[0m\033[38;5;10mGet msg.\t\033[38;5;9mPORT \033[4m" + str(
                self.recieve_port) + "\033[0m\033[38;5;9m ← \033[4m" +
                  str(address[1]) + "\033[0m\t\033[38;5;6mIP \033[4m" + address[0] + "\033[0m")
        return json.loads(msg[:-1].decode("utf-8").replace("  ", " ").replace("(", '["').replace(")", '"]').
                          replace(" ", '","').replace('"[', "[").replace(']"', "]").replace("][", "],[").
                          replace('""', '"')), address
```

156行の短いプログラムだ。これを一つづつ説明していく。

このプログラムは今の所外部ライブラリは使っていない。

また各クラス等の使い方は[libscips WIKI](https://kumitatepazuru.github.io/libscips/jp/#!index.md)を参照してほしい。

## analysisクラス

まず、analysisから、説明していく。

普通は後述のplayer_signalに継承して使われる。ただ見やすくするためにクラスを分けている。

なので一番最初の\_\_init\__関数

```python
def __init__(self, error, analysis_log):
        self.error = error
        self.analysis_log = analysis_log
```

は完全にNameError回避&Pycharm警告出さなくする用。なくても大丈夫。

次のmsg_analysisは引数textを分解して、コマンドの種類を分類し、条件分岐をして扱いやすい辞書型にして返すプログラム。

引数textの中身は

```python
(["see", "0", [["b"], "10", "0"], ...], (127.0.0.1, 6000))
```

こんな感じ。

```python
def msg_analysis(self, text, log_show=None):
        text = text[0]
        if text[0] == "error":
            text = text[1].replace("_", " ")
            log = "\033[38;5;1m[ERR]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[4m" + text + "\033[0m"
            r = {"type": "error", "value": str(self.error.get(text) + (self.error.get(text) is None))}
        elif text[0] == "init":
            self.no = text[2]
            log = "\033[38;5;10m[OK]" + (
                    "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                          self.no != "") + "\t\033[38;5;10minit msg.\t\033[4m" + "\033[38;5;11mleft team" * (
                          text[1] == "l") + \
                  "\033[38;5;1mright team" * (text[1] == "r") + "\033[0m\033[38;5;6m no \033[4m" + text[2] + "\033[0m"
            r = {"type": "init", "value": text[:-2]}
        # --- 条件分岐が続く ---
        
        if log_show is None:
            log_show = r["type"] in self.analysis_log
        if log_show:
            print(log)
        return r
```

コマンドの条件分岐が永遠と続く関数だ。

変数textは解析するもとデータが入っている。なぜ、一番最初に`text = text[0]`が入っているかと言うと上に書いてある引数textの例を見てわかるとおり、元データだと送信元の情報も入っていて邪魔だから消している。

変数logはlog_showまたはself.analysis_logにコマンドが当てはまる場合にその中身が表示される。

変数rはreturnされる辞書型が入っている。



次はsee_analysis。see情報の中に特定のオブジェクトがあるか調べてあったら扱いやすい情報にして返すという関数だ。

```python
def see_analysis(self, text, hit, log_show=None):
    if type(hit) == str:
        hit = [hit]
    text = text[0]
    for i in text[2:]:
        if i[0] == hit:
            if log_show is None:
                log_show = hit in self.analysis_log or hit[0] in self.analysis_log
            if log_show:
                print("\033[38;5;12m[INFO]\t\033[38;5;10mThere was a " + str(
                    hit) + " in the visual information.\033[0m")
            return i[1:]
    if log_show:
        print("\033[38;5;12m[INFO]\t\033[38;5;10mThere was no " + str(hit) + " in the visual information.\033[0m")
    return None
```

最初の

```python
if type(hit) == str:
        hit = [hit]
```

はオブジェクトデータがリスト化されているから、string形式のままで処理をするとエラーが起こってしまう。なのでstring形式の場合はリストに変換する、という部分だ。

あとは、オブジェクトデータをあさってあったらオブジェクト情報を返す。そして、log_showがTrueなら、ログを出すというすごい簡単な関数だ。



## player_signalクラス

次は、player_signalクラスだ。

一番最初の\_\_init\_\_関数

```python
    def __init__(self, ADDRESS="127.0.0.1", HOST="", send_log=False, recieve_log=False, analysis_log=("unknown","init", "error")):
        self.ADDRESS = ADDRESS
        self.s = socket(AF_INET, SOCK_DGRAM)
        ok = 0
        i = 0
        print("\033[38;5;12m[INFO]\t\033[38;5;13mSearching for available ports ...\033[0m")
        while ok == 0:
            try:
                self.s.bind((HOST, 1000 + i))
                ok = 1
            except OSError:
                i += 1
        self.recieve_port = 1000 + i
        self.recieve_log = recieve_log
        self.send_log = send_log
        self.analysis_log = analysis_log
        self.no = ""
        self.player_port = 0
        self.error = {"no more player or goalie or illegal client version": 0}
        super().__init__(self.error, self.analysis_log)
```

は初期設定をしてポートを確保する関数だ。引数をselfにぶち込んで

```python
while ok == 0:
    try:
        self.s.bind((HOST, 1000 + i))
        ok = 1
    except OSError:
    	i += 1
```

ここでOSErrorがでなくなるまで回して空いているポートを探す&確保をする。

そして、

```python
super().__init__(self.error, self.analysis_log)
```

ここで先程のエラー回避initを実行する。

\_\_init\_\_関数はこんな感じ。

次に\_\_del\_\_関数。

```python
def __del__(self):
    self.s.close()
```

プログラムが終了したときなどにポートを開放する関数。一応自動的に開放されるが、念の為。

次はsend_msg関数。

```python
def send_msg(self, text, PORT=6000, log=None):
    self.s.sendto((text + "\0").encode(), (self.ADDRESS, PORT))
    self.send_logging(text, PORT, log=log)
```

この関数はメッセージを送る関数だが、やっていることは、2行目でメッセージを送信、3行目でログを表示する場合は表示（後述のsend_loggingを呼び出し）している。たったそれだけ。

つぎは、先程にも出たsend_logging。ただprint文を使ってログを出しているだけ。

```python
def send_logging(self, text, PORT, log=None):
    if log is None:
        log = self.send_log
    if log:
        print("\033[38;5;12m[INFO]\t" + (
                "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (self.no != "") + "\033[38;5;10mSend msg.\t" +
              "\033[38;5;9mPORT \033[4m" + str(self.recieve_port) + "\033[0m\033[38;5;9m → \033[4m" + str(PORT) +
              "\033[0m\t\033[38;5;6mTEXT \033[4m" + text + "\033[0m")
```

logがNoneだったら\_\_init\_\_関数で指定したsend_logを参照してTrueだったら表示、Trueだったら問答無用で表示するというプログラム。

次は、send_init。名前の通りinitコマンドを送るだけの関数。

```python
def send_init(self, name, goalie=False, version=15, log=None):
    msg = "(init " + name + " (goalie)" * goalie + " (version " + str(version) + "))"
    self.send_msg(msg, log=log)
    r = self.recieve_msg(log=log)
    self.player_port = r[1][1]
    return r
```

ざっくり言うと

2行目で送るmsgを作成

3行目で実際に送る（send_msg関数を呼び出し）

4行目でサーバーのレスポンスを確認（後述のrecieve_msg関数を呼び出し）

5行目で移動コマンド等のサーバーのポートを確認（サーバーのポート6000番は確かinitコマンドしか受け付けない）

6行目で戻り値としてレスポンスを返す。

といった感じ。

次は、send_move・send_dash・send_turn・send_turn_neck・send_kick。プレイヤーを動かす関数。

中身は（send_move)

```python
def send_move(self, x, y, log=None):
    msg = "(move " + str(x) + " " + str(y) + ")"
    self.send_msg(msg, self.player_port, log=log)
```

ただ、msgを作って送る（send_msgを呼び出し）しているだけ。

最後にrecieve_msg。その名の通りサーバーから送られてくる情報を受信する関数。自分の一番の力作関数でもある。

```python
def recieve_msg(self, log=None):
    msg, address = self.s.recvfrom(8192)
    if log is None:
        log = self.recieve_log
    if log:
        print("\033[38;5;12m[INFO]" + (
                "\033[38;5;13mno \033[4m" + self.no + "\033[0m ") * (
                      self.no != "") + "\t\033[0m\033[38;5;10mGet msg.\t\033[38;5;9mPORT \033[4m" + str(
            self.recieve_port) + "\033[0m\033[38;5;9m ← \033[4m" +
              str(address[1]) + "\033[0m\t\033[38;5;6mIP \033[4m" + address[0] + "\033[0m")
    return json.loads(msg[:-1].decode("utf-8").replace("  ", " ").replace("(", '["').replace(")", '"]').
                      replace(" ", '","').replace('"[', "[").replace(']"', "]").replace("][", "],[").
                      replace('""', '"')), address
```

説明をすると

2行目でサーバーからのメッセージ受信

3~8行目で必要ならばログを表示

9~11行目で戻り値として扱いやすい情報にメッセージを直す。

何がすごいかと言うと扱いやすい情報にするのに実質1行で済ませているから。（Pycharmの自動整形で3行になっているだけ。）

なぜ、json.loadsを使っているかと言うと、jsonは以下のように辞書型以外に、リストも扱える。

なので、json.loadsを使い、文字列のリストから、リストに変換してもらっている。

しかし、受信した情報はリスト型に変換できないのでリスト型に変換できるようにしてからリスト型にしている。

```json
[
	{
	"hello":"jobs"
	},
	[
	"contents"
	]
]
```

現段階である機能はこれだけ。もし、アップデートで機能追加がされたら、随時②や③で増やしていこうと思う。

## 最後に

そのうちcszp版も作りたいな...一生終わらなさそうだけど。

ていうか書いていて思ったけれどこの記事のフォント読みやすいしほのぼのしているしブログに最適！すごい合ってる。ちょっと嬉しい。

それでは、またいつか。<br><br><br>



質問等はこちらまで。

https://forms.gle/V6NRhoTooFw15hJdA

また、自分が参加しているRobocup soccer シミュレーションリーグのチームでは参加者募集中です！活動の見学、活動に参加したい方、ご連絡お待ちしております！

[詳しくはこちら](https://kumitatepazuru.github.io/jyo_sen/jp/#!contents/profile.md)
