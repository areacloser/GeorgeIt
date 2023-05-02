import os
import time
import queue
import colorsys
from random import randint
from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
from tkinter.colorchooser import *
from tkinter.messagebox import *
from threading import *
from socket import *

__version__ = "0.1.1.1"

user_config = []
counter = 1

def rgb2hex(r,g,b):
    r, g, b = r/255.0, g/255.0, b/255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return '0x{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def hex2rgb(hexcolor):
    hexcolor = int(hexcolor, base=16) if isinstance(hexcolor, str) else hexcolor
    rgb = ((hexcolor >> 16) & 0xff, (hexcolor >> 8) & 0xff, hexcolor & 0xff)
    return rgb

def rewrite(mode="r"):
    global user_config
    if mode == "r":
        if os.path.exists("userconfig.ini"):
            with open("userconfig.ini", "r") as file:
                user_config = list(map(lambda x: x.strip(), file.readlines()))

        else:
            with open("userconfig.ini", "w") as file:          
                file.write(f"127.0.0.1\n80\nnoname\n{rgb2hex(randint(1,255), randint(1,255), randint(1,255))}")
            with open("userconfig.ini", "r") as file:
                user_config = list(map(lambda x: x.strip(), file.readlines()))
    elif mode == "w":
        with open("userconfig.ini", "w") as file:
            content = "\n".join(user_config)
            file.write(content)
                
