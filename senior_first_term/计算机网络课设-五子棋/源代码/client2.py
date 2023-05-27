import tkinter as tk
from tkinter import *
import tkinter.messagebox
import socket, _thread
import json
import winsound

width = 420
height = 520
matrix = [[0 for i in range(19)] for j in range(19)]  # 棋盘上（y，x）位置黑白子信息，0为无棋子，1为白棋，2为黑棋
Bool_ = True
add_ip = ('localhost', 8712)
match_num = None  # 对局编号
color = None
sendID = None


def set_color_white():
    """
    设置当前颜色为白棋
    """
    global color
    window.button_color["fg"] = "black"
    window.button_color["bg"] = "white"
    window.button_color["text"] = "白棋"
    window.button_color.place(x=280, y=40)
    color = 1


def set_color_black():
    """
    当前颜色为黑棋
    """
    global color
    window.button_color["fg"] = "white"
    window.button_color["bg"] = "black"
    window.button_color["text"] = "黑棋"
    window.button_color.place(x=280, y=40)
    color = 2


def send_point(point, color_code):
    """
    向服务器发送坐标
    """
    global sendID, match_num, MyID
    print(match_num)
    send_dict = {"match_num": match_num, "point": point, "sendID": sendID,  # 发送内容有对局的id, 棋子在棋盘上的x和y坐标，对手的ip，棋子颜色，本机的ip
                 "color_code": color_code, "MyID": MyID}
    s.sendall(json.dumps(send_dict).encode("utf8"))


def send_isShowconnect():
    """
    向服务发送获取闲置连接请求
    """
    global MyID, match_num  # 发送本机ip，对局id，
    s.sendall(json.dumps({"isShowConnect": True, "MyId": MyID,
                          "match_num": match_num, "ID": None}).encode("utf8"))


def start_match():
    """
    开始配对
    """
    global color, MyID, sendID
    if MyID == sendID:  # 不能自己连接自己
        return 0
        # 发送 想连接的主机ip, 本机ip, 棋子位置为无, 棋子颜色为自己的颜色, 对局ID还未获得
    send_dict = {"ID": sendID, "MyID": MyID, "point": [0, 0],
                 "color_code": color, "match_num": None}
    s.sendall(json.dumps(send_dict).encode("utf8"))
    # match_num = json.loads(s.recv(1024).decode("utf8"))


def server_init():
    """
    初始化连接
    """
    global s, MyID
    s = socket.socket()  # 创建 socket 对象
    s.connect(add_ip)  # 连接到服务器
    MyID = json.loads(s.recv(1024).decode(encoding='utf8'))["add_ip"]  # 从服务器获取本机ip
    print(MyID)  # MyID为建立连接后的socket内容


def receive_info():
    """
    消息接收处理
    """
    global matrix, table, Bool_, match_num, c, sendID, color
    while True:  # 保持接收信息
        dict_str = s.recv(10240).decode("utf8")
        print(dict_str)
        receive_dict = json.loads(dict_str)
        print(receive_dict)

        #  对收到的信息解析
        #  如果包含重开信息 重新设置棋子颜色
        if "restart" in receive_dict:
            print("收到restart %s" % receive_dict)
            _init()
            if receive_dict["color"] == 1:
                set_color_white()
            else:
                set_color_black()
                Bool_ = True
            window.butoon_restart["state"] = DISABLED
        #  接收到断开连接
        elif "drop_successful" in receive_dict:
            tkinter.messagebox.showinfo(message="已经断开连接")
            match_num = None
            Bool_ = True
            _init()
            window.dis_button.destroy()
            window.butoon_restart["state"] = DISABLED
        #  连接池不为空 提供连接池ip选择窗口
        elif receive_dict["ConnectPool"] is not None:
            create_find_connect(receive_dict)
        #  收到连接成功的状态，如果有发送方ip，即自己是被连接的一方，获取发送方ip，   否则， 获取对局ID
        elif "successful_connect" in receive_dict:
            if "sendID" in receive_dict:
                sendID = receive_dict["sendID"]
            match_num = receive_dict["match_num"]
            tkinter.messagebox.showinfo(title="successful", message="连接成功！")
            # 根据收到的棋子颜色，选择另一种颜色
            if receive_dict["color"] == 1:
                set_color_white()
                Bool_ = False
            else:
                set_color_black()
                Bool_ = True
            window.butoon_restart["state"] = DISABLED
            window.disconnect()
            #  收到下棋位置信息， 在point位置放置合适颜色的棋子
        elif receive_dict["point"] is not None:
            Bool_ = True
            point = receive_dict["point"]
            if receive_dict["color_code"] == 1:
                table.create_white(point[0], point[1])
            elif receive_dict["color_code"] == 2:
                table.create_black(point[0], point[1])
                #  如果收到对局结束信息
            if receive_dict["isFalse"] is True:
                tkinter.messagebox.showinfo(title="game over", message="游戏结束")
                window.butoon_restart["state"] = NORMAL
                Bool_ = False


