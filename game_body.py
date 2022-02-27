"""
这里是游戏体，使用model中的父类进行专门针对游戏的类创建
"""

import pygame
import sys
import model
from random import randint


# 进入游戏后的主界面，由pygame制作
class MainWindow:
    width = 1400
    height = 700
    size = width, height
    role1 = None  # 电脑
    role2 = None  # 玩家
    duel = None
    text_skill = None
    text_choice = None
    text_role = None
    text_role_name = None
    text_win = None
    text_restart = None
    num = 1

    def __init__(self, num, name):
        MainWindow.num = num   # 玩家选择的人物序号
        self.name = name
        self.screen = pygame.display.set_mode(MainWindow.size, 0)
        self.game_live = True  # 游戏是否结束
        self.winner = None
        self.color = (192, 192, 192)  # 主界面背景颜色
        self.role_color = (0, 0, 205)  # 人物属性字体颜色
        self.skill_color = (0, 0, 255)  # 技能显示字体颜色
        self.result_color = (220, 20, 60)  # 结果显示字体颜色
        # 为了平台的移植性，不使用系统字体，使用项目提供字体
        self.chinese_font = r'./fonts/STKAITI.ttf'  # 中文字体文件名
        self.english_font = r'./fonts/CENTAUR.ttf'  # 英文字体文件名

    def start(self):
        # 窗口设置
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('fighting! my man!')
        icon = pygame.image.load('./images/benghuai.jpg')
        pygame.display.set_icon(icon)
        # 背景音乐
        pygame.mixer.music.load(r'./music/Tiger Rhythm.wav')
        # 播放音乐流，里面的参数是播放的次数，-1表示无限循环播放
        pygame.mixer.music.play(-1)
        self.loop()

    # 循环体
    def loop(self):
        # 创建对象
        self.create()
        # 进入循环
        while True:
            self.screen.fill(self.color)
            # 背景图片
            background = pygame.image.load('./images/background.png')
            self.screen.blit(background, (0, 0))

            # 显示对象
            self.show()
            self.get_event()
            # 决斗
            if self.game_live:
                if MainWindow.role1.live and MainWindow.role2.live:
                    if MainWindow.role1.next:
                        MainWindow.duel.start()
                        MainWindow.role1.next = 0
                    self.show_skill(MainWindow.role1, 150)
                    self.show_skill(MainWindow.role2, 200)
                else:
                    MainWindow.duel.who_winner()
                    # 背景音乐
                    s = pygame.mixer.Sound('./music/ah.wav')
                    # 播放音乐流，里面的参数再+1是播放的次数，-1表示无限循环播放
                    s.play(0)
                    self.game_live = False
            else:
                self.result()
            pygame.display.update()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.game_live = True
                    self.loop()
                if event.key == pygame.K_1:
                    MainWindow.role2.flag = 0
                    MainWindow.role1.next = 1
                if event.key == pygame.K_2:
                    MainWindow.role2.flag = 1
                    MainWindow.role1.next = 1
                if event.key == pygame.K_3:
                    MainWindow.role2.flag = 2
                    MainWindow.role1.next = 1
                if event.key == pygame.K_4:
                    MainWindow.role2.flag = 3
                    MainWindow.role1.next = 1
                if event.key == pygame.K_5:
                    MainWindow.role2.flag = 4
                    MainWindow.role1.next = 1

    # 所有的对象都在这里创建
    def create(self):
        # 玩家的创建
        # NPC
        MainWindow.role1 = Role(self.screen, 'Kiana', './role/0.png', 30, 100, 1)
        # 玩家
        file_path = './role/' + str(MainWindow.num) + '.png'
        MainWindow.role2 = Role(self.screen, self.name, file_path, 830, 100, 0)
        # 战场的创建
        MainWindow.duel = model.Fight(MainWindow.role1, MainWindow.role2)
        # 文字对象
        MainWindow.text_skill = Text(self.chinese_font, 25)  # 显示技能的使用
        MainWindow.text_choice = Text(self.chinese_font, 21)  # 显示技能的选择
        MainWindow.text_role = Text(self.english_font, 22)  # 显示人物属性
        MainWindow.text_role_name = Text(self.chinese_font, 22)  # 显示人物名字
        MainWindow.text_win = Text(self.english_font, 40)
        MainWindow.text_restart = Text(self.english_font, 25)

    def show(self):
        # 显示技能选择上覆盖的框条
        image = pygame.image.load('./images/frame.png')
        rect = image.get_rect()
        rect.left = 0
        rect.top = MainWindow.role1.rect.bottom
        self.screen.blit(image, rect)
        # 显示文字
        self.write_text(MainWindow.role1)
        self.write_text(MainWindow.role2)
        self.write_choice()
        # 显示玩家对象
        MainWindow.role1.display()
        MainWindow.role2.display()

    # 人物基本属性
    def write_text(self, role):
        x = role.rect.left
        name = MainWindow.text_role_name.font.render('Name: %s' % role.name, True, self.role_color)
        self.screen.blit(name, (x, 8))
        attack = MainWindow.text_role.font.render('Attack: %d' % role.attack, True, self.role_color)
        self.screen.blit(attack, (x, 70))
        defence = MainWindow.text_role.font.render('Defence: %d' % role.defence, True, self.role_color)
        self.screen.blit(defence, (x + 150, 70))
        # 血量显示在血条后面，这里加上低血量警告
        if role.hp <= 100:
            hp = MainWindow.text_role.font.render('HP: %d/%d' % (role.hp, role.hp_max), True, (255, 0, 0))
        else:
            hp = MainWindow.text_role.font.render('HP: %d/%d' % (role.hp, role.hp_max), True, self.role_color)
        self.screen.blit(hp, (role.hp_bar.left + role.bar_length + 5, role.hp_bar.top - 2))
        # 能量显示在能量条后
        mp = MainWindow.text_role.font.render('MP: %d/%d' % (role.energy, role.energy_max), True, self.role_color)
        self.screen.blit(mp, (role.mp_bar.left + role.bar_length + 5, role.mp_bar.top - 2))

    # 技能的展示
    def write_choice(self):
        content = [
            '1-恢复（无消耗，+200MP，+200HP）',
            '2-超级攻击（消耗60MP，+10-20攻击与防御）',
            '3-天使力量（消耗100MP，+30-35攻击，+10-15防御）',
            '4-苏钊的愤怒（消耗200MP，+50-55攻击）',
            '5-超级防御（消耗100MP，+50防御）'
        ]
        x = [50, 450, 870]
        y1 = MainWindow.height - 100
        skill = MainWindow.text_choice.font.render(content[0], True, self.role_color)
        rect1 = skill.get_rect()
        self.screen.blit(skill, (x[0], y1))
        y2 = y1 + rect1.height + 2
        skill = MainWindow.text_choice.font.render(content[1], True, self.role_color)
        self.screen.blit(skill, (x[1], y1))
        skill = MainWindow.text_choice.font.render(content[2], True, self.role_color)
        self.screen.blit(skill, (x[2], y1))
        skill = MainWindow.text_choice.font.render(content[3], True, self.role_color)
        self.screen.blit(skill, (x[0], y2))
        skill = MainWindow.text_choice.font.render(content[4], True, self.role_color)
        self.screen.blit(skill, (x[1], y2))

    def result(self):
        # 显示决斗结果
        if not MainWindow.duel.winner:
            content = 'NO WINNER!'
        elif MainWindow.duel.winner == MainWindow.role1:
            content = 'YOU LOST!'
        else:
            content = 'YOU WIN!'
        text1 = MainWindow.text_win.font.render(content, True, (255, 0, 0))
        rect1 = text1.get_rect()
        left1 = int((MainWindow.width - rect1.width) / 2)
        # 后面是该文字放置的位置，（x,y），这里的x是定值，使得文字始终位于界面中心
        self.screen.blit(text1, (left1, 280))

        # 显示游戏重启提示信息
        text2 = MainWindow.text_restart.font.render('press R to restart', True, (255, 0, 0))
        rect2 = text2.get_rect()
        left2 = int((MainWindow.width - rect2.width) / 2)
        self.screen.blit(text2, (left2, 340))

        text3 = MainWindow.text_restart.font.render('press ESC to exit', True, (255, 0, 0))
        rect3 = text3.get_rect()
        left3 = int((MainWindow.width - rect3.width) / 2)
        self.screen.blit(text3, (left3, 380))

    def show_skill(self, role, y):
        skill = MainWindow.text_skill.font.render(role.skill, True, self.skill_color)
        rect = skill.get_rect()
        left = int((MainWindow.width - rect.width) / 2)
        self.screen.blit(skill, (left, y))