def main():
    global user_config, closing
    win = Tk()
    win.title(f"GeorgeIt V{__version__} -- By lanlan2_")
    #win.resizable(0,0)

    rewrite()

    theme_color = StringVar()
    theme_color.set(f"RGB{str(hex2rgb(user_config[3]))}")

    sock = socket(AF_INET, SOCK_STREAM)
    #sock.connect((user_config[0], int(user_config[1])))

    def optsettings(first=False):
        top = Toplevel()
        top.title("基本设置")
        top.resizable(0, 0)
        lfm_1 = LabelFrame(top, text="加入服务器")
        lfm_1.pack(padx=5, pady=5, ipadx=5, ipady=5)
        lfm_2 = LabelFrame(top, text="用户设置")
        lfm_2.pack(padx=5, pady=5, ipadx=5, ipady=5)
        fm_4 = Frame(lfm_2)
        fm_5 = Frame(top)
        fm_5.pack(fill=X, pady=5)

        lab_1 = Label(lfm_1, text="地址：")
        lab_1.grid(row=0, column=0, pady=10)
        lab_2 = Label(lfm_1, text="端口：")
        lab_2.grid(row=1, column=0)
        ent_1 = Entry(lfm_1, width=30)
        ent_1.insert(END, user_config[0])
        ent_1.grid(row=0, column=1)
        ent_2 = Entry(lfm_1, width=30)
        ent_2.insert(END, user_config[1])
        ent_2.grid(row=1, column=1)
        lab_3 = Label(lfm_2, text="昵称：")
        lab_3.grid(row=0, column=0, pady=10)
        ent_3 = Entry(lfm_2, width=30)
        ent_3.insert(END, user_config[2])
        ent_3.grid(row=0, column=1)
        lab_4 = Label(lfm_2, text="主题：")
        lab_4.grid(row=1, column=0)
        fm_4.grid(row=1, column=1, sticky=W)
        can = Canvas(fm_4, width=25, height=25, bg="white", cursor="hand2", highlightthickness=0)
        can.create_rectangle(0,0,24,24, fill="#"+user_config[3][2:])
        can.grid(row=0, column=0, sticky=W)
        lab_5 = Label(fm_4, textvariable=theme_color)
        lab_5.grid(row=0, column=1)
        but_1 = Button(fm_5, text="确定")
        but_1.pack(side=LEFT, padx=10)
        but_2 = Button(fm_5, text="取消", command=top.destroy)
        but_2.pack(side=RIGHT, padx=10)

        def choosetheme(event):
            color = askcolor(title="主题颜色设置", parent=top)
            if str(color[0]) != "None":
                theme_color.set("RGB"+str(color[0]))
                can.create_rectangle(0,0,24,24, fill=color[1])

        def submit():
            #TODO: check
            user_config[0] = ent_1.get()
            user_config[1] = ent_2.get()
            user_config[2] = ent_3.get()
            collist = theme_color.get()[4:-1].split(", ")
            user_config[3] = str(rgb2hex(int(collist[0]), int(collist[1]), int(collist[2])))
            lab_stat.config(text=f"当前用户：{user_config[2]} | 服务器：{user_config[0]}:{user_config[1]} | 房间号：xxx")
            rewrite("w")
            top.destroy()

        can.bind("<Button-1>", choosetheme)
        but_1.config(command=submit)

    def joinroom():
        #sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect((user_config[0], int(user_config[1])))
        except Exception:
            showerror("错误","要连接的服务器不存在或拒绝请求！")
            return
        
        def recv():
            while True:
                msg = sock.recv(1024).decode("utf-8")
                addcon(msg)
        recv_thread = Thread(target=recv)
        #recv_thread.daemon = True
        recv_thread.start()
        
    bar = Menu(win)
    chat = Menu(bar, tearoff=False)
    chat.add_command(label="加入房间", command=joinroom)
    chat.add_command(label="查找聊天记录")
    bar.add_cascade(label="聊天", menu=chat)
    bar.add_command(label="基本设置", command=optsettings)
    more = Menu(bar, tearoff=False)
    more.add_command(label="关于")
    more.add_command(label="更新日志")
    more.add_command(label="使用说明")
    more.add_command(label="特别致谢")
    bar.add_cascade(label="更多", menu=more)
    bar.add_command(label="退出", command=win.destroy)
    win.config(menu=bar)

    fm_1 = Frame(win)
    fm_2 = Frame(win)
    fm_3 = Frame(win)
    fm_1.pack(fill=BOTH, expand=True)
    fm_2.pack(fill=X)
    fm_3.pack(fill=X)

    text = Text(fm_1, relief=FLAT, height=30, state="disabled", bg="whitesmoke")
    text.pack(fill=BOTH, expand=True)

    ent = Entry(fm_2, width=100)
    ent.pack(side=LEFT, fill=X)
    but = Button(fm_2, text="发送")
    but.pack(side=RIGHT)

    lab_stat = Label(fm_3, text=f"当前用户：{user_config[2]} | 服务器：{user_config[0]}:{user_config[1]} | 房间号：xxx")
    lab_stat.pack(side=LEFT)

    lab_time = Label(fm_3, text="当前时间："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    lab_time.pack(side=RIGHT)

    joinroom()

    def addcon(info):
        global counter
        content = info.split("|")
        text["state"] = "normal"
        text.insert(END, content[0]+":"+content[2]+"\n")
        text.tag_add("tag"+str(2*counter-1), str(counter)+".0", str(counter)+"."+str(len(content[0])+1))
        text.tag_add("tag"+str(2*counter), str(counter)+"."+str(len(content[0])+1), str(counter)+".end")
        text.tag_config("tag"+str(2*counter-1), font=("Fixedsys",16,"bold"), foreground="#"+content[1][2:])
        text.tag_config("tag"+str(2*counter), font=("consolas",12), foreground="#"+content[1][2:])
        text["state"] = "disabled"
        counter += 1
        
    def send_msg():
        if ent.get().strip() == "":
            return
        msg = user_config[2]+"|"+user_config[3]+"|"+ent.get().strip()
        ent.delete("0", END)
        addcon(msg)
        sock.send(msg.encode("utf-8"))
    but.config(command=send_msg)

    def close():
        #sock.close()
        win.destroy()
    def update_win():
        lab_time.config(text="当前时间："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        win.update()
        win.after(0,update_win)
    update_win()
    rewrite()
    ent.bind("<KeyPress-Return>", lambda x: send_msg())
    win.protocol("WM_DELETE_WINDOW", close)
    win.mainloop()
    
if __name__ == "__main__":
    main()
