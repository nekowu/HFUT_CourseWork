import socket
from threading import Thread
import json
import random
import numpy as np

ADDRESS = ('localhost', 8712)  # 绑定地址

g_socket_server = None  # 负责监听的socket

# 连接池，存储当前请求连接的客户端的socket，上限为5，存储方式为字典类型，一个IP地址端口号为键，对应的值为该地址对应的客户端socket
g_conn_pool = {}
# 棋盘池，存储不同客户端对局的棋盘状态信息
matrix_pool = {}
# 配对池，存储每一场进行中的对局，以及对局双方的地址和对应的socket
match_pool = {}


# 结束某场对局，num为对局的在配对池中的编号
def drop_match(num):
    global g_conn_pool, matrix_pool, matrix_pool
    match_list = list(match_pool[num].items())  # match_pool[num]中包含第num场对局双方的IP地址端口号和对应客户端的socket
    # match_list[0][0]是其对局双方第一方的IP地址端口号，match_list[0][1]是对应的socket
    g_conn_pool[match_list[0][0]] = match_list[0][1]
    g_conn_pool[match_list[1][0]] = match_list[1][1]  # 同上，不过返回的是另一方的信息
    # 向对局双方第一方发送对局结束的消息(断开连接)
    match_list[0][1].sendall(json.dumps({"drop_successful": True}).encode("utf8"))
    # 向对局双方的另一方发送对局结束的消息(断开连接)
    match_list[1][1].sendall(json.dumps({"drop_successful": True}).encode("utf8"))
    matrix_pool.pop(num)  # 弹出棋盘池中对应对局的棋盘信息
    match_pool.pop(num)  # 弹出配对池中对应对局的信息
    print("drop successful")  # 输出提示信息表示对局成功结束


# 用于判断胜利，参数为刚刚下的那一步的位置，刚刚下的那一步的旗子的颜色，以及棋盘状态
def judge(x, y, color_code, matrix):
    v = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]]  # 表示棋子周围的八个方向
    # 一对一对的取出两个方向，依次是上下，左右，右上左下，左上右下
    for i in range(0, len(v) - 1, 2):
        count_1 = 0  # 其中一个方向的棋子计数
        # 另一个方向的棋子计数，因为初始位置的，即刚刚下的那一步会被算两次，所以从-1开始计数
        count_2 = -1
        x_ = x
        y_ = y  # 从刚下的那一步开始往一个方向统计连着的棋子数
        while ((19 > x_ >= 0 and 19 > y_ >= 0) and matrix[y_][x_] == color_code):  # 判断位置不超过棋盘大小且与刚下的那一步棋子同色
            x_ += v[i][0]
            y_ += v[i][1]  # 满足条件则继续往该方向搜寻
            count_1 += 1  # 并另棋子计数+1
        x_ = x
        y_ = y  # 从刚下的那一步开始往另一个方向统计连着的棋子数
        while ((19 > x_ >= 0 and 19 > y_ >= 0) and matrix[y_][x_] == color_code):  # 同上
            x_ += v[i + 1][0]
            y_ += v[i + 1][1]  # 同上
            count_2 += 1  # 同上

        if count_1 + count_2 >= 5:  # 最后判断总数，连在一起的棋子数目是否大于等于5，即下棋方是否胜利
            print("True")  # 输出提示信息
            return True  # 返回True


def init():  # 初始化服务器
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket对象
    g_socket_server.bind(ADDRESS)  # 绑定对应的地址
    g_socket_server.listen(5)  # 设置最大等待数
    print("服务端已启动，等待客户端连接...")  # 输出提示信息


def accept_client():  # 用于接受客户端的连接请求
    while True:
        client, _ = g_socket_server.accept()  # 接收到的客户端信息,为其创建socketID
        g_conn_pool[_[0] + ":" + str(_[1])] = client  # 在连接池中创建对应客户端的项目，IP号：端口号，值为对应的客户端socket对象
        # 将该客户端信息作为参数传给message_handle函数并创建一个线程管理该客户端
        thread = Thread(target=message_handle, args=(client, _,))
        thread.setDaemon(True)  # 当前客户端线程设置为守护线程，主线程结束时直接不检查直接中断所有子线程，不等待子线程结束
        thread.start()  # 客户端线程开始运行


