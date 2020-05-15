# player.player_signal

```python
player.player_signal(self, ADDRESS="127.0.0.1", HOST="", send_log=False, recieve_log=False, analysis_log=("unknown","init", "error"))
```
このクラスはサッカーエージェントを操作するクラスです。

## 引数

| 引数名       | 説明                                                         |
| ------------ | ------------------------------------------------------------ |
| ADDRESS      | 接続するサーバーのIPアドレスを入力します。初期値=127.0.0.1   |
| HOST         | サーバーとの通信に使うIPアドレスを入力します。<br />普通はこのままでいいでしょう。初期値="" |
| send_log     | 送信ログをデフォルトで表示するか指定します。初期値=False     |
| recieve_log  | 受信ログをデフォルトで表示するか指定します。初期値=False     |
| analysis_log | 受信データの解析時にログをデフォルトで表示するかをタプル形式で指定します。<br />タプル内にある名前の受信コマンドのみ表示します。<br />なので、デフォルトではunknownとinitコマンドとerrorコマンドのみが表示されます。<br />初期値=("unknown","init", "error") |

## player_signal.send_msg

```python
player_signal.send_msg(self, text, PORT=6000, log=None)
```

この関数はサーバーにテキストを送信する関数です。デフォルトではPORT 6000番に送信されます。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| text   | サーバーに送信するテキストを指定します。                     |
| PORT   | サーバーのポートを指定します。初期値=6000                    |
| log    | 送信のログを表示するか指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_logging

```python
player_signal.send_logging(self, text, PORT, log=None)
```

この関数は送信のログを表示する関数です。主に内部プログラムで使用されます。

### 引数

| 引数名 | 説明                           |
| ------ | ------------------------------ |
| text   | 送信したテキストを設定します。 |
| PORT   | 送信先のポートを指定します。   |
| log    | ログを表示するか指定します。   |

## player_signal.send_init

```python
send_init(self, name, goalie=False, version=15, log=None)
```

この関数はサーバーにエージェントを登録する関数です。

### 引数

| 引数名  | 説明                                                         |
| ------- | ------------------------------------------------------------ |
| name    | エージェントのチーム名を指定します。<br />同じチーム名がすでに登録されていた場合はそちらのチームに登録されます。<br />その場合エージェントが11人未満である必要があります。 |
| goalie  | 登録するエージェントがゴールキーパーかを決めます。初期値=False |
| version | 対応しているサーバーバージョンを指定します。<br />特に変更しなくていいと思います。初期値=15 |
| log     | initコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_move

```python
send_move(self, x, y, log=None)
```

この関数はサーバーにmoveコマンドを送信する関数です。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| x      | moveする場所のx座標を指定します。                            |
| y      | moveする場所のy座標を指定します。                            |
| log    | moveコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_dash

```python
send_dash(self, power, log=None)
```

この関数はサーバーにdashコマンドを送信する関数です。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| power  | dashパワーを指定します。通常は-100〜100の間で指定します。    |
| log    | dashコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_turn

```python
send_turn(self, moment, log=None)
```

この関数はサーバーにturnコマンドを送信する関数です。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| moment | 回転する角度を指定します。通常は-180〜180の間で指定します。  |
| log    | turnコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_turn_neck

```python
send_turn_neck(self, angle, log=None)
```

この関数はサーバーにturn_neckコマンドを送信する関数です。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| angle  | 回転する角度を指定します。通常は-90〜90の間で指定します。    |
| log    | turn_neckコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.send_kick

```python
send_kick(self, power, direction, log=None)
```

この関数はサーバーにkickコマンドを送信する関数です。

### 引数

| 引数名    | 説明                                                         |
| --------- | ------------------------------------------------------------ |
| power     | キックパワーを指定します。通常は0〜100の間で指定します。     |
| direction | キックする角度を指定します。通常は-180〜180の間で指定します。 |
| log       | kickコマンドが送られたときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## player_signal.recieve_msg

```python
recieve_msg(self, log=None)
```

この関数はサーバーから送られてくる情報を取得、リスト化する関数です。

### 引数

| 引数名 | 説明                                                         |
| ------ | ------------------------------------------------------------ |
| log    | 情報を受信したときにログを表示するかを指定します。<br />Noneを指定するとplayer.player_signalで指定した表示方法になります。初期値=None |

## 使用例

```python
import sys
import libscips.player
import threading


def th(name, goalie):
    sig = libscips.player.player_signal(send_log=False, recieve_log=True,
                                        analysis_log=("hear", "unknown", "init", "error"))
    r = sig.send_init(name, log=True, goalie=goalie)
    if sig.msg_analysis(r)["type"] == "error":
        sys.exit(1)
    sig.send_move(-20, -20, log=True)
    while True:
        sig.recieve_msg()


for i in range(10):
    threading.Thread(target=th, args=["test1", False]).start()
threading.Thread(target=th, args=["test1", True]).start()
for i in range(10):
    threading.Thread(target=th, args=["test2", False]).start()
threading.Thread(target=th, args=["test2", True]).start()
```

## 最後に

これで、player.player_signalの解説は以上です。書き方のサンプルもありますので見ていってもらえればと思います。次はplayer.analysisの解説をしようと思います。

