import os
import socketserver
import threading
import time
import shutil
import urllib.parse
from http.server import BaseHTTPRequestHandler

import wx
import wx.richtext
import wx.html2
import re
from wx import stc
import wx.lib.mixins.listctrl as listmix
from bs4 import BeautifulSoup

html = ""
file_path = ""


class HTTPServer_Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(200)
            self.end_headers()
            try:
                with open(urllib.parse.unquote(self.path), "rb") as f:
                    self.wfile.write(f.read())
            except FileNotFoundError as e:
                print("\033[38;5;4m[INFO]", e)
                try:
                    with open(urllib.parse.unquote(self.path[1:]), "rb") as f:
                        self.wfile.write(f.read())
                except FileNotFoundError as e:
                    print("\033[38;5;3m[WARNING]", e)
                    self.wfile.write("404 Not Found!".encode("utf-8"))


def server():
    PORT = 12345
    Handler = HTTPServer_Handler
    try:
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.ThreadingTCPServer(("", PORT), Handler)
        print("\t\033[38;5;10m\033[1m[OK]\033[0mThe web server has been started. Port:", PORT)
        httpd.serve_forever()
    except OSError as e:
        print("\t\033[38;5;3m[WARNING]\033[0mCould not start web server port", PORT, ":" + str(e))
        time.sleep(5)
        server()


th = threading.Thread(target=server)
th.setDaemon(True)
th.start()


class Saveok(wx.Frame):
    def __init__(self, parent, name):
        self.parent = parent
        wx.Frame.__init__(self, parent, -1, "公開をする", size=(500, 400),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        text = wx.StaticText(self, wx.ID_ANY, '公開可能htmlファイルを生成しました。\n'
                                              '最後にサーバー上の今回生成したhtmlファイルを載せる予定の場所と同じ'
                                              'ディレクトリのcontent.jsonに以下の要素を追加してください。')
        self.json = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY, value="""{
    "text":""" + self.parent.title.GetValue() + """,
    "link":""" + name + "\n}")
        sizer1.Add(text, proportion=3, flag=wx.GROW)
        sizer1.Add(self.json, proportion=2, flag=wx.GROW)
        self.SetSizer(sizer1)

    def close(self, _):
        self.Destroy()
        self.parent.Show()