class Text:

    def __init__(self, font_path, size):
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, size)
        self.rect = None

    def get_position(self, text, x, y):
        self.rect = text.get_rect()
        self.rect.left = x
        self.rect.top = y


class Role(model.Player):

    def __init__(self, screen, name, image_path, x, y, ai):
        self.ai = ai
        super().__init__(name, self.ai, MainWindow.num)
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        # 状态条参数
        self.bar_length = 400  # 状态条（血条，能量条）最长长度
        self.hp_top = 35
        self.mp_top = 55
        self.hp_bar = pygame.Rect(self.rect.left, self.hp_top, self.bar_length, 18)
        self.mp_bar = pygame.Rect(self.rect.left, self.mp_top, self.bar_length, 18)

    def display(self):
        # 人物的显示
        self.screen.blit(self.image, self.rect)

        # 血条的显示，血条由两个 矩形构成，一个是血条背景，一个是当前血量
        # 血条背景
        pygame.draw.rect(self.screen, (128, 0, 0), self.hp_bar)
        # 血条
        if self.hp != 0:
            pygame.draw.rect(
                self.screen, (255, 0, 0),
                (self.rect.left, self.hp_top, int(self.bar_length / self.hp_max * self.hp), 18)
            )

        # 能量条的显示
        # 能量条背景
        pygame.draw.rect(self.screen, (0, 0, 128), self.mp_bar)
        # 能量条
        if self.energy != 0:
            pygame.draw.rect(
                self.screen, (0, 0, 255),
                (self.rect.left, self.mp_top, int(self.bar_length / self.energy_max * self.energy), 18)
            )

    def choice(self):
        if self.ai:
            # 为提高决斗效率，hp大于400不可使用恢复技能
            if self.hp < 400:
                self.flag = randint(0, 4)
            else:
                self.flag = randint(1, 4)
