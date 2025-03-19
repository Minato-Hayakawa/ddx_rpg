import pyxel
import time
import math
import random
import sympy as sym
import PyxelUniversalFont as puf
from enum import Enum


class Phase(Enum):
    START = "start"
    MENU = "menu"
    NORMAL_MODE = "nomalmode"
    EASY_MODE = "easiymode"
    NORMAL_STAGE_1 = "nomalstage1"
    NORMAL_STAGE_2 = "nomalstage2"
    GAME_CLEAR = "gameclear"
    END = "end"


class KeyCtrl:
    def __init__(self):
        pass

    def Is_Decide(self):
        return pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN)

    def Is_Up(self):
        return pyxel.btnp(pyxel.KEY_UP)

    def Is_Down(self):
        return pyxel.btnp(pyxel.KEY_DOWN)

    def Is_Left(self):
        return pyxel.btnp(pyxel.KEY_LEFT)

    def Is_Right(self):
        return pyxel.btnp(pyxel.KEY_RIGHT)


class App:
    def __init__(self):

        self.updown = False
        self.itembotan = False
        self.retirebotan = True
        self.sabilitybotan = False
        self.attackbotan = False
        self.stagescreen = False
        self.gamestgart = False
        self.ddx = False
        # self.ddy=False
        self.integral_dx = False
        self.C = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}  # 10は無限大扱い
        # self.integral_dy=False
        self.lim_x0 = False
        # self.lim_y0=False
        self.z = random.randrange(1, 6)
        self.timer = 0
        self.timer2 = 0

        self.font = puf.Writer("misaki_gothic.ttf")  # フォントを指定

        # ゲームの操作用座標
        self.x0 = False
        self.x1 = False
        self.x2 = False
        self.y0 = False
        self.y1 = False
        self.y2 = False

        # アイテム
        self.item1 = 5
        self.item2 = 5
        self.item3 = 5
        self.item4 = 5

        self.rulet = {16: {}}
        self.myhp = 100  # 自分のhp
        self.hp = 100  # 敵のhp
        self.myfunc1 = math.factorial(self.z)  # x!
        self.func1 = math.e**2 * self.z  # ステージ1の敵
        self.attackpower1 = self.func1

        self.phase = Phase.START

        self.myKey = KeyCtrl()

        pyxel.init(150, 150, title="The Integral War")
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.phase == Phase.START:
            self.start()
        elif self.phase == Phase.MENU:
            self.menu()
        elif self.phase == Phase.NORMAL_MODE:
            self.timer += 1
            self.timer2 += 1
            self.nomalmode()
        elif self.phase == Phase.EASY_MODE:
            self.easiymode()
        elif self.phase == Phase.NORMAL_STAGE_1:
            self.nomalstage1()
            if self.gamestgart == True:
                self.botan()
                self.itemfunc()
        elif self.phase == Phase.NORMAL_STAGE_2:
            self.nomalstage2()
            self.botan()
        elif self.phase == Phase.GAME_CLEAR:
            self.gameclear()
        elif self.phase == Phase.END:
            self.end()

    def botan(self):
        if self.retirebotan == True:
            if self.myKey.Is_Down():
                print("down")
                self.itembotan = True
                self.retirebotan = False
            elif self.myKey.Is_Decide():
                self.end()

        elif self.itembotan == True:
            if self.myKey.Is_Up():
                self.itembotan = False
                self.retirebotan = True
            elif self.myKey.Is_Down():
                self.itembotan = False
                self.sabilitybotan = True
            elif self.myKey.Is_Decide():
                self.x0 = True
                self.y0 = True
                if self.x0 == True and self.y0 == True:
                    if self.myKey.Is_Decide():
                        self.item1 -= 1
                    elif self.myKey.Is_Right():
                        self.x0 = False
                        self.x1 = True
                    elif self.myKey.Is_Left():
                        self.y0 = False
                        self.y1 = True
                elif self.x1 == True and self.y0 == True:
                    if(self.myKey.Is_Decide()):
                        self.item2 -= 1
                    elif self.myKey.Is_Down():
                        self.y0 = False
                        self.y1 = True
                    elif self.myKey.Is_Left():
                        self.x0 = True
                        self.x1 = False
                elif self.x1 == True and self.y1 == True:
                    if self.myKey.Is_Decide():
                        self.item3 -= 1
                    elif self.myKey.Is_Up():
                        self.y0 = True
                        self.y1 = False
                    elif self.myKey.Is_Left():
                        self.x0 = True
                        self.x1 = False
                elif self.x1 == True and self.y1 == True:
                    if self.myKey.Is_Decide():
                        self.item4 -= 1
                    elif self.myKey.Is_Up():
                        self.y0 = True
                        self.y1 = False
                    elif self.myKey.Is_Right():
                        self.x0 = False
                        self.x1 = True

        if self.sabilitybotan == True:
            if self.myKey.Is_Up():
                self.sabilitybotan = False
                self.itembotan = True
            elif self.myKey.Is_Down():
                self.sabilitybotan = False
                self.attackbotan = True
            elif self.myKey.Is_Decide():
                self.x0 = True
                self.y0 = True
                if self.x0 == True and self.y0 == True:
                    if self.myKey.Is_Decide():
                        self.nabla = True
                    elif self.myKey.Is_Right():
                        self.x0 = False
                        self.x1 = True
                    elif self.myKey.Is_Down():
                        self.y0 = False
                        self.y1 = True
                elif self.x1 == True and self.y0 == 0:
                    if self.myKey.Is_Decide():
                        self.delta = True
                    elif self.myKey.Is_Left():
                        self.x1 = False
                        self.x0 = True
                    elif self.myKey.Is_Down():
                        self.y0 = False
                        self.y1 = True
                elif self.x0 == True and self.y1 == True:
                    if self.myKey.Is_Decide():
                        self.round_x = True
                    elif self.myKey.Is_Up():
                        self.y1 = False
                        self.y0 = True
                    elif self.myKey.Is_Right():
                        self.x0 = False
                        self.x1 = True
                    elif self.myKey.Is_Down():
                        self.y1 = False
                        self.y2 = True
                elif self.x1 == True and self.y1 == True:
                    if self.myKey.Is_Decide():
                        self.round_y = True
                    elif self.myKey.Is_Up():
                        self.y1 = False
                        self.y0 = True
                    elif self.myKey.Is_Left():
                        self.x1 = False
                        self.x0 = True
                    elif self.myKey.Is_Down():
                        self.y1 = False
                        self.y2 = True
                elif self.x0 == True and self.y2 == True:
                    if self.myKey.Is_Decide():
                        self.lim_00 = True
                    elif self.myKey.Is_Up():
                        self.y2 = False
                        self.y1 = True
                    elif self.myKey.Is_Right():
                        self.x0 = False
                        self.x1 = True
                elif self.x1 == True and self.y2 == True:
                    if self.myKey.Is_Decide():
                        self.lim_mm = True
                    elif self.myKey.Is_Up():
                        self.y2 = False
                        self.y1 = True
                    elif self.myKey.Is_Left():
                        self.x0 = True
                        self.x1 = False

        if self.attackbotan == True:
            if self.myKey.Is_Up():
                self.attackbotan = False
                self.sabilitybotan = True
            elif self.myKey.Is_Decide():
                self.x0 = True
                self.y0 = True
            elif self.x0 == True and self.y0 == True:
                if self.myKey.Is_Right():
                    self.x0 = False
                    self.x1 = True
                elif self.myKey.Is_Down():
                    self.y0 = False
                    self.y1 = True
                elif self.myKey.Is_Decide():
                    self.ddx = True
            elif self.x1 == True and self.y0 == True:
                if self.myKey.Is_Left():
                    self.x0 = True
                    self.x1 = False
                elif self.myKey.Is_Down():
                    self.y0 = False
                    self.y1 = True
                elif self.myKey.Is_Decide():
                    self.ddy = True
            elif self.x0 == True and self.y1 == True:
                if self.myKey.Is_Up():
                    self.y0 = True
                    self.y1 = False
                elif self.myKey.Is_Right():
                    self.x1 = True
                    self.x0 = False
                elif self.myKey.Is_Down():
                    self.y0 = False
                    self.y1 = False
                    self.y2 = True
                elif self.myKey.Is_Decide():
                    self.integral_dx = True
            elif self.x1 == True and self.y1 == True:
                if self.myKey.Is_Left():
                    self.x0 = True
                    self.x1 = False
                elif self.myKey.Is_Up():
                    self.y0 = True
                    self.y1 = False
                elif self.myKey.Is_Down():
                    self.y0 = False
                    self.y1 = False
                    self.y2 = True
                elif self.myKey.Is_Decide():
                    self.integral_dy = True
            elif self.x0 == True and self.y2 == True:
                if self.myKey.Is_Up():
                    self.y0 = False
                    self.y1 = True
                    self.y2 = False
                elif self.myKey.Is_Right():
                    self.x0 = False
                    self.x1 = True
                elif self.myKey.Is_Decide():
                    self.lim_x0 = True
            elif self.x1 == True and self.y2 == True:
                if self.myKey.Is_Up():
                    self.y1 = True
                    self.y0 = False
                    self.y2 = False
                elif self.myKey.Is_Left():
                    self.x0 = True
                    self.x1 = False
                elif self.myKey.Is_Decide():
                    self.lim_y0 = True

    def start(self):
        if self.myKey.Is_Decide():
            self.phase = Phase.MENU

    def menu(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.updown = False
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.updown = True

        if self.updown == False:
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.phase = Phase.NORMAL_MODE
                self.stagescreen = True
        elif self.updown == True:
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.phase = Phase.EASY_MODE
                self.stagescreen = True

    def nomalmode(self):
        if self.timer2 >= 145:
            self.stagescreen = False
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.phase = Phase.NORMAL_STAGE_1

    def nomalstage1(self):
        self.gamestgart = True

    # def nomalstage2(self):
    #     self.stagescreen=True
    #     if pyxel.blt(pyxel.KEY_RETURN) and self.timer2>=145:
    #         self.gamestart=True
    #         self.stagescreen=False

    # def nomalstage3(self):

    # def nomalstage4(self):

    # def nomalstage5(self):

    # def easiystage1(self):

    # def easiystage2(self):

    # def easiystage3(self):

    # def easiystage4(self):

    # def easiystage5(self):

    # def gameclear(self):
    #     pyxel.blt(0,0,0,0,0,160,120) #対戦画面を表示
    #     self.font.draw(0,0, "game clear!", 50, 13) #テロップにgame clear!と表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
    #     time.sleep(0.5)
    #     for i in range(3):
    #         pyxel.blt(0,72,0,0,0,80,16) #ステージを表示(矢印なし)
    #         time.sleep(0.5)
    #         pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示(矢印あり)
    #         pyxel.blt(24,18,1,0,0,16,16)#矢印
    #         time.sleep(0.5)
    #     self.phase=Phase.END

    # def end(self):
    #     pyxel.blt(30,0,0,0,16,50,120) #真っ黒を表示
    #     self.start()

    def draw(self):
        if self.phase == Phase.START:
            pyxel.blt(
                10, 15, 0, 96, 0, 140, 80, pyxel.COLOR_BLACK
            )  # スタート画面を表示
            pyxel.blt(42, 79, 1, 16, 0, 65, 16, pyxel.COLOR_BLACK)
            self.font.draw(22, 43, "∫積分伝説〜勇者とdxの旅〜", 8, 13)
            self.font.draw(46, 83, "Enterでスタート", 8, 13)
        elif self.phase == Phase.MENU:
            pyxel.cls(0)
            pyxel.blt(
                10, 15, 0, 96, 0, 140, 120, pyxel.COLOR_BLACK
            )  # スタート画面を表示
            self.font.draw(22, 43, "∫積分伝説〜勇者とdxの旅〜", 8, 13)
            self.font.draw(58, 83, "ノーマル", 8, 13)
            self.font.draw(59, 115, "イージー", 8, 13)
            if self.updown == False:
                pyxel.blt(42, 79, 1, 16, 0, 65, 16, pyxel.COLOR_BLACK)
            elif self.updown == True:
                pyxel.blt(42, 111, 1, 16, 0, 65, 16, pyxel.COLOR_BLACK)
        elif self.phase == Phase.NORMAL_MODE:
            if self.stagescreen == True:
                pyxel.cls(0)
                for i in range(3):
                    pyxel.blt(
                        35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK
                    )  # ステージを表示(矢印なし)
                    if 45 >= self.timer >= 30:  # 1秒後
                        pyxel.blt(
                            35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK
                        )  # ステージを表示(矢印なし)
                        pyxel.blt(35, 85, 1, 0, 14, 16, 16, pyxel.COLOR_BLACK)  # 矢印
                    elif self.timer >= 45:  # 1秒後
                        pyxel.cls(0)
                        pyxel.blt(
                            35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK
                        )  # ステージを表示(矢印なし)
                        self.timer = 0
            else:
                self.font.draw(100, 140, "Push return", 8, 7)
        elif self.phase == Phase.NORMAL_STAGE_1 and self.gamestgart == True:
            pyxel.cls(0)
            pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
            pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
            pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
            pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
            pyxel.blt(24, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
            pyxel.blt(40, 41, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
            # ↑微分に変える
            pyxel.blt(22, 72, 0, 0, 32, 16, 16, pyxel.COLOR_BLACK)  # ∫d
            pyxel.blt(33, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
            pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
            pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
            pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

            self.font.draw(0, 0, "リタイア", 8, 7)
            self.font.draw(0, 10, "アイテム", 8, 7)
            self.font.draw(0, 18, "特殊能力", 8, 7)
            self.font.draw(0, 28, "こうげき", 8, 7)
            self.font.draw(73, 5, "あいて", 8, 7)
            self.font.draw(33, 120, "e^2*xが現れた！", 8, 7)
            pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
            pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            if self.retirebotan == True:
                pyxel.blt(0, 0, 2, 0, 60, 38, 9, pyxel.COLOR_BLACK)
            elif self.itembotan == True:
                pyxel.blt(0, 8, 2, 0, 67, 38, 11, pyxel.COLOR_BLACK)
            elif self.sabilitybotan == True:
                pyxel.blt(0, 16, 2, 0, 75, 38, 12, pyxel.COLOR_BLACK)
            elif self.attackbotan == True:
                pyxel.blt(0, 27, 2, 0, 93, 38, 11, pyxel.COLOR_BLACK)
                if self.x0 == True and self.y0 == True:
                    pyxel.blt(1, 41, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                elif self.x1 == True and self.y0 == True:
                    pyxel.blt(24, 41, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                elif self.x0 == True and self.y1 == True:
                    pyxel.blt(1, 72, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                elif self.x1 == True and self.y1 == True:
                    pyxel.blt(24, 72, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)

                # self.font.draw()#文字を表示
        # elif self.phase==Phase.NOMALSTAGE2:
        #     if self.stagescreen==True:
        #         pyxel.cls(0)
        #         for i in range(3):
        #             pyxel.blt(25,52,0,0,0,80,16) #ステージを表示(矢印なし)
        #             if 45>=self.timer>=30: #1秒後
        #                 pyxel.blt(25,52,0,0,0,80,16) #ステージを表示(矢印なし)
        #                 pyxel.blt(25,70,1,0,14,16,16)#矢印
        #             elif self.timer>=45: #1秒後
        #                 pyxel.cls(0)
        #                 pyxel.blt(25,52,0,0,0,16,80) #ステージを表示(矢印なし)
        #                 self.timer=0
        #         pyxel.blt()#対戦画面を表示
        #     elif self.gamestart==True:
        #         pyxel.blt()#対戦画面を表示
        #         self.font.draw()#文字を表示

    def itemfunc(self):
        if self.item1:  # 自分のHPを50回復
            self.item1 -= 1
            self.myhp += 50
        if self.item2:  # 自分のHPを100回復
            self.item2 -= 1
            self.myhp += 100
        if self.item3:  # 相手のターンを一回無視
            self.item3 -= 1
            # 相手のターンを無視する処理
        if self.item4:  # "相手の関数の位相を+π/4ずらす"
            self.item4 -= 1
            self.z += math.pi / 4
            self.func1 = math.e**2 * self.z

    def battlemode(self):
        if self.hp >= 0 and self.myhp >= 0:
            if self.ddx == True:
                self.func1 = sym.Derivative(self.func1).doit()
                self.hp = self.hp * 2
            if self.integral_dx == True:
                self.func1 = sym.integrate(self.func1)
                self.hp = self.hp / 2
                if self.C[random.randrange(10)] != 10:
                    self.hp += self.C[random.randrange(10)]  # 積分定数Cの値だけhpが増加
                else:
                    self.hp = 0

            # 自分の攻撃
            self.z = random.randrange(
                10
            )  # ←ここの確率を調整してください。出やすさ:2>3>4>1>5>6
            self.myfunc1 = math.factorial(self.z)  # このときの自分の関数:x!
            self.hp = self.hp - self.myfunc1

            # 敵の攻撃
            self.z = random.randrange(6)
            self.func1 = math.e**self.z * 2
            self.myhp -= self.func1
        elif self.myhp <= 0:
            self.phase = Phase.END
        elif self.hp <= 0 or (self.hp <= 0 and self.myhp <= 0):
            self.phase = Phase.GAMECLEAR

    def end(self):
        pyxel.quit()


App()
