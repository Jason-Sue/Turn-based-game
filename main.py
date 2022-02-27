"""
这里是主程序，定义窗口类，进入窗口后点击开始游戏即开始
点击开始游戏，调用游戏体
"""

import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import game_body


# 游戏欢迎界面，使用tkinter制作
class BaseRoot:
    name = None
    num = 1  # 玩家选择的角色id
    root = tk.Tk()

    def __init__(self):
        BaseRoot.root.title('欢迎')
        BaseRoot.root.geometry('900x320')

        Welcome()


class Welcome:

    def __init__(self):
        BaseRoot.root.title('欢迎')
        BaseRoot.root.geometry('900x320')
        self.frame = tk.Frame(BaseRoot.root)
        self.frame.pack()
        self.bm = ImageTk.PhotoImage(file='./images/苏钊之光.png')
        l_img = tk.Label(self.frame, image=self.bm)
        l_img.pack()
        # 按键
        self.t1 = tk.Button(
            self.frame, width=40, height=2, text='进入游戏', font=8, fg='black', command=self.game_start, bg='#F0FFFF'
        ).pack()
        self.t2 = tk.Button(
            self.frame, width=40, height=2, text='退出游戏', font=8, fg='black', command=self.drop, bg='#F0FFFF'
        ).pack()

    @staticmethod
    def drop():
        BaseRoot.root.quit()

    def game_start(self):
        self.frame.destroy()
        Choice()


class Choice:
    # 第一个是人机，其他是玩家选择的角色对应的属性，这里的类属性是为了显示给玩家，model里的类属性是游戏体使用的，为了避免导入文件获取该数据，这里选择复制
    hp = [2420, 2200, 2100, 2500, 2100, 2200, 2310, 2342, 2600, 2300, 2010, 2300, 1985, 2420]
    mp = [540, 530, 533, 560, 600, 585, 562, 560, 510, 542, 580, 523, 620, 540]
    attack = [125, 120, 122, 132, 135, 120, 125, 124, 130, 132, 133, 120, 132, 133]
    defence = [118, 110, 120, 132, 120, 111, 120, 120, 112, 118, 121, 132, 120, 119]

    def __init__(self):
        BaseRoot.root.title('人物选择')
        BaseRoot.root.geometry('760x610')
        self.frame = tk.Frame(BaseRoot.root)
        self.frame.pack()

        self.text1 = tk.Label(
            self.frame, height=2, text='请点击您要选择的角色', font=8, fg='black', anchor='w'
        ).grid(row=0, columnspan=2)

        # 角色列表
        role1 = ImageTk.PhotoImage(file='./head/1.png')
        tk.Button(self.frame, image=role1, command=lambda: self.role(1)).grid(row=1, column=0)
        role2 = ImageTk.PhotoImage(file='./head/2.png')
        tk.Button(self.frame, image=role2, command=lambda: self.role(2)).grid(row=1, column=1)
        role3 = ImageTk.PhotoImage(file='./head/3.png')
        tk.Button(self.frame, image=role3, command=lambda: self.role(3)).grid(row=1, column=2)
        role4 = ImageTk.PhotoImage(file='./head/4.png')
        tk.Button(self.frame, image=role4, command=lambda: self.role(4)).grid(row=1, column=3)
        role5 = ImageTk.PhotoImage(file='./head/5.png')
        tk.Button(self.frame, image=role5, command=lambda: self.role(5)).grid(row=1, column=4)
        role6 = ImageTk.PhotoImage(file='./head/6.png')
        tk.Button(self.frame, image=role6, command=lambda: self.role(6)).grid(row=2, column=0)
        role7 = ImageTk.PhotoImage(file='./head/7.png')
        tk.Button(self.frame, image=role7, command=lambda: self.role(7)).grid(row=2, column=1)
        role8 = ImageTk.PhotoImage(file='./head/8.png')
        tk.Button(self.frame, image=role8, command=lambda: self.role(8)).grid(row=2, column=2)
        role9 = ImageTk.PhotoImage(file='./head/9.png')
        tk.Button(self.frame, image=role9, command=lambda: self.role(9)).grid(row=2, column=3)
        role10 = ImageTk.PhotoImage(file='./head/10.png')
        tk.Button(self.frame, image=role10, command=lambda: self.role(10)).grid(row=2, column=4)
        role11 = ImageTk.PhotoImage(file='./head/11.png')
        tk.Button(self.frame, image=role11, command=lambda: self.role(11)).grid(row=3, column=0)
        role12 = ImageTk.PhotoImage(file='./head/12.png')
        tk.Button(self.frame, image=role12, command=lambda: self.role(12)).grid(row=3, column=1)
        role13 = ImageTk.PhotoImage(file='./head/13.png')
        tk.Button(self.frame, image=role13, command=lambda: self.role(13)).grid(row=3, column=2)

        # 显示玩家选择的角色
        self.head = ImageTk.PhotoImage(file='./head/1.png')
        label = tk.Label(self.frame, image=self.head)
        label.grid(row=4, column=0)

        label_info = tk.Label(
            self.frame,
            text='hp:%d\nmp:%d\nattack:%d\ndefence:%d' % (Choice.hp[BaseRoot.num],
                                                          Choice.mp[BaseRoot.num],
                                                          Choice.attack[BaseRoot.num],
                                                          Choice.defence[BaseRoot.num]),
            font=5, justify=tk.LEFT
        )
        label_info.grid(row=4, column=1)

        # 提示文本
        self.text2 = tk.Label(
            self.frame, height=2, text='请输入您的名字', font=8, fg='black', anchor='w'
        ).grid(row=4, column=2)

        # 按钮
        self.b = tk.Button(
            self.frame, width=14, height=2, text='返回', font=8, fg='black', command=self.back, bg='#F0FFFF'
        ).grid(row=5, column=0)
        self.b = tk.Button(
            self.frame, width=14, height=2, text='确认', font=8, fg='black', command=self.game_start, bg='#F0FFFF'
        ).grid(row=5, column=4)

        # 输入名字
        self.name = tk.Entry(self.frame, show=None, highlightcolor='green', highlightthickness=1, width=23, font=10)
        self.name.grid(row=4, column=3, columnspan=2)

        # 前面使用图片覆盖按钮，这里需要使用这个语句使得图片正常显示
        tk.mainloop()

    def back(self):
        self.frame.destroy()
        Welcome()

    def game_start(self):
        BaseRoot.name = self.name.get()
        if not BaseRoot.name == '':
            root = game_body.MainWindow(BaseRoot.num, BaseRoot.name)
            root.start()
        else:
            tk.messagebox.showwarning(title='未输入姓名哦！', message='告诉我你的大名嘛')

    def role(self, num):
        self.head = ImageTk.PhotoImage(file='./head/' + str(num) + '.png')
        label = tk.Label(self.frame, image=self.head)
        label.grid(row=4, column=0)
        label_info = tk.Label(
            self.frame,
            text='hp:%d\nmp:%d\nattack:%d\ndefence:%d' % (Choice.hp[num],
                                                          Choice.mp[num],
                                                          Choice.attack[num],
                                                          Choice.defence[num]),
            font=5, justify=tk.LEFT
        )
        label_info.grid(row=4, column=1)

        BaseRoot.num = num


if __name__ == '__main__':
    main_root = BaseRoot()
    BaseRoot.root.mainloop()