def ismatch(into):  # 用于在配对池中新建一场对局，参数为请求建立对局的客户端发来的消息
    global g_conn_pool, matrix_pool, match_pool
    if into["ID"] in g_conn_pool:  # 如果发送信息的客户端在连接池中
        match_index = len(match_pool)  # 新对局编号等于配对池中已有对局数量
        # 在配对池中新建对局，对局编号为match_index,包含两组键值对，前者为发出对局请求的客户端信息，后者为接受请求的客户端信息
        match_pool[match_index] = {into["ID"]: g_conn_pool[into["ID"]], into["MyID"]: g_conn_pool[into["MyID"]]}
        g_conn_pool.pop(into["ID"])  # 弹出连接池中发出对局请求的客户端信息
        g_conn_pool.pop(into["MyID"])  # 弹出连接池中接受请求的客户端信息
        return match_index  # 返回对局编号
    else:
        pass


def massage_match(bytes_, client, myid):  # 用于与另一客户端建立对局，参数为另一客户端发来的消息，自身的socket对象，自身的地址
    into = json.loads(bytes_.decode(encoding="utf8"))  # 将接受到的json类型的数据转换为python对应的类型
    if into["ID"] in g_conn_pool:  # 如果发送信息的客户端在连接池中
        match_num = ismatch(into)  # 建立对局并获取对局编号
        color = random.randint(1, 2)  # 随机选一个颜色
        # 向接受请求的客户端发送对局编号，离开连接池，对局建立成功，以及棋子颜色这些信息
        client.sendall(json.dumps(
            {"match_num": match_num, "ConnectPool": None, "successful_connect": True, "color": color}).encode("utf8"))
        # 向发送请求的客户端发送对局编号，离开连接池，对局建立成功，以及棋子颜色这些信息
        match_pool[match_num][into["ID"]].sendall(
            json.dumps({"match_num": match_num, "ConnectPool": None, "successful_connect": True, "sendID": myid,
                        "color": 3 - color}).encode("utf8"))
        matrix_pool[match_num] = np.zeros((19, 19), int)  # 初始化对应对局的棋盘，清空棋盘信息


def Gobang_IO(input_json):  # 用于更新棋盘并判断胜负，参数为接收到的信息
    # 根据接受的信息在棋盘对应位置设置对应颜色的棋子 拆分收到的字典
    matrix_pool[input_json["match_num"]][input_json["point"][1]][input_json["point"][0]] = input_json["color_code"]
    # 调用函数判断下完这一步后下棋方是否取得胜利
    isFalse = judge(input_json["point"][0], input_json["point"][1], input_json["color_code"], matrix_pool[
        input_json["match_num"]])
    sendto_kh = {  # 设置准备发送的信息，包括对局是否结束(胜利),下棋位置，棋子颜色，以及是否处于连接池中这些信息
        "isFalse": isFalse, "point": (input_json["point"][0], input_json["point"][1]),
        "color_code": input_json["color_code"], "ConnectPool": None}
    if isFalse:  # 如果游戏结束，即下棋方取得胜利
        # 向接受信息的客户端发送准备好的信息
        match_pool[input_json["match_num"]][input_json["MyID"]].sendall(json.dumps(sendto_kh).encode("utf8"))
        # 向发送信息的客户端发送准备好的信息
    match_pool[input_json["match_num"]][input_json["sendID"]].sendall(json.dumps(sendto_kh).encode("utf8"))