class convert(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "公開をする", size=(500, 150),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.text1 = wx.StaticText(self, wx.ID_ANY, 'ファイル名')
        self.file = wx.TextCtrl(self, -1)
        self.button = wx.Button(self, wx.ID_ANY, '公開できる形式のファイルを作成')
        self.button.Bind(wx.EVT_BUTTON, self.generate_html)
        sizer1.Add(self.file, flag=wx.GROW)
        sizer1.Add(self.button, flag=wx.GROW | wx.TOP, border=10)
        self.SetSizer(sizer1)

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def generate_html(self, _):
        soup = BeautifulSoup(open("index2.html").read(), 'html.parser')
        nt = BeautifulSoup(self.parent.text.GetValue(), 'html.parser')
        # print(nt)
        f = os.path.splitext(os.path.basename(self.file.GetValue()))[0]
        if not os.path.isdir("./html_files/" + f):
            os.makedirs("./html_files/" + f)
        df = []
        for elem in nt.select("img"):
            df.append(elem["src"])
            elem["src"] = f + "/" + os.path.basename(elem.get("src"))
        for elem in nt.select("a"):
            df.append(elem["href"])
            elem["href"] = f + "/" + os.path.basename(elem.get("href"))
        soup.select(".left")[0].append(nt)

        with open("html_files/" + self.file.GetValue() + ".html" * abs(
                len(self.file.GetValue().split(".")) - 2),
                  "w") as file:
            file.write(str(soup.contents[0]))
        for i in df:
            try:
                shutil.copy(i, "html_files/" + f + "/")
            except FileNotFoundError as e:
                print("\033[38;5;3m[WARNING]", e)
        # self.close(None)

        self.Destroy()
        Saveok(self.parent, self.file.GetValue() + ".html" * abs(len(self.file.GetValue().split(".")) - 2)).Show()


class Point(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "注意文の作成", size=(500, 150),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.StaticText(self, wx.ID_ANY, 'タイトル')
        self.title = wx.TextCtrl(self, -1)
        self.button = wx.Button(self, wx.ID_ANY, '注意文を作成')
        self.button.Bind(wx.EVT_BUTTON, self.link_generate)
        sizer2.Add(self.text1, proportion=1, flag=wx.GROW)
        sizer2.Add(self.title, proportion=1, flag=wx.GROW)
        sizer1.Add(sizer2, flag=wx.GROW)
        sizer1.Add(self.button, flag=wx.GROW | wx.TOP, border=10)
        self.SetSizer(sizer1)
        if self.parent.text.GetStringSelection() != "":
            self.title.SetValue(self.parent.text.GetStringSelection())
        else:
            self.title.SetValue("POINT")

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def link_generate(self, _):
        if self.title.GetValue() == "":
            wx.MessageBox('タイトルを入力してください', '注意文の作成')
        else:
            self.parent.text.Replace(self.parent.text.GetSelection()[0], self.parent.text.GetSelection()[1],
                                     "<div class='checkdiv'>\n\t<span class='divtitle'>" + self.title.GetValue() +
                                     "</span>\n\t\n</div>")
            self.close(None)


class Code(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "コード文の作成", size=(500, 300))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.code = stc.StyledTextCtrl(self, wx.ID_ANY)
        self.code.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.code.SetMarginWidth(1, 30)
        self.code.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "fore:#999999")
        self.button = wx.Button(self, wx.ID_ANY, 'コード文を作成')
        self.button.Bind(wx.EVT_BUTTON, self.link_generate)
        sizer1.Add(self.code, proportion=1, flag=wx.GROW)
        sizer1.Add(self.button, flag=wx.GROW | wx.TOP, border=10)
        self.SetSizer(sizer1)

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def link_generate(self, _):
        if self.code.GetValue() == "":
            wx.MessageBox('コードを入力してください', 'コード文の作成')
        else:
            self.parent.text.Replace(self.parent.text.GetSelection()[0], self.parent.text.GetSelection()[1],
                                     '<pre class="prettyprint linenums" style="font-size: 18px;">' +
                                     self.code.GetValue() + "</pre>")
            self.close(None)


class ListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class List(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "リストを作成", size=(500, 150),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.StaticText(self, wx.ID_ANY, '列')
        self.col = wx.SpinCtrl(self, wx.ID_ANY, value="2", min=1, max=9999)
        button = wx.Button(self, wx.ID_ANY, 'リストを作成')
        button.Bind(wx.EVT_BUTTON, self.create_list)
        sizer2.Add(self.text1, proportion=1, flag=wx.GROW)
        sizer2.Add(self.col, proportion=1, flag=wx.GROW)

        sizer1.Add(sizer2, flag=wx.GROW)
        sizer1.Add(button, flag=wx.GROW)
        self.SetSizer(sizer1)

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def create_list(self, _):
        self.parent.text.Replace(self.parent.text.GetSelection()[0], self.parent.text.GetSelection()[1],
                                 "<ul>\n" + "\t<li>\n\t\t\n\t</li>\n" * int(self.col.GetValue()) + "</ul>")
        self.close(None)


class Table(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "表の作成", size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.StaticText(self, wx.ID_ANY, '列')
        self.text2 = wx.StaticText(self, wx.ID_ANY, '行')
        self.col = wx.SpinCtrl(self, wx.ID_ANY, value="2", min=1, max=9999)
        self.row = wx.SpinCtrl(self, wx.ID_ANY, value="3", min=1, max=9999)
        button = wx.Button(self, wx.ID_ANY, '表を作成')
        button.Bind(wx.EVT_BUTTON, self.create_table)
        sizer2.Add(self.text1, proportion=1, flag=wx.GROW)
        sizer2.Add(self.col, proportion=1, flag=wx.GROW)
        sizer3.Add(self.text2, proportion=1, flag=wx.GROW)
        sizer3.Add(self.row, proportion=1, flag=wx.GROW)

        sizer1.Add(sizer2, flag=wx.GROW)
        sizer1.Add(sizer3, flag=wx.GROW)
        sizer1.Add(button, flag=wx.GROW)
        self.SetSizer(sizer1)

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def create_table(self, _):
        self.parent.text.Replace(self.parent.text.GetSelection()[0], self.parent.text.GetSelection()[1],
                                 "<table><tbody>\n\t<tr>\n" + "\t\t<th>\n\t\t\t\n\t\t</th>\n" * self.row.GetValue() +
                                 "\t</tr>\n" + ("\t<tr>\n" + "\t\t<td>\n\t\t\t\n\t\t</td>\n" * self.row.GetValue() +
                                                "\t</tr>\n") * self.col.GetValue() + "</tbody></table>")
        self.close(None)


class Mylink(wx.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.Hide()
        wx.Frame.__init__(self, parent, -1, "リンクの作成", size=(500, 200),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.close)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.StaticText(self, wx.ID_ANY, 'リンク')
        self.text2 = wx.StaticText(self, wx.ID_ANY, '表示テキスト')
        self.link = wx.TextCtrl(self, -1)
        self.value = wx.TextCtrl(self, -1)
        self.button = wx.Button(self, wx.ID_ANY, 'リンクを作成')
        self.button.Bind(wx.EVT_BUTTON, self.link_generate)
        sizer2.Add(self.text1, proportion=1, flag=wx.GROW)
        sizer2.Add(self.link, proportion=1, flag=wx.GROW)
        sizer3.Add(self.text2, proportion=1, flag=wx.GROW)
        sizer3.Add(self.value, proportion=1, flag=wx.GROW)
        sizer1.Add(sizer2, flag=wx.GROW)
        sizer1.Add(sizer3, flag=wx.GROW | wx.TOP, border=10)
        sizer1.Add(self.button, flag=wx.GROW | wx.TOP, border=10)
        self.SetSizer(sizer1)
        if self.parent.text.GetStringSelection() != "":
            self.value.SetValue(self.parent.text.GetStringSelection())

    def close(self, _):
        self.Destroy()
        self.parent.Show()

    def link_generate(self, _):
        if self.link.GetValue() == "":
            wx.MessageBox('リンクを入力してください', 'リンクの作成')
        elif self.value.GetValue() == "":
            wx.MessageBox('表示テキストを入力してください', 'リンクの作成')
        else:
            self.parent.text.Replace(self.parent.text.GetSelection()[0], self.parent.text.GetSelection()[1],
                                     '<a href="' + self.link.GetValue() + '">' + self.value.GetValue() + '</a>')
            self.close(None)


class MyBrowser(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "html generator", size=(1280, 1000))
        self.SetMinSize((1280, 800))
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))
        sizer = wx.BoxSizer(wx.VERTICAL)
        menu = wx.BoxSizer(wx.HORIZONTAL)
        file = wx.BoxSizer(wx.HORIZONTAL)
        zoom = wx.BoxSizer(wx.HORIZONTAL)
        self.browser = wx.html2.WebView.New(self)
        self.title = wx.TextCtrl(self, -1, value="ページのタイトルを入力")

        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.title.SetFont(font)
        self.default_color = self.title.GetForegroundColour()
        self.title.SetForegroundColour("#848484")
        self.title.Bind(wx.EVT_SET_FOCUS, self.On_Text_Active)
        self.title.Bind(wx.EVT_KILL_FOCUS, self.On_Text_Active)
        self.title.Bind(wx.EVT_TEXT, self.change_html)
        self.text = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.text.Bind(wx.EVT_TEXT, self.change_html)
        self.combobox_1 = wx.ComboBox(self, wx.ID_ANY, '見出し・本文',
                                      choices=("p(本文)", "h1(タイトル)", "h2(副題)", "h3(見出し)", "h4", "h5", "h6"),
                                      style=wx.CB_DROPDOWN)
        self.combobox_1.Bind(wx.EVT_COMBOBOX, self.set_tag)
        self.button1 = wx.Button(self, wx.ID_ANY, 'リンクを作成')
        self.button1.Bind(wx.EVT_BUTTON, self.link)
        self.combobox_2 = wx.ComboBox(self, wx.ID_ANY, '表・リスト', choices=("表の作成", "リストの作成"), style=wx.CB_DROPDOWN)
        self.combobox_2.Bind(wx.EVT_COMBOBOX, self.create_list)
        self.button4 = wx.Button(self, wx.ID_ANY, '注意文の作成')
        self.button4.Bind(wx.EVT_BUTTON, self.point)
        self.button5 = wx.Button(self, wx.ID_ANY, 'コード文の作成')
        self.button5.Bind(wx.EVT_BUTTON, self.code)
        self.button6 = wx.Button(self, wx.ID_ANY, 'ファイルの保存')
        self.button6.Bind(wx.EVT_BUTTON, self.save)
        self.button7 = wx.Button(self, wx.ID_ANY, 'ファイルを開く')
        self.button7.Bind(wx.EVT_BUTTON, self.open)
        self.button8 = wx.Button(self, wx.ID_ANY, '画像を載せる')
        self.button8.Bind(wx.EVT_BUTTON, self.img)
        self.button9 = wx.Button(self, wx.ID_ANY, '公開をする')
        self.button9.Bind(wx.EVT_BUTTON, self.convert)
        self.text1 = wx.StaticText(self, wx.ID_ANY, '拡大率')
        self.zoom = wx.ComboBox(self, wx.ID_ANY, "MEDIUM", choices=("TINY", "SMALL", "MEDIUM", "LARGE", "LARGEST"),
                                style=wx.CB_READONLY)
        self.zoom.Bind(wx.EVT_COMBOBOX, self.change_zoom)
        zoom.Add(self.text1, proportion=1, flag=wx.GROW)
        zoom.Add(self.zoom, proportion=5, flag=wx.GROW)

        # menu add
        menu.Add(self.combobox_1, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        menu.Add(self.button1, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        menu.Add(self.combobox_2, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        menu.Add(self.button4, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        menu.Add(self.button5, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        menu.Add(self.button8, proportion=1, flag=wx.GROW | wx.TOP, border=10)

        file.Add(self.button7, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        file.Add(self.button9, proportion=1, flag=wx.GROW | wx.TOP, border=10)
        file.Add(self.button6, proportion=1, flag=wx.GROW | wx.TOP, border=10)

        sizer.Add(zoom, flag=wx.GROW)
        sizer.Add(self.browser, proportion=1, flag=wx.GROW)
        sizer.Add(menu, flag=wx.GROW)
        sizer.Add(self.title, flag=wx.GROW | wx.TOP, border=10)
        sizer.Add(self.text, proportion=1, flag=wx.GROW)
        sizer.Add(file, flag=wx.GROW)
        self.SetSizer(sizer)
        self.change_html(None)

    def change_html(self, _):
        global html
        soup = BeautifulSoup(open("index.html").read(), 'html.parser')

        # title
        nt = BeautifulSoup("<h2>" + self.title.GetValue() + "</h2>", 'html.parser')
        soup.select(".left")[0].append(nt)

        # clear style
        font = self.GetFont()
        font.SetUnderlined(False)
        self.text.SetStyle(0, len(self.text.GetValue()),
                           wx.TextAttr(self.text.GetForegroundColour(),
                                       font=font))

        # tag h1-h6 and p
        find1 = re.finditer(r"(<h[1-6](.|\s)*?>(.|\s)*?</h[1-6]>)|(<p(.|\s)*?>(.|\s)*?</p>)", self.text.GetValue())
        find2 = re.findall(r"(<h[1-6](.|\s)*?>(.|\s)*?</h[1-6]>)|(<p(.|\s)*?>(.|\s)*?</p>)", self.text.GetValue())
        for i, j in zip(find1, find2):
            for k in j:
                size = None
                if len(k) > 1 and k[1] == "p":
                    size = 17
                elif re.match("h[1-6]", k[1:3]) is not None:
                    size = (32, 24, 18.72, 16, 13.28, 10.72)[int(k[2]) - 1]
                if size is not None:
                    font = self.text.GetFont()
                    font.SetPointSize(size)
                    self.text.SetStyle(i.start(), (i.end() - i.start()) + i.start(),
                                       wx.TextAttr(self.text.GetForegroundColour(), font=font))

        # tag a
        nt = BeautifulSoup(self.text.GetValue(), 'html.parser')
        if len(nt.find_all("a")) != 0:
            find = re.finditer(r"(<a(.|\s)*?>(.|\s)*?</a>)", self.text.GetValue())
            if len(re.findall(r"(<a(.|\s)*?>(.|\s)*?</a>)", self.text.GetValue())) != 0 and \
                    len(re.findall(r"(<a(.|\s)*?>(.|\s)*?</a>)", self.text.GetValue())[0]) != 0:

                for i, j in zip(nt.find_all("a"), find):
                    size = None
                    if str(i.parent)[1] == "p":
                        size = 17
                    elif re.match("h[1-6]", str(i.parent)[1:3]) is not None:
                        size = (32, 24, 18.72, 16, 13.28, 10.72)[int(str(i.parent)[2]) - 1]

                    if size is not None:
                        font = wx.Font(size, wx.DEFAULT,
                                       wx.FONTSTYLE_NORMAL, wx.NORMAL)
                    else:
                        font = self.text.GetFont()
                    font.SetUnderlined(True)
                    self.text.SetStyle(j.start(), j.end(), wx.TextAttr((255, 176, 63, 255), font=font))
        # for i in range(len(self.text.GetValue())):
        #     value = list(map(lambda n: n[0], self.html.items()))
        #     for j in range(0, len(value), 2):
        #         print(self.text.GetValue()[i],value[j] >= i >= int(value[j + 1]))
        #         if value[j] >= i >= int(value[j + 1]) or self.text.GetInsertionPoint()-1 == int(value[j + 1]):
        #             print(self.html, i)
        #             tmp = self.html[value[j + 1]]
        #             del self.html[str(self.text.GetInsertionPoint()-1)]
        #             self.html[str(self.text.GetInsertionPoint())] = tmp
        #             font = wx.Font({"p": 17, "h1": 32, "h2": 24, "h3": 18.72, "h4": 16, "h5": 13.28, "h6": 10.72}
        #                            [list(self.html.values())[j]], wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        #             self.text.SetStyle(i,i+1,wx.TextAttr(self.text.GetForegroundColour(),font=font))

        nt = BeautifulSoup(self.text.GetValue(), 'html.parser')
        soup.select(".left")[0].append(nt)

        # print(str(soup.contents[0]))
        html = str(soup.contents[0])
        self.browser.LoadURL("http://localhost:12345/")

    def On_Text_Active(self, _):
        if self.title.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.title.SetFont(font)
            self.title.SetForegroundColour(self.default_color)
            self.title.SetValue('')
        elif self.title.GetValue() == "":
            self.title.SetValue("ページのタイトルを入力")
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.title.SetFont(font)
            self.title.SetForegroundColour('#848484')

    def set_tag(self, _):
        midasi = self.combobox_1.GetSelection()
        if midasi == 0:
            # self.html[self.text.GetInsertionPoint()] = "p"
            # self.html[str(self.text.GetInsertionPoint())] = "p"
            self.text.Replace(self.text.GetSelection()[0], self.text.GetSelection()[1],
                              "<p>" + self.text.GetStringSelection() + "</p>")
        else:
            # self.html[self.text.GetInsertionPoint()] = "h" + str(midasi)
            # self.html[str(self.text.GetInsertionPoint())] = "h" + str(midasi)
            self.text.Replace(self.text.GetSelection()[0], self.text.GetSelection()[1],
                              "<h" + str(midasi) + ">" + self.text.GetStringSelection() + "</h" + str(midasi) + ">")
        self.combobox_1.SetValue("見出し・本文")

    def link(self, _):
        Mylink(self).Show()

    def create_list(self, _):
        if self.combobox_2.GetSelection() == 0:
            Table(self).Show()
        else:
            List(self).Show()
        self.combobox_1.SetValue("表・リスト")

    def point(self, _):
        Point(self).Show()

    def code(self, _):
        Code(self).Show()

    def save(self, _):
        soup = BeautifulSoup(open("index.html").read(), 'html.parser')
        nt = BeautifulSoup(self.text.GetValue(), 'html.parser')
        soup.select(".left")[0].append(nt)
        if file_path == "":
            dialog = wx.FileDialog(None, '保存', style=wx.FD_SAVE,
                                   wildcard="html File (*.html)|*.html|All Files (*.*)|*")
            if dialog.ShowModal() == wx.ID_OK:
                with open(dialog.GetPath(), "w") as f:
                    f.write(str(soup.contents[0]))
        else:
            with open(file_path, "w") as f:
                f.write(str(soup.contents[0]))

    def open(self, _):
        global file_path
        # print(wx.FileSelectorDefaultWildcardStr)
        dialog = wx.FileDialog(None, '開く', style=wx.FD_OPEN,
                               wildcard="html File (*.html)|*.html|All Files (*.*)|*")
        if dialog.ShowModal() == wx.ID_OK:
            try:
                with open(dialog.GetPath(), "r") as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                self.text.SetValue("".join(map(lambda n: str(n), soup.select(".left")[0].contents)))
            except IndexError:
                pass
            else:
                file_path = dialog.GetPath()

    def img(self, _):
        dialog = wx.FileDialog(None, '画像の選択', style=wx.FD_OPEN,
                               wildcard="All Files (*.*)|*")
        dialog.ShowModal()
        if os.path.isfile(dialog.GetPath()):
            self.text.Replace(self.text.GetSelection()[0], self.text.GetSelection()[1],
                              "<img src='" + dialog.GetPath() + "' width=100% vspace='10'>" + self.text.GetStringSelection())

    def convert(self, _):
        convert(self).Show()

    def change_zoom(self, _):
        self.browser.SetZoom(self.zoom.GetSelection())


if __name__ == '__main__':
    app = wx.App()
    dialog = MyBrowser().Show()
    app.MainLoop()
