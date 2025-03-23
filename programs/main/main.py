import pyxel
import math
import random
import sympy as sym
import PyxelUniversalFont as puf
from enum import Enum, auto

x= sym.symbols('x')

class Phase(Enum):
    START = "start"
    MENU = "menu"
    NORMAL_MODE = "nomalmode"
    EASY_MODE = "easiymode"
    NORMAL_STAGE_1 = "nomalstage1"
    NORMAL_STAGE_2 = "nomalstage2"
    GAME_OVER="gameover"
    GAME_CLEAR = "gameclear"
    END = "end"

class InputHandler():
    def isDecide():
        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
            return True
        else:
            return False

    def isUp():
        if pyxel.btnp(pyxel.KEY_UP):
            return True
        else:
            return False

    def isDown():
        if pyxel.btnp(pyxel.KEY_DOWN):
            return True
        else:
            return False

    def isLeft():
        if pyxel.btnp(pyxel.KEY_LEFT):
            return True
        else:
            return False

    def isRight():
        if pyxel.btnp(pyxel.KEY_RIGHT):
            return True
        else:
            return False

class AttackMenu(Enum):
    左上 = auto(),
    右上 = auto(),
    左下 = auto(),
    右下 = auto(),

class KIGOUViwer:
    def showHPFrame(self, x, y):
        pyxel.blt(x,y,2,161,0,8,8,pyxel.COLOR_BLACK)#=

    def showHPLid(self, x, y):
        pyxel.blt(x, y, 2, 144, 0, 8, 8, pyxel.COLOR_BLACK)#[

    def showHPCharacter(self, x, y):
        pyxel.blt(x,y,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示

    def showX(self, x, y):
        pyxel.blt(x, y, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示

    def show_d(self, x, y):
        pyxel.blt(x, y, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示

    def show_dx(self, x, y):
        pyxel.blt(x, y, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示

    def show_exclamationMark(self,x,y):
        pyxel.blt(x, y, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示

    def show_XJOU(self,x,y):
        pyxel.blt(x, y, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示
    
    def show_2JOU(self,x,y):
        pyxel.blt(x, y, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示

    def show_e(self,x,y):
        pyxel.blt(x, y, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
    
    def show_Integral(self,x,y):
        pyxel.blt(x, y, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫

class App:
    def __init__(self):

        self.updown = False
        self.itembotan = False  # 現在カーソルがアイテムにあるかどうかを判断するフラグ
        self.retirebotan = True
        self.sabilitybotan = False
        self.attackbotan = False
        self.stagescreen = False
        self.gamestgart = False
        self.botanstart = False
        self.func1attack = False
        self.func2attack = False
        self.gameover_flag = False
        self.ddx = False
        self.ddx_count=0
        # self.ddy=False
        self.integral_dx = False
        self.C = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 10は無限大扱い
        # self.integral_dy=False
        self.lim_x0 = False
        # self.lim_y0=False

        self.timer = 0
        self.timer2 = 0 # normalmodeに遷移した後に、normalstage1に遷移するまでの時間を計測するための変数っぽいけど、他でガンガンに使われてるからよくわからん

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
        self.num=0
        self.rulet = [0,sym.pi/6,sym.pi/4,sym.pi/3,sym.pi/2,sym.pi*2/3,sym.pi*3/4,sym.pi*5/6,sym.pi,sym.pi*7/6,sym.pi*5/4,sym.pi*4/3,sym.pi*3/2,sym.pi*5/3,sym.pi*7/4,sym.pi*11/6]
        self.myhp = 100  # 自分のhp
        self.hp = 100  # 敵のhp
        self.myfunc1=sym.factorial(x) # x!
        self.myfunc2=x
        self.func1 = math.e**2 * x  # ステージ1の敵
        self.func2=sym.tan(x)
        self.attackpower1 = self.func1
        self.damage=0
        self.mydamage=0

        self.attackMenu = AttackMenu.左上 # 攻撃メニューの初期値
        self.phase = Phase.START

        self.kigouViwer = KIGOUViwer()  # KIGOUViwerのインスタンスを作成

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
            self.botan()
        elif self.phase==Phase.GAME_OVER:
            self.gameover()
            self.timer+=1

        elif self.phase == Phase.NORMAL_STAGE_2:
            self.nomalstage_2()
            self.timer+=1
            self.timer2+=1
            if self.gamestgart==True:
                self.botan()
        elif self.phase == Phase.GAME_CLEAR:
            self.gameclear()
            self.timer+=1
        elif self.phase == Phase.END:
            self.end()

    def setAttackMenuStats(self, name: AttackMenu):        
        self.attackMenu = name
        if(name == AttackMenu.左上):
            self.changeXpos(0)
            self.changeYpos(0)
        elif(name == AttackMenu.右上):
            self.changeXpos(1)
            self.changeYpos(0)
        elif(name == AttackMenu.左下):
            self.changeXpos(0)
            self.changeYpos(1)
        elif(name == AttackMenu.右下):
            self.changeXpos(1)
            self.changeYpos(1)

    def changeXpos(self ,num: int):
        if num == 1:
            self.x0 = False
            self.x1 = True
        else:
            self.x0 = True
            self.x1 = False

    def changeYpos(self, num:int):
        if num == 1:
            self.y0 = False
            self.y1 = True
        else:
            self.y0 = True
            self.y1 = False

    def botan(self):
        if self.retirebotan == True:#最初の状態ではreturebotanはTrueです
            if InputHandler.isDown():#下を押したらretirebotanにカーソルを動かす
                self.itembotan = True
                self.retirebotan = False
            elif InputHandler.isDecide():#カーソルがretirebotanにあるときに決定を押したらゲームを終了します
                self.end()

        elif self.itembotan == True:#カーソルがアイテムにあるとき
            if InputHandler.isUp():#上を押されたらretirebotanに移動します
                self.itembotan = False
                self.retirebotan = True
            elif InputHandler.isDown():#下を押されたらsabilitybotanに移動します
                self.itembotan = False
                self.sabilitybotan = True
            elif InputHandler.isDecide():#決定を押されたらアイテムの選択画面に移動します.おそらくまだ未完成なので押してもなにも動かない.実行してもなにも動きませんでした。
                self.x0 = True
                self.y0 = True

                if self.x0 == True and self.y0 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item1 -= 1
                    elif pyxel.btnp(pyxel.KEY_RIGHT):
                        self.x0 = False
                        self.x1 = True
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y0 = False
                        self.y1 = True
                elif self.x1 == True and self.y0 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item2 -= 1
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y0 = False
                        self.y1 = True
                    elif pyxel.btnp(pyxel.KEY_LEFT):
                        self.x0 = True
                        self.x1 = False
                elif self.x1 == True and self.y1 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item3 -= 1
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y0 = True
                        self.y1 = False
                    elif pyxel.btnp(pyxel.KEY_LEFT):
                        self.x0 = True
                        self.x1 = False
                elif self.x1 == True and self.y1 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item4 -= 1
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y0 = True
                        self.y1 = False
                    elif pyxel.btnp(pyxel.KEY_RIGHT):
                        self.x0 = False
                        self.x1 = True

        elif self.sabilitybotan == True:#カーソルが特殊能力にあるとき
            if InputHandler.isUp():#上を押したらitembotanに移動します
                self.sabilitybotan = False
                self.itembotan = True
            elif InputHandler.isDown():#下を押したらattackbotanに移動します
                self.sabilitybotan = False
                self.attackbotan = True
            elif InputHandler.isDecide():#決定を押したら特殊能力の選択画面に移動します.おそらくまだ未完成なので押してもなにも動かない.実行してもなにも動きませんでした。
                self.x0 = True
                self.y0 = True
                if self.x0 == True and self.y0 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.nabla = True
                    elif pyxel.btnp(pyxel.KEY_RIGHT):
                        self.x0 = False
                        self.x1 = True
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y0 = False
                        self.y1 = True
                elif self.x1 == True and self.y0 == 0:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.delta = True
                    elif pyxel.btnp(pyxel.KEY_LEFT):
                        self.x1 = False
                        self.x0 = True
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y0 = False
                        self.y1 = True
                elif self.x0 == True and self.y1 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.round_x = True
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y1 = False
                        self.y0 = True
                    elif pyxel.btnp(pyxel.KEY_RIGHT):
                        self.x0 = False
                        self.x1 = True
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y1 = False
                        self.y2 = True
                elif self.x1 == True and self.y1 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.round_y = True
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y1 = False
                        self.y0 = True
                    elif pyxel.btnp(pyxel.KEY_LEFT):
                        self.x1 = False
                        self.x0 = True
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y1 = False
                        self.y2 = True
                elif self.x0 == True and self.y2 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.lim_00 = True
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y2 = False
                        self.y1 = True
                    elif pyxel.btnp(pyxel.KEY_RIGHT):
                        self.x0 = False
                        self.x1 = True
                elif self.x1 == True and self.y2 == True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.lim_mm = True
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y2 = False
                        self.y1 = True
                    elif pyxel.btnp(pyxel.KEY_LEFT):
                        self.x0 = True
                        self.x1 = False

        elif self.attackbotan == True:#カーソルがこうげきにあるとき
            if InputHandler.isUp() and self.attackMenu == AttackMenu.左上:#上を押した時に、左上にいたらsablitybotanに移動します
                self.attackbotan = False
                self.sabilitybotan = True
            elif InputHandler.isDecide() and self.botanstart==False:#決定ボタンを押したときにとある条件に重なるとbotanstartという用途不明なフラグが立ちます
                self.changeXpos(0)
                self.changeYpos(0)
                self.botanstart=True
            elif self.attackMenu == AttackMenu.左上:# 決定を押した後の状態。決定を押したら←のif文の条件が満たされます
                if InputHandler.isRight():#右を押すと右に移動します。移動するといってもx1というフラグが立つだけです
                    self.setAttackMenuStats(AttackMenu.右上)
                elif InputHandler.isDown():#下を押すと下に移動します。移動するといってもy1というフラグが立つだけです
                    self.setAttackMenuStats(AttackMenu.左下)
                elif InputHandler.isDecide():#決定を押すと攻撃が発動します。攻撃が発動するといってもfunc1attackというフラグが立つだけです。botanstartという謎のフラグが立ちます。また、attackmodeという謎のフラグも立ちます
                    self.func1attack=True
                    self.botanstart=False
                    self.battlemode()
            elif self.attackMenu == AttackMenu.右上:#攻撃メニューの右上にカーソルがあるとき
                if InputHandler.isLeft():
                    self.setAttackMenuStats(AttackMenu.左上)
                elif InputHandler.isDown():
                    self.setAttackMenuStats(AttackMenu.右下)
                elif InputHandler.isDecide():
                    self.ddx = True
                    self.ddx_count+=1
                    self.battlemode()
            elif self.attackMenu == AttackMenu.左下:#攻撃メニューの左下にカーソルがあるとき
                if InputHandler.isUp():
                    self.setAttackMenuStats(AttackMenu.左上)
                elif InputHandler.isRight():
                    self.setAttackMenuStats(AttackMenu.右下)
                elif InputHandler.isDecide():
                    self.func2attack=True
                    self.battlemode()
            elif self.attackMenu == AttackMenu.右下:#攻撃メニューの右下にカーソルがあるとき
                if InputHandler.isLeft():
                    self.setAttackMenuStats(AttackMenu.左下)
                elif InputHandler.isUp():
                    self.setAttackMenuStats(AttackMenu.右上)
                elif InputHandler.isDecide():
                    self.integral_dx = True
                    self.ddx_count-=1
                    self.battlemode()

    def start(self):
        if InputHandler.isDecide():
            self.phase = Phase.MENU

    def menu(self):
        if InputHandler.isUp():
            self.updown = False
        elif InputHandler.isDown():
            self.updown = True

        if not InputHandler.isDecide():
            return

        if self.updown is True:
            self.phase = Phase.EASY_MODE
            print("easy")
        else:
            self.phase = Phase.NORMAL_MODE
            print("normal")

        self.stagescreen = True

    def nomalmode(self):
        if self.timer2 >= 145:
            self.stagescreen = False
            if InputHandler.isDecide():
                self.phase = Phase.NORMAL_STAGE_1
                self.timer = 0
                self.timer2=0

    def nomalstage1(self):
        self.gamestgart = True
        if self.hp<=0:
            self.phase=Phase.GAME_CLEAR
        elif self.myhp<=0:
            self.phase=Phase.GAME_OVER

    '''
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
    '''

    def showGreen(self, x, y):
        pyxel.blt(x, y, 2, 176, 0, 8, 8, pyxel.COLOR_BLACK)  # 緑を表示

    def showKEISUU(self):
        if self.ddx_count==1:
            pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
        elif self.ddx_count==2:
            pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
        elif self.ddx_count==3:
            pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
        elif self.ddx_count==4:
            pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
        elif self.ddx_count==-1:
            pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-2:
            pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-3:
            pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-4:
            pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/

    def showAttackMenuRedCursor(self, x, y):
        pyxel.blt(x, y, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)

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
            self.kigouViwer.showX(1, 41)  # xを表示
            self.kigouViwer.show_exclamationMark(17, 41)  # !を表示
            self.kigouViwer.showX(1, 72)  # xを表示
            self.kigouViwer.show_d(30, 40)  # dを表示
            self.kigouViwer.show_dx(24, 41)  # /dxを表示
            # ↑微分に変える
            self.kigouViwer.show_Integral(20, 72)  # ∫を表示
            self.kigouViwer.show_d(26, 71)  # dを表示
            self.kigouViwer.showX(31, 73)  # xを表示
            self.kigouViwer.show_e(75, 40)  # eを表示
            self.kigouViwer.show_2JOU(88, 37)  # ^2を表示
            self.kigouViwer.show_XJOU(92, 37)  # ^xを表示

            self.font.draw(0, 0, "リタイア", 8, 7)
            self.font.draw(0, 10, "アイテム", 8, 7)
            self.font.draw(0, 18, "特殊能力", 8, 7)
            self.font.draw(0, 28, "こうげき", 8, 7)
            self.font.draw(73, 5, "あいて", 8, 7)
            self.font.draw(33, 120, "e^2xが現れた！", 8, 7)
            #自分のHP
            self.kigouViwer.showHPLid(75, 100)
            self.kigouViwer.showHPFrame(83, 100)
            self.kigouViwer.showHPFrame(90, 100)
            self.kigouViwer.showHPFrame(97, 100)
            if self.mydamage==0:
                self.showGreen(76,100)
                self.showGreen(84,100)
                self.showGreen(92,100)
                self.showGreen(96,100)
            elif self.mydamage<=self.myhp/5:
                self.showGreen(76,100)
                self.showGreen(84,100)
                self.showGreen(92,100)
            elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                self.showGreen(76,100)
                self.showGreen(84,100)
                self.showGreen(88,100)
            elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                self.showGreen(84,100)
                self.showGreen(76,100)
            elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                self.showGreen(76,100)
                self.showGreen(80,100)
            elif self.myhp*4/5<=self.mydamage<self.myhp:
                pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
            elif self.myhp<=self.mydamage:
                pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)

            #敵のHP
            self.kigouViwer.showHPLid(75, 28)
            self.kigouViwer.showHPFrame(83, 28)
            self.kigouViwer.showHPFrame(90, 28)
            self.kigouViwer.showHPFrame(97, 28)
            self.kigouViwer.showHPCharacter(104, 28)#HPを表示
            
            self.showKEISUU()

            if self.damage==0:
                self.showGreen(76,28)
                self.showGreen(84,28)
                self.showGreen(92,28)
                self.showGreen(96,28)
            elif self.damage<=self.hp/5:
                self.showGreen(76,28)
                self.showGreen(84,28)
                self.showGreen(92,28)
            elif self.hp/5<=self.damage<=self.hp*2/5:
                self.showGreen(76,28)
                self.showGreen(84,28)
                self.showGreen(88,28)
            elif self.hp*2/5<=self.damage<=self.hp*3/5:
                self.showGreen(76,28)
                self.showGreen(84,28)
            elif self.hp*3/5<=self.damage<=self.hp*4/5:
                self.showGreen(76,28)
                self.showGreen(80,28)
            elif self.hp*4/5<=self.damage<self.hp:
                pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
            elif self.hp<=self.damage:
                pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)

            if self.retirebotan == True:#カーソルがリタイアにあるときにリタイアの周りを赤く表示する
                pyxel.blt(0, 0, 2, 0, 60, 38, 9, pyxel.COLOR_BLACK)
            elif self.itembotan == True:#アイテムの周りを赤く表示する
                pyxel.blt(0, 8, 2, 0, 67, 38, 11, pyxel.COLOR_BLACK)
            elif self.sabilitybotan == True:#特殊能力の周りを赤く表示する
                pyxel.blt(0, 16, 2, 0, 75, 38, 12, pyxel.COLOR_BLACK)
            elif self.attackbotan == True:#カーソルがこうげきにあるとき....
                if self.func1attack==False and self.func2attack==False and self.ddx==False and self.integral_dx==False:
                    pyxel.blt(0, 27, 2, 0, 93, 38, 11, pyxel.COLOR_BLACK)
                    if self.attackMenu == AttackMenu.左上:
                        self.showAttackMenuRedCursor(1, 41)
                    elif self.attackMenu == AttackMenu.右上:
                        self.showAttackMenuRedCursor(24, 41)
                    elif self.attackMenu == AttackMenu.左下:
                        self.showAttackMenuRedCursor(1, 72)
                    elif self.attackMenu == AttackMenu.右下:
                        self.showAttackMenuRedCursor(24, 72)
                elif self.func1attack==True:

                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示
                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "x!で攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.ddx_count==1:
                        pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                    elif self.ddx_count==2:
                        pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                    elif self.ddx_count==3:
                        pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                    elif self.ddx_count==4:
                        pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                    elif self.ddx_count==-1:
                        pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-2:
                        pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-3:
                        pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-4:
                        pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.hp<=self.damage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0


                elif self.func2attack==True:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示
                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "xで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.ddx_count==1:
                        pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                    elif self.ddx_count==2:
                        pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                    elif self.ddx_count==3:
                        pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                    elif self.ddx_count==4:
                        pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                    elif self.ddx_count==-1:
                        pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-2:
                        pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-3:
                        pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    elif self.ddx_count==-4:
                        pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示

                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                elif self.ddx==True and self.ddx_count==1:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                
                elif self.ddx==True and self.ddx_count==2:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==3:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==4:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==0:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示 # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==0:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示 # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==-1:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==-2:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.ddx==True and self.ddx_count==-3:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 2, 40, 64, 16, 16, pyxel.COLOR_BLACK)#8
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                    elif self.ddx==True and self.ddx_count==-4:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                        pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                        pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                        pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0

                elif self.integral_dx==True and self.ddx_count==-1:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==-2:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==-3:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==-4:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                    pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==1:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==2:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==3:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
                elif self.integral_dx==True and self.ddx_count==4:
                    pyxel.cls(0)
                    pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                    pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                    pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                    pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                    # ↑微分に変える
                    pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                    pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                    pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                    pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                    pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
                    pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
                    pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示

                    self.font.draw(0, 0, "リタイア", 8, 7)
                    self.font.draw(0, 10, "アイテム", 8, 7)
                    self.font.draw(0, 18, "特殊能力", 8, 7)
                    self.font.draw(0, 28, "こうげき", 8, 7)
                    self.font.draw(73, 5, "あいて", 8, 7)
                    self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                    #自分のHP
                    pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                    pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                    if self.mydamage==0:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.mydamage<=self.myhp/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                        pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp*4/5<=self.mydamage<self.myhp:
                        pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                    elif self.myhp<=self.mydamage:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    #敵のHP
                    pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                    pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                    if self.damage==0:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.damage<=self.hp/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp/5<=self.damage<=self.hp*2/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*2/5<=self.damage<=self.hp*3/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*3/5<=self.damage<=self.hp*4/5:
                        pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                        pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    elif self.hp*4/5<=self.damage<self.hp:
                        pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                    self.timer+=1
                    if self.timer>=60:
                        self.func1attack=False
                        self.func2attack=False
                        self.ddx=False
                        self.integral_dx=False
                        self.attackbotan=False
                        self.itembotan=False
                        self.sabilitybotan=False
                        self.retirebotan=True
                        self.timer=0
                        
        elif self.phase==Phase.GAME_OVER:
            pyxel.cls(0)
            pyxel.blt(50,50,0,0,48,30,8,pyxel.COLOR_BLACK) #gameoverを表示
            pyxel.blt(74,50,0,0,56,24,8,pyxel.COLOR_BLACK)
            
        elif self.phase==Phase.GAME_CLEAR:
            pyxel.cls(0)
            pyxel.blt(50,50,0,0,48,24,8,pyxel.COLOR_BLACK) #gameclearを表示
            pyxel.blt(74,50,0,0,64,64,8,pyxel.COLOR_BLACK)
            
        elif self.phase==Phase.NORMAL_STAGE_2:
            if self.stagescreen==True:
                pyxel.cls(0)
                for i in range(3):
                    pyxel.blt(35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK)  # ステージを表示(矢印なし)
                    if 45 >= self.timer >= 30:  # 1秒後
                        pyxel.blt(35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK)  # ステージを表示(矢印なし)
                        pyxel.blt(51, 85, 1, 0, 14, 16, 16, pyxel.COLOR_BLACK)  # 矢印
                    elif self.timer >= 45:  # 1秒後
                        pyxel.cls(0)
                        pyxel.blt(35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK)  # ステージを表示(矢印なし)
                        self.timer = 0
            elif self.stagescreen==False and self.gamestgart==False:
                self.font.draw(100, 140, "Push return", 8, 7)
            
            elif self.stagescreen==False and self.gamestgart == True:
                pyxel.cls(0)
                pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                # ↑微分に変える
                pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                self.font.draw(0, 0, "リタイア", 8, 7)
                self.font.draw(0, 10, "アイテム", 8, 7)
                self.font.draw(0, 18, "特殊能力", 8, 7)
                self.font.draw(0, 28, "こうげき", 8, 7)
                self.font.draw(73, 5, "あいて", 8, 7)
                self.font.draw(33, 120, "tan(x)が現れた！", 8, 7)
                #自分のHP
                pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                if self.mydamage==0:
                    pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.mydamage<=self.myhp/5:
                    pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                    pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                    pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                    pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.myhp*4/5<=self.mydamage<self.myhp:
                    pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                elif self.myhp<=self.mydamage:
                    pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)

                #敵のHP
                pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                # if self.ddx_count==1:
                #     pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                # elif self.ddx_count==2:
                #     pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                # elif self.ddx_count==3:
                #     pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                # elif self.ddx_count==4:
                #     pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                # elif self.ddx_count==-1:
                #     pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                #     pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                # elif self.ddx_count==-2:
                #     pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                #     pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                # elif self.ddx_count==-3:
                #     pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                #     pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                # elif self.ddx_count==-4:
                #     pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                #     pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                if self.damage==0:
                    pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.damage<=self.hp/5:
                    pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.hp/5<=self.damage<=self.hp*2/5:
                    pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                    pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.hp*2/5<=self.damage<=self.hp*3/5:
                    pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.hp*3/5<=self.damage<=self.hp*4/5:
                    pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                    pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                elif self.hp*4/5<=self.damage<self.hp:
                    pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                elif self.hp<=self.damage:
                    pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                if self.retirebotan == True:
                    pyxel.blt(0, 0, 2, 0, 60, 38, 9, pyxel.COLOR_BLACK)
                elif self.itembotan == True:
                    pyxel.blt(0, 8, 2, 0, 67, 38, 11, pyxel.COLOR_BLACK)
                elif self.sabilitybotan == True:
                    pyxel.blt(0, 16, 2, 0, 75, 38, 12, pyxel.COLOR_BLACK)
                elif self.attackbotan == True:
                    if self.func1attack==False and self.func2attack==False and self.ddx==False and self.integral_dx==False:
                        pyxel.blt(0, 27, 2, 0, 93, 38, 11, pyxel.COLOR_BLACK)
                        if self.x0 == True and self.y0 == True:
                            pyxel.blt(1, 41, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                        elif self.x1 == True and self.y0 == True:
                            pyxel.blt(24, 41, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                        elif self.x0 == True and self.y1 == True:
                            pyxel.blt(1, 72, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                        elif self.x1 == True and self.y1 == True:
                            pyxel.blt(24, 72, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)
                    elif self.func1attack==True:

                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "x!で攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.ddx_count==1:
                            pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                        elif self.ddx_count==2:
                            pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                        elif self.ddx_count==3:
                            pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                        elif self.ddx_count==4:
                            pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                        elif self.ddx_count==-1:
                            pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-2:
                            pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-3:
                            pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-4:
                            pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.hp<=self.damage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0


                    elif self.func2attack==True:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "xで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.ddx_count==1:
                            pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
                        elif self.ddx_count==2:
                            pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
                        elif self.ddx_count==3:
                            pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
                        elif self.ddx_count==4:
                            pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
                        elif self.ddx_count==-1:
                            pyxel.blt(62, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-2:
                            pyxel.blt(62, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-3:
                            pyxel.blt(62, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        elif self.ddx_count==-4:
                            pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
                            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示

                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                    elif self.ddx==True and self.ddx_count==1:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                    
                    elif self.ddx==True and self.ddx_count==2:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==3:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==4:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==0:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #) # ^xを表示

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==0:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==-1:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==-2:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.ddx==True and self.ddx_count==-3:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                        elif self.ddx==True and self.ddx_count==-4:
                            pyxel.cls(0)
                            pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                            pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                            pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                            pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                            pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                            pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                            # ↑微分に変える
                            pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                            pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                            pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                            pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                            pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                            pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                            pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                            self.font.draw(0, 0, "リタイア", 8, 7)
                            self.font.draw(0, 10, "アイテム", 8, 7)
                            self.font.draw(0, 18, "特殊能力", 8, 7)
                            self.font.draw(0, 28, "こうげき", 8, 7)
                            self.font.draw(73, 5, "あいて", 8, 7)
                            self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
                            #自分のHP
                            pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                            pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                            pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                            pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                            if self.mydamage==0:
                                pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            elif self.mydamage<=self.myhp/5:
                                pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                                pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                                pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                                pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            elif self.myhp*4/5<=self.mydamage<self.myhp:
                                pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                            elif self.myhp<=self.mydamage:
                                pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                            #敵のHP
                            pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                            pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                            if self.damage==0:
                                pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                            elif self.damage<=self.hp/5:
                                pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                            elif self.hp/5<=self.damage<=self.hp*2/5:
                                pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                                pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                            elif self.hp*2/5<=self.damage<=self.hp*3/5:
                                pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                            elif self.hp*3/5<=self.damage<=self.hp*4/5:
                                pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                                pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)

                            elif self.hp*4/5<=self.damage<self.hp:
                                pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                            self.timer+=1
                            if self.timer>=60:
                                self.func1attack=False
                                self.func2attack=False
                                self.ddx=False
                                self.integral_dx=False
                                self.attackbotan=False
                                self.itembotan=False
                                self.sabilitybotan=False
                                self.retirebotan=True
                                self.timer=0

                    elif self.integral_dx==True and self.ddx_count==-1:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==-2:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==-3:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==-4:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==1:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==2:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==3:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                            
                    elif self.integral_dx==True and self.ddx_count==4:
                        pyxel.cls(0)
                        pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
                        pyxel.blt(1, 41, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(17, 41, 2, 0, 36, 3, 16, pyxel.COLOR_BLACK)  #!を表示
                        pyxel.blt(1, 72, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(30, 40, 2, 112, 40, 4, 8, pyxel.COLOR_BLACK)  # dを表示
                        pyxel.blt(24, 41, 2, 96, 32, 16, 16, pyxel.COLOR_BLACK)  # /dxを表示
                        # ↑微分に変える
                        pyxel.blt(20, 72, 2, 16, 16, 8, 16, pyxel.COLOR_BLACK)  # ∫
                        pyxel.blt(26, 71, 2, 0, 16, 16, 16, pyxel.COLOR_BLACK)  # d
                        pyxel.blt(31, 73, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)  # xを表示
                        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
                        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
                        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
                        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)

                        self.font.draw(0, 0, "リタイア", 8, 7)
                        self.font.draw(0, 10, "アイテム", 8, 7)
                        self.font.draw(0, 18, "特殊能力", 8, 7)
                        self.font.draw(0, 28, "こうげき", 8, 7)
                        self.font.draw(73, 5, "あいて", 8, 7)
                        self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
                        #自分のHP
                        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
                        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
                        if self.mydamage==0:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.mydamage<=self.myhp/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp/5<=self.mydamage<=self.myhp*2/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*2/5<=self.mydamage<=self.myhp*3/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*3/5<=self.mydamage<=self.myhp*4/5:
                            pyxel.blt(76,100,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,100,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp*4/5<=self.mydamage<self.myhp:
                            pyxel.blt(75,100,2,144,8,8,8,pyxel.COLOR_BLACK)
                        elif self.myhp<=self.mydamage:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        #敵のHP
                        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
                        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
                        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
                        if self.damage==0:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.damage<=self.hp/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp/5<=self.damage<=self.hp*2/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                            pyxel.blt(88,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*2/5<=self.damage<=self.hp*3/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*3/5<=self.damage<=self.hp*4/5:
                            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
                            pyxel.blt(80,28,2,176,0,8,8,pyxel.COLOR_BLACK)
                        elif self.hp*4/5<=self.damage<self.hp:
                            pyxel.blt(75,28,2,144,8,8,8,pyxel.COLOR_BLACK)
                        self.timer+=1
                        if self.timer>=60:
                            self.func1attack=False
                            self.func2attack=False
                            self.ddx=False
                            self.integral_dx=False
                            self.attackbotan=False
                            self.itembotan=False
                            self.sabilitybotan=False
                            self.retirebotan=True
                            self.timer=0
                


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
            x += math.pi / 4
            self.func1 = math.e**2 * x

    def battlemode(self):
        if self.hp >= 0 and self.myhp >= 0:#　お互いに生きているなら
            if self.ddx == True:
                self.func1 = sym.Derivative(self.func1).doit()
                self.hp = self.hp * 2

            elif self.integral_dx == True:
                self.func1 = sym.integrate(self.func1,x)
                self.hp = self.hp / 2

                if self.C[random.randrange(10)] != 10:
                    self.hp += self.C[random.randint(0,9)]  # 積分定数Cの値だけhpが増加
                else:
                    self.hp = 0
            
            elif self.func1attack==True:

                self.damage=self.myfunc1.subs(x,random.randint(1,6))
                self.hp-=self.damage

            elif self.func2attack==True:

                self.damage=self.myfunc2.subs(x,random.randint(1,6))
                self.hp-=self.damage

            # 敵の攻撃

            if self.phase==Phase.NORMAL_STAGE_1:
                self.mydamage=self.func1.subs(x,random.randint(1,6))
                self.myhp -= self.mydamage
            elif self.phase==Phase.NORMAL_STAGE_2:
                self.mydamage=abs(self.func2.subs(x,math.radians(self.rulet[self.num%16])))
                self.num+=1
                self.myhp-=self.mydamage
        '''
    # elif self.myhp <= 0:
        #     self.phase = Phase.GAME_OVER
        # elif self.hp <= 0 or (self.hp <= 0 and self.myhp <= 0):
        #     self.phase = Phase.GAMECLEAR
        #     self.gamestgart=False
        '''

            
    def nomalstage_2(self):
        if self.timer2 >= 145:
            self.stagescreen = False
            if InputHandler.isDecide():
                self.stagescreen=False
                self.gamestgart=True
                if self.hp<=0:
                    self.phase=Phase.GAME_CLEAR
                elif self.myhp<=0:
                    self.phase=Phase.GAME_OVER

    def end(self):
        pyxel.quit()
        
    def gameover(self):
        if self.timer>=120:
            self.phase=Phase.END
            self.timer=0
    def gameclear(self):
        self.hp=100
        self.damage=0
        self.myhp=100
        self.mydamage=0
        self.gamestgart=False
        if self.timer>=120:
            self.phase=Phase.NORMAL_STAGE_2
            self.stagescreen=True
            self.timer=0
            
        

App()