# 用于处理展示等待对局的客户端信息的信息，参数为接收到的信息
def SendConnectPool(input_json):
    try:
        sendto_kh = {"ConnectPool": list(g_conn_pool.keys())}  # 获取当前连接池中所有客户端的地址信息
        # 向发出请求的客户端发送连接池中所有客户端的地址信息
        g_conn_pool[input_json["MyId"]].sendall(json.dumps(sendto_kh).encode("utf8"))
    except KeyError:  # 出现KeyError，即发出请求的客户端不在连接池中
        sendto_kh = {"ConnectPool": list(g_conn_pool.keys())}  # 获取当前连接池中所有客户端的地址信息
        # 从连接池中找到发出请求的客户端并发送对应信息
        match_pool[input_json["match_num"]][input_json["MyId"]].sendall(json.dumps(sendto_kh).encode("utf8"))


def send_restart(receive_json):  # 用于处理重新开始游戏的请求，参数为接收到的信息
    match_num = receive_json["match_num"]  # 获取对局编号
    matrix_pool[match_num] = np.zeros((19, 19), int)  # 将对应对局的棋盘信息清空
    color = random.randint(1, 2)  # 随机确定一个颜色
    # 向发出请求的客户端发送重新开始的信息，并设置其在新的一局中的棋子颜色
    match_pool[match_num][receive_json["MyID"]].sendall(json.dumps({"restart": True, "color": color}).encode("utf8"))
    # 向对局中另一个客户端发送重新开始的消息，并设置其在新的一局中的棋子颜色
    match_pool[match_num][receive_json["sendID"]].sendall(
        json.dumps({"restart": True, "color": 3 - color}).encode("utf8"))


# 用于处理客户端信息的线程，参数为客户端socket对象和其IP地址：端口号
def message_handle(client, add_ip):
    global ISMATCH
    Myadd_ip = add_ip[0] + ":" + str(add_ip[1])  # 将地址转化为一整个字符串
    sendto_kh = {"add_ip": Myadd_ip, "code": True}  # 设置要发送的消息，为字典类型，包含地址和控制信息
    client.sendall((json.dumps(sendto_kh)).encode(encoding='utf8'))  # 将字典类型转化为json格式用于数据传输

    while True:  # 持续处理各种消息直到线程被强制终止
        bytes_ = client.recv(1024)  # 接受长为1024字节的数据
        # 将接受到的json类型的数据转换为python对应的类型,input_json为字典类型
        input_json = json.loads(bytes_.decode(encoding="utf8"))
        if "restart" in input_json:  # 如果接受的信息中包含restart，即接收到了重新开始的信息
            send_restart(input_json)
        elif "isShowConnect" in input_json:  # 如果接受的信息中包含isShowConnect，即接收到了展示等待对局的客户端信息的信息
            SendConnectPool(input_json)
        elif input_json["match_num"] is None:  # 如果接受的信息中的对局编号为None，说明发送信息的客户端未处在对局状态并请求进行对局
            massage_match(bytes_, client, Myadd_ip)
        elif "disconnect" in input_json:  # 如果接受的信息中包含disconnect，说明发送信息的客户端请求断开连接，即结束对局
            drop_match(input_json["match_num"])
        elif input_json["point"] is not None:  # 如果接受的信息中下棋信息不为空，则根据该信息更新棋盘
            Gobang_IO(input_json)


if __name__ == '__main__':  # 主函数（线程）
    init()  # 初始化服务器
    thread = Thread(target=accept_client)  # 对用于接受客户端连接请求的函数建立一个线程
    thread.setDaemon(True)  # 设置其为守护线程，主线程结束时直接不检查直接中断所有子线程，不等待子线程结束
    thread.start()  # 开启线程
    while True:
        cmd = input("""--------------------------  
输入1:查看当前在线人数
输入2:关闭服务端
""")  # 输出提示信息，向服务器输入不同数字提供不同服务
        if cmd == '1':  # 获取当前在线人数
            print("--------------------------")
            print("当前在线人数：", len(g_conn_pool))
        elif cmd == '2':  # 关闭服务器，结束主线程
            exit()