def _init():
    """
    棋盘界面初始化
    """
    global table, matrix

    if table is not None:
        del table
    matrix = [[0 for i in range(19)] for j in range(19)]
    table = GameTable(window.root)
    table.table.bind("<Button-1>", table.point)


def restart():
    """
    向服务器发送重新开始请求 发送信息有  重开标志位、对方ip、对局id、本机ip、
    """
    global MyID
    s.sendall(json.dumps({"restart": True, "sendID": sendID, "match_num": match_num,
                          "MyID": MyID}).encode("utf8"))
    print("发送restart")


def create_find_connect(dict_):
    """创建连接选择窗口、dict_为服务器发送的数据包、抽取其中连接池信息"""
    c = ConnectWindows(dict_["ConnectPool"])
    #  调用函数绘制窗口
    c.choice()


class GameWindow:
    """
    游戏主体窗口
    """

    def __init__(self):
        self.root = tk.Tk()  # 调用tkinter制作gui
        self.root.title("五子棋(%s)" % MyID)
        self.root.resizable(width=False, height=False)  # 固定大小
        self.root.geometry("%sx%s+200+100" % (width, height))  # 位置大小

    def create_frame(self):
        self.frame = tk.Frame(self.root, width=width, height=100, bg='light blue')
        self.butoon_start = tk.Button(self.frame, bg="light yellow", text="开始游戏",
                                      font=("微软雅黑", 10))
        self.butoon_start.place(x=10, y=40)
        self.butoon_restart = tk.Button(self.frame, bg="light yellow", text="重新开始",
                                        font=("微软雅黑", 10), command=restart,
                                        state=DISABLED)
        self.butoon_restart.place(x=100, y=40)
        self.button_color = tk.Button(self.frame, fg="black", bg="white", text="     ",
                                      font=("微软雅黑", 10),
                                      state=DISABLED)
        button_showpool = tk.Button(self.frame, fg="black", bg="light yellow", text="显示连接池",
                                    font=("微软雅黑", 10),
                                    command=send_isShowconnect)
        button_showpool.place(x=320, y=40)

        self.frame.place(x=0, y=0)

    def disconnect(self):
        self.dis_button = tk.Button(self.frame, fg="black", bg="white", text="断开连接", font=("微软雅黑", 10),
                                    command=self.dis_buttonclean)
        self.dis_button.place(x=180, y=40)

    def dis_buttonclean(self):
        global s, match_num
        s.sendall(json.dumps({"match_num": match_num, "disconnect": True}).encode("utf8"))


class GameTable:
    """
    游戏桌区域
    """

    def __init__(self, frame):
        self.table = tk.Canvas(frame, width=width, height=height, bd=0, highlightthickness=0)
        self.table.place(x=0, y=100)
        #  棋盘背景颜色，棋盘大小（根据线段两端点xy坐标）
        self.table.create_rectangle(0, 0, width, height - 100, fill="light yellow")
        self.table.create_line(20, 20, 400, 20)
        self.table.create_line(20, 20, 20, 400)
        self.table.create_line(400, 400, 20, 400)
        self.table.create_line(400, 400, 400, 20)
        #  画20*20
        for i in range(20):
            self.table.create_line(20, i * 20, 400, i * 20)
            self.table.create_line(i * 20, 20, i * 20, 400)

    #  下黑棋，更新棋盘matrix信息
    def create_black(self, x, y):
        matrix[y][x] = 2  # 该位置为黑棋
        x += 1
        y += 1
        #  画棋子
        self.table.create_oval(x * 20 - 7, y * 20 - 7, x * 20 + 7, y * 20 + 7, fill="black")
        # winsound.PlaySound(r"C:\Users\yuanhuanfa\Desktop\wuziqi\heng.wav", flags=1)

    def create_white(self, x, y):
        matrix[y][x] = 1
        x += 1
        y += 1
        self.table.create_oval(x * 20 - 7, y * 20 - 7, x * 20 + 7, y * 20 + 7, fill="white")
        # winsound.PlaySound(r"C:\Users\yuanhuanfa\Desktop\wuziqi\aaa.wav", flags=1)

    def point(self, event):

        global matrix, Bool_, color

        if Bool_:
            #  判断下棋位置合法 且可以下棋
            if event.x > 380 or event.x < 40 or event.y > 380 or event.y < 40 or Bool_ is False:
                pass
            else:
                #  求得下棋坐标
                if event.x % 20 <= 10:
                    x = event.x // 20 - 1
                else:
                    x = event.x // 20
                if event.y % 20 <= 10:
                    y = event.y // 20 - 1
                else:
                    y = event.y // 20
                if matrix[y][x] == 0:  # 该位置无棋子

                    if match_num is not None:  # 存在该对局
                        if color == 1:
                            self.create_white(x, y)
                        else:
                            self.create_black(x, y)
                        send_point(point=(x, y), color_code=color)
                        Bool_ = False
                    else:
                        tk.messagebox.showwarning(title="提示", message="请先进行连接")


