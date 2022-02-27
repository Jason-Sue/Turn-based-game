"""
这里是角色文件，定义了角色类与手柄类
作为游戏体的父类
"""

from random import randint
import pygame


# 定义角斗场类，本质为手柄，通过这个类来实现游戏的游玩
class Fight:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.round = 0   # 回合数
        self.record1 = []   # 玩家一hp记录
        self.record2 = []   # 玩家二hp记录
        self.winner = None

    # 定义玩家一的攻击规则
    @staticmethod
    def attack_way(attacker, defender):
        if attacker.move:
            hurt = 2 * attacker.attack - defender.defence
            if hurt >= 0:
                if defender.hp > hurt:
                    defender.hp -= hurt
                else:
                    defender.hp = 0
            else:
                pass
        attacker.move = 1

    # 决斗开始
    def start(self):
        self.player1.choice()
        self.player1.release()
        self.player2.choice()
        self.player2.release()
        self.attack_way(self.player1, self.player2)
        self.attack_way(self.player2, self.player1)
        # 记录此时属性
        self.record1.append(self.player1.hp)
        self.record2.append(self.player2.hp)
        # 回合数
        self.round += 1
        # 任一方血量归零，决斗结束
        if self.player1.hp <= 0:
            self.player1.live = False
        if self.player2.hp <= 0:
            self.player2.live = False

    # 获胜判定
    def who_winner(self):
        if self.player1.hp <= 0 and self.player2.hp <= 0:
            self.player1.live = False
            self.player2.live = False
        elif self.player1.hp > self.player2.hp:
            self.player2.live = False
            self.winner = self.player1
        else:
            self.player1.live = False
            self.winner = self.player2


class Player(pygame.sprite.Sprite):
    # 第一个是人机，其他是玩家选择的角色对应的属性
    hp = [2420, 2200, 2100, 2500, 2100, 2200, 2310, 2342, 2600, 2300, 2010, 2300, 1985, 2420]
    mp = [540, 530, 533, 560, 600, 585, 562, 560, 510, 542, 580, 523, 620, 540]
    attack = [125, 120, 122, 132, 135, 120, 125, 124, 130, 132, 133, 120, 132, 133]
    defence = [118, 110, 120, 132, 120, 111, 120, 120, 112, 118, 121, 132, 120, 119]

    def __init__(self, name, ai, num):
        pygame.sprite.Sprite.__init__(self)
        self.name = name   # 名字
        self.ai = ai
        if self.ai:
            self.num = 0
        else:
            self.num = num
        self.attack = Player.attack[self.num]   # 攻击值
        self.defence = Player.defence[self.num]   # 防御值
        # 可减少的数值
        self.hp_max = Player.hp[self.num]
        self.hp = self.hp_max  # 生命值
        self.energy_max = Player.mp[self.num]
        self.energy = self.energy_max   # 能量值

        self.flag = 0   # 选择技能
        self.move = 1   # 是否能攻击，使用恢复类技能不能攻击
        self.live = True   # 玩家是否被击败
        self.skill = None   # 存储使用的技能文本
        self.next = 0

    # 技能的释放
    def release(self):
        # 能量值小于0时只能使用恢复技能
        if self.energy > 0:
            if self.flag == 0:
                self.recover()
            elif self.flag == 1 and self.energy >= 60:
                self.super_attack()
            elif self.flag == 2 and self.energy >= 100:
                self.angle_power()
            elif self.flag == 3 and self.energy >= 200:
                self.jason_anger()
            elif self.flag == 4 and self.energy >= 100:
                self.super_defence()
            else:
                self.recover()
        else:
            self.recover()

    def super_attack(self):
        self.attack += randint(10, 20)
        self.defence += randint(10, 20)
        self.energy -= 60
        self.skill = '%s使用了技能：超级攻击' % self.name

    def recover(self):
        # 使用后相关数值不上溢
        self.energy += 200
        if self.energy > self.energy_max:
            self.energy = self.energy_max
        self.hp += 200
        if self.hp > self.hp_max:
            self.hp = self.hp_max

        self.move = 0
        self.skill = '%s使用了技能：恢复' % self.name

    def angle_power(self):
        self.attack += randint(30, 35)
        self.defence += randint(10, 15)
        self.energy -= 100
        self.skill = '%s使用了技能：天使力量' % self.name

    def jason_anger(self):
        self.attack += randint(50, 55)
        self.energy -= 200
        self.skill = '%s使用了技能：苏钊的愤怒' % self.name

    def super_defence(self):
        self.defence += 50
        self.energy -= 100
        self.skill = '%s使用了技能：超级防御' % self.name
