import tkinter as tk
from tkinter import *
import tkinter.messagebox
import socket, _thread
import json
import winsound

width = 420
height = 520
matrix = [[0 for i in range(19)] for j in range(19)]
Bool_ = True
add_ip = ('localhost', 8712)
match_num = None
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
    send_dict = {"match_num": match_num, "point": point, "sendID": sendID,
                 "color_code": color_code, "MyID": MyID}
    s.sendall(json.dumps(send_dict).encode("utf8"))


def send_isShowconnect():
    """
    向服务发送获取闲置连接请求
    """

    global MyID, match_num
    s.sendall(json.dumps({"isShowConnect": True, "MyId": MyID,
                          "match_num": match_num, "ID": None}).encode("utf8"))


def start_match():
    """
    开始配对
    """

    global color, MyID, sendID
    if MyID == sendID:
        return 0
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
    s.connect(add_ip)
    MyID = json.loads(s.recv(1024).decode(encoding='utf8'))["add_ip"]
    print(MyID)  # MyID为建立连接后的socket内容


def receive_info():
    """
    消息接收处理
    """

    global matrix, table, Bool_, match_num, c, sendID, color
    while True:
        dict_str = s.recv(10240).decode("utf8")
        print(dict_str)
        receive_dict = json.loads(dict_str)
        print(receive_dict)

        if "restart" in receive_dict:
            print("收到restart %s" % receive_dict)
            _init()
            if receive_dict["color"] == 1:
                set_color_white()
            else:
                set_color_black()
                Bool_ = True
            window.butoon_restart["state"] = DISABLED

        elif "drop_successful" in receive_dict:
            tkinter.messagebox.showinfo(message="已经断开连接")
            match_num = None
            Bool_ = True
            _init()
            window.dis_button.destroy()
            window.butoon_restart["state"] = DISABLED

        elif receive_dict["ConnectPool"] is not None:
            create_find_connect(receive_dict)

        elif "successful_connect" in receive_dict:
            if "sendID" in receive_dict:
                sendID = receive_dict["sendID"]
            match_num = receive_dict["match_num"]
            tkinter.messagebox.showinfo(title="successful", message="连接成功！")

            if receive_dict["color"] == 1:
                set_color_white()
                Bool_ = False
            else:
                set_color_black()
                Bool_ = True
            window.butoon_restart["state"] = DISABLED
            window.disconnect()

        elif receive_dict["point"] is not None:
            Bool_ = True
            point = receive_dict["point"]
            if receive_dict["color_code"] == 1:
                table.create_white(point[0], point[1])
            elif receive_dict["color_code"] == 2:
                table.create_black(point[0], point[1])
            if receive_dict["isFalse"] is True:
                tkinter.messagebox.showinfo(title="game over", message="游戏结束")
                window.butoon_restart["state"] = NORMAL
                Bool_ = False


def _init():
    """
    GUI界面初始化
    """

    global table, matrix

    if table is not None:
        del table
    matrix = [[0 for i in range(19)] for j in range(19)]
    table = GameTable(window.root)
    table.table.bind("<Button-1>", table.point)


def restart():
    """
    向服务器发送
    重新开始请求
    """

    global MyID
    s.sendall(json.dumps({"restart": True, "sendID": sendID, "match_num": match_num,
                          "MyID": MyID}).encode("utf8"))
    print("发送restart")


def create_find_connect(dict_):
    """创建连接选择窗口"""

    c = ConnectWindows(dict_["ConnectPool"])
    c.choice()


class GameWindow:
    """
    游戏主体窗口
    """

    def __init__(self):
        self.root = tk.Tk()  # 调用tkinter制作gui
        self.root.title("五子棋(%s)" % MyID)
        # self.root.iconbitmap(r"E:\test\gobang.ico")
        self.root.resizable(width=False, height=False)  # 固定大小
        self.root.geometry("%sx%s+1000+100" % (width, height))  # 位置大小

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
        self.table.create_rectangle(0, 0, width, height - 100, fill="light pink")
        self.table.create_line(20, 20, 400, 20)
        self.table.create_line(20, 20, 20, 400)
        self.table.create_line(400, 400, 20, 400)
        self.table.create_line(400, 400, 400, 20)

        for i in range(20):
            self.table.create_line(20, i * 20, 400, i * 20)
            self.table.create_line(i * 20, 20, i * 20, 400)

    def create_black(self, x, y):
        matrix[y][x] = 2
        x += 1
        y += 1

        self.table.create_oval(x * 20 - 7, y * 20 - 7, x * 20 + 7, y * 20 + 7, fill="black")
        # _thread.start_new_thread(self.music, ())
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
            if event.x > 380 or event.x < 40 or event.y > 380 or event.y < 40 or Bool_ is False:
                pass
            else:
                if event.x % 20 <= 10:
                    x = event.x // 20 - 1
                else:
                    x = event.x // 20
                if event.y % 20 <= 10:
                    y = event.y // 20 - 1
                else:
                    y = event.y // 20
                if matrix[y][x] == 0:

                    if match_num is not None:
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
        # self.top.iconbitmap(r"E:\test\gobang.ico")
        self.top.title("选择连接")
        # self.top.resizable(width=False, height=False)
        self.frame_ = tk.Frame(self.top, width=300, height=200)
        self.connect_list = _pool

    def send_match(self):

        global sendID, match_num, MyID

        if match_num is None:
            if MyID + "(本机)" == self.theLB.get(ACTIVE):
                tk.messagebox.showerror(title="Error", message="请勿点击本ID")
            else:
                sendID = self.theLB.get(ACTIVE)
                start_match()
                print(self.theLB.get(ACTIVE))
        else:
            tk.messagebox.showerror(title="Error", message="您已连接成功\n请勿重复连接")

    def choice(self):
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
        server_init()
        _thread.start_new_thread(receive_info, ())
        window = GameWindow()
        window.create_frame()
        table = GameTable(window.root)
        table.table.bind("<Button-1>", table.point)
        mainloop()
        s.shutdown(2)
        s.close()

    except ConnectionRefusedError:

        error_window = Tk()
        error_window.geometry("200x150+800+300")
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