class ConnectWindows:
    """
    选择连接窗口
    """

    def __init__(self, _pool):
        self.top = tk.Toplevel(width=300, height=330)
        self.top.resizable(width=False, height=False)
        self.top.title("选择连接")
        # self.top.resizable(width=False, height=False)
        self.frame_ = tk.Frame(self.top, width=300, height=200)
        self.connect_list = _pool

    def send_match(self):

        global sendID, match_num, MyID

        if match_num is None:
            if MyID + "(本机)" == self.theLB.get(ACTIVE):  # 禁止连接自己
                tk.messagebox.showerror(title="Error", message="请勿点击本ID")
            else:
                sendID = self.theLB.get(ACTIVE)  # 向需要连接的ip发送信息，开始配对
                start_match()
                print(self.theLB.get(ACTIVE))
        else:
            tk.messagebox.showerror(title="Error", message="您已连接成功\n请勿重复连接")

    def choice(self):  # 连接池窗口绘制
        self.sb = tk.Scrollbar(self.frame_)
        self.sb.pack(side=RIGHT, fill=Y)
        self.theLB = tk.Listbox(self.frame_, setgrid=True, yscrollcommand=self.sb.set,
                                font=("微软雅黑", 14), width=25)
        self.theLB.pack(side=LEFT, fill=Y)

        for item in self.connect_list:
            if MyID == item:
                self.theLB.insert(END, item + "(本机)")
            else:
                self.theLB.insert(END, item)
        self.sureButton = Button(self.top, text="确认连接", command=self.send_match,
                                 font=("微软雅黑", 14))
        self.sureButton.place(x=20, y=280)
        self.flushButton = Button(self.top, text="关闭", command=self.top.destroy,
                                  font=("微软雅黑", 14))
        self.flushButton.place(x=150, y=280)
        self.sb.config(command=self.theLB.yview)
        self.frame_.place(x=0, y=0)


if __name__ == '__main__':
    try:
        server_init()  # 初始化连接，为自己创建socket对象，连接到服务器，并且接收服务器信息
        _thread.start_new_thread(receive_info, ())  # 根据服务器返回信息，创建新线程
        window = GameWindow()  # 创建棋盘
        window.create_frame()
        table = GameTable(window.root)
        table.table.bind("<Button-1>", table.point)  # 绑定单机鼠标左键时获得点击信息
        mainloop()  # 监控组件变化，更新窗口
        s.shutdown(2)  # 关闭socket连接，2代表禁止读入写出
        s.close()  # 关闭socket标识符

    except ConnectionRefusedError:

        error_window = Tk()
        error_window.geometry("200x150+800+300")  # 弹窗
        error_window.title("错误")
        error_window.resizable(width=False, height=False)
        CV = tk.Canvas(width=80, height=80)
        x = 5
        y = 5
        CV.place(x=0, y=25)
        CV.create_oval(x, y, 60 - x, 60 - y, fill="red")
        CV.create_line(x + 15, y + 15, 60 - x - 15, 60 - y - 15, fill="white", width=6)
        CV.create_line(60 - x - 15, x + 15, y + 15, 60 - y - 15, fill="white", width=6)
        lab = Label(text="服务器未开启。。。", font=("微软雅黑", 14))
        lab.place(x=70, y=30)
        button = Button(text="确认", font=("微软雅黑", 14), width=5,
                        command=lambda: error_window.quit())
        button.place(x=75, y=100)
        error_window.mainloop()
