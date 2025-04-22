import pyxel
import math
import random
import sympy as sym
import PyxelUniversalFont as puf
from enum import Enum

x= sym.symbols('x')

class Phase(Enum):
    START = "start"
    MENU = "menu"
    NORMAL_MODE = "nomalmode"
    EASY_MODE = "easiymode"
    NORMAL_STAGE_1 = "nomalstage1"
    NORMAL_STAGE_2 = "nomalstage2"
    NORMAL_STAGE_3="nomalstage3"
    NORMAL_STAGE_4="nomalstage4"
    NORMAL_STAGE_5="nomalstage5"
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

class App:
    def __init__(self):

        self.updown = False
        self.botancount=0
        self.stagescreen = False
        self.gamestgart = False
        self.itemstart=False
        self.botanstart=False
        self.func1attack=False
        self.func2attack=False
        self.attackmode=False
        self.gameover_flag=False
        self.eattack=False
        self.ddx = False
        self.ddx_count=0
        self.integral_dx = False
        self.C = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.lim_x0 = False

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
        self.item2 = 2
        self.item3 = 1
        self.item1flag=False
        self.item2flag=False
        self.item3flag=False
        self.num=0
        self.rulet = [0,sym.pi/6,sym.pi/4,sym.pi/3,sym.pi/2,sym.pi*2/3,sym.pi*3/4,sym.pi*5/6,sym.pi,sym.pi*7/6,sym.pi*5/4,sym.pi*4/3,sym.pi*3/2,sym.pi*5/3,sym.pi*7/4,sym.pi*11/6]
        self.myhp = 1000  # 自分のhp
        self.hp = 1000  # 敵のhp
        self.myfunc1=sym.factorial(x) # x!
        self.myfunc2=x
        self.func1 = math.e**2 * x  # ステージ1の敵
        self.func2=sym.tan(x)
        self.func3=1/x**2
        self.attackpower1 = self.func1
        self.damage=0
        self.mydamage=0
        self.stagecount=1

        self.phase = Phase.START

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
        elif self.phase == Phase.NORMAL_STAGE_1 or self.phase==Phase.NORMAL_STAGE_2 or self.phase==Phase.NORMAL_STAGE_3 or self.phase==Phase.NORMAL_STAGE_4 or self.phase==Phase.NORMAL_STAGE_5:
            self.nomalstage()
            if self.gamestgart == True:
                self.botan()
                self.itemfunc()
                if self.attackmode==True:
                    self.battlemode()
                    
        elif self.phase==Phase.GAME_OVER:
            self.gameover()
            self.timer+=1
            
        elif self.phase == Phase.GAME_CLEAR:
            self.gameclear()
            self.timer+=1
            
        elif self.phase == Phase.END:
            self.end()

    def botan(self):
        
        if self.botancount==0:
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.botancount+=1
            elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.end()

        elif self.botancount==1:
            if pyxel.btnp(pyxel.KEY_UP) and self.botanstart==False:
                self.botancount-=1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.botanstart==False:
                self.botancount+=1
            elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN)  and self.botanstart==False:
                self.y0 = True
                self.botanstart=True
            elif self.y0 == True:
                if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.item1flag=True
                    self.botanstart=False
                    self.x0=False
                    self.y0=False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0 = False
                    self.y1 = True
            elif self.y1 == True:
                if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.item2flag=True
                    self.botanstart=False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y1 = False
                    self.y2 = True
                elif pyxel.btnp(pyxel.KEY_UP):
                    self.y1=False
                    self.y0=True
            elif self.y2 == True:
                if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.item3flag=True
                    self.botanstart=False
                elif pyxel.btnp(pyxel.KEY_UP):
                    self.y1 = True
                    self.y2 = False

        elif self.botancount==2:
            if pyxel.btnp(pyxel.KEY_UP):
                self.botancount-=1
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.botancount+=1
            elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
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

        elif self.botancount==3:
            if pyxel.btnp(pyxel.KEY_UP) and self.botanstart==False:
                self.botancount-=1
            elif (pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN)) and self.botanstart==False:
                self.x0 = True
                self.y0 = True
                self.botanstart=True

            elif self.x0 == True and self.y0 == True:
                if pyxel.btnp(pyxel.KEY_RIGHT):
                    self.x0 = False
                    self.x1 = True
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0 = False
                    self.y1 = True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.func1attack=True
                    self.botanstart=False
                    self.x0=False
                    self.y0=False
                    self.attackmode=True

            elif self.x1 == True and self.y0 == True:
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.x0 = True
                    self.x1 = False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0 = False
                    self.y1 = True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.ddx = True
                    self.botanstart=False
                    self.x1=False
                    self.y0=False
                    if self.ddx_count!=4 and self.phase==Phase.NORMAL_STAGE_1:
                        self.ddx_count+=1
                    elif self.ddx_count!=2 and self.phase==Phase.NORMAL_STAGE_3:
                        self.ddx_count+=1
                    self.attackmode=True
            elif self.x0 == True and self.y1 == True:
                if pyxel.btnp(pyxel.KEY_UP):
                    self.y0 = True
                    self.y1 = False
                elif pyxel.btnp(pyxel.KEY_RIGHT):
                    self.x1 = True
                    self.x0 = False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0 = False
                    self.y1 = False
                    self.y2 = True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.func2attack=True
                    self.botanstart=False
                    self.attackmode=True
                    self.x0=False
                    self.y1=False

            elif self.x1 == True and self.y1 == True:
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.x0 = True
                    self.x1 = False
                elif pyxel.btnp(pyxel.KEY_UP):
                    self.y0 = True
                    self.y1 = False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0 = False
                    self.y1 = False
                    self.y2 = True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.integral_dx = True
                    self.botanstart=False
                    self.x1=False
                    self.y1=False
                    if self.ddx_count!=-4 and self.phase==Phase.NORMAL_STAGE_1:
                        self.ddx_count-=1
                    elif self.ddx_count!=-2 and self.phase==Phase.NORMAL_STAGE_3:
                        self.ddx_count-=1
                    self.attackmode=True

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
                if self.stagecount==1:
                    self.phase = Phase.NORMAL_STAGE_1
                elif self.stagecount==2:
                    self.phase=Phase.NORMAL_STAGE_2
                elif self.stagecount==3:
                    self.phase=Phase.NORMAL_STAGE_3
                elif self.stagecount==4:
                    self.phase=Phase.NORMAL_STAGE_4
                self.timer = 0
                self.timer2=0

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
                        if self.stagecount==1:
                            pyxel.blt(35, 85, 1, 0, 14, 16, 16, pyxel.COLOR_BLACK)  # 矢印
                        elif self.stagecount==2:
                            pyxel.blt(51,85,1,0,14,16,16,pyxel.COLOR_BLACK)
                        elif self.stagecount==3:
                            pyxel.blt(67,85,1,0,14,16,16,pyxel.COLOR_BLACK)
                        elif self.stagecount==4:
                            pyxel.blt(83,85,1,0,14,16,16,pyxel.COLOR_BLACK)
                        elif self.stagecount==5:
                            pyxel.blt(99,85,1,0,14,16,16,pyxel.COLOR_BLACK)
                    elif self.timer >= 45:  # 1秒後
                        pyxel.cls(0)
                        pyxel.blt(
                            35, 67, 0, 0, 0, 80, 16, pyxel.COLOR_BLACK
                        )  # ステージを表示(矢印なし)
                        self.timer = 0
            else:
                self.font.draw(100, 140, "Push return", 8, 7)
        elif self.phase == Phase.NORMAL_STAGE_1 and self.gamestgart == True:
            self.nomalscreenfunc()
            self.stage1screenfunc()
            self.myhpfunc()
            self.stage1ddx_count()
            self.hpfunc()
            if self.botancount==0:
                self.retirebotanfunc()
            elif self.botancount==1:
                self.itembotanfunc()
            elif self.botancount==2:
                self.sabilitybotanfunc()
            elif self.botancount==3:
                self.attackbotanfunc()
            if self.eattack==True:
                pyxel.blt(33,120,1,22,146,80,16)
                self.font.draw(33, 120, "e^2xが攻撃!", 8, 7)
                # self.wait2()
                self.waitob.wait2()
                        
        elif self.phase==Phase.GAME_OVER:
            pyxel.cls(0)
            pyxel.blt(50,50,0,0,48,30,8,pyxel.COLOR_BLACK) #gameoverを表示
            pyxel.blt(74,50,0,0,56,24,8,pyxel.COLOR_BLACK)
            
        elif self.phase==Phase.GAME_CLEAR:
            pyxel.cls(0)
            pyxel.blt(50,50,0,0,48,24,8,pyxel.COLOR_BLACK) #gameclearを表示
            pyxel.blt(74,50,0,0,64,64,8,pyxel.COLOR_BLACK)

            
        elif self.phase==Phase.NORMAL_STAGE_2 and self.gamestgart == True:
                self.nomalscreenfunc()
                self.stage2screenfunc()
                self.myhpfunc()
                self.hpfunc()
                if self.botancount==0:
                    self.retirebotanfunc()
                elif self.botancount==1:
                    self.itembotanfunc()
                elif self.botancount==2:
                    self.sabilitybotanfunc()
                elif self.botancount==3:
                   self.attackbotanfunc()
                if self.eattack==True:
                    pyxel.blt(33,120,1,22,146,80,16)
                    self.font.draw(33, 120, "tan(x)が攻撃!", 8, 7)
                    # self.wait2()
                    self.waitob.wait2()
                            
        elif self.phase==Phase.NORMAL_STAGE_3 and self.gamestgart == True:
                self.nomalscreenfunc()
                self.stage3screenfunc()
                self.stage3ddx_count()
                self.myhpfunc()
                self.hpfunc()
                if self.botancount==0:
                    self.retirebotanfunc()
                elif self.botancount==1:
                    self.itembotanfunc()
                elif self.botancount==2:
                    self.sabilitybotanfunc()
                elif self.botancount==3:
                   self.attackbotanfunc()
                if self.eattack==True:
                    pyxel.blt(33,120,1,22,146,80,16)
                    self.font.draw(33, 120, "1/x^2が攻撃!", 8, 7)
                    # self.wait2()
                    self.waitob.wait2()
                    
        elif self.phase==Phase.NORMAL_STAGE_4 and self.gamestgart == True:
                self.nomalscreenfunc()
                self.stage4screenfunc()
                self.myhpfunc()
                self.hpfunc()
                if self.botancount==0:
                    self.retirebotanfunc()
                elif self.botancount==1:
                    self.itembotanfunc()
                elif self.botancount==2:
                    self.sabilitybotanfunc()
                elif self.botancount==3:
                   self.attackbotanfunc()
                if self.eattack==True:
                    pyxel.blt(33,120,1,22,146,80,16)
                    self.font.draw(33, 120, "ln(cot(x))が攻撃!", 8, 7)
                    # self.wait2()
                    self.waitob.wait2()

    def itemfunc(self):
        if self.item1!=0 and self.item1flag==True:  # 自分のHPを100回復
            self.item1 -= 1
            self.myhp += 100
            self.item1flag=False
            self.y0=False
        elif self.item2!=0 and self.item2flag==True:  # 自分のHPを200回復
            self.item2 -= 1
            self.myhp += 200
            self.item2flag=False
            self.y1=False
        elif self.item3!=0 and self.item3flag==True:  #自分のHPを500回復
            self.item3-=1
            self.myhp+=500
            self.item3flag=False
            self.y2=False

    def battlemode(self):
        if self.hp >= 0 and self.myhp >= 0:
            if self.ddx == True:
                if self.phase==Phase.NORMAL_STAGE_1:
                    if self.ddx_count!=4:
                        self.func1 = sym.Derivative(self.func1).doit()
                elif self.phase==Phase.NORMAL_STAGE_2:
                    self.func2 = sym.Derivative(self.func2).doit()
                elif self.phase==Phase.NORMAL_STAGE_3:
                    if self.ddx_count!=2:
                        self.func3= sym.Derivative(self.func3).doit()

            elif self.integral_dx == True:
                if self.phase==Phase.NORMAL_STAGE_1:
                    if self.ddx_count!=4:
                        self.func1 = sym.integrate(self.func1,x)
                elif self.phase==Phase.NORMAL_STAGE_2:
                    self.func2=sym.integrate(self.func2,x)
                elif self.phase==Phase.NORMAL_STAGE_3:
                    if self.ddx_count!=-2:
                        self.func3=sym.integrate(self.func3,x)
                self.hp += self.C[random.randint(0,9)]  # 積分定数Cの値だけhpが増加
            elif self.func1attack==True:
                self.damage+=self.myfunc1.subs(x,random.randint(1,6))
               

            elif self.func2attack==True:
                self.damage+=self.myfunc2.subs(x,random.randint(1,6))
            # 敵の攻撃
            if self.phase==Phase.NORMAL_STAGE_1:
                self.mydamage+=self.func1.subs(x,random.uniform(1,6))
                print(self.damage)
            elif self.phase==Phase.NORMAL_STAGE_2:
                if self.num!=5 or self.num!=13: 
                    self.mydamage+=abs(self.func2.subs(x,math.radians(self.rulet[self.num%16])))
                    self.num+=1
                else:
                    self.mydamage=self.myhp
                
                print(self.hp)
                print(self.damage)
            elif self.phase==Phase.NORMAL_STAGE_3:
                self.mydamage=abs(self.func3.subs(x,random.uniform(0.1,3))) 
                print(self.ddx_count)
        self.attackmode=False
            
            
    def nomalstage(self):
        self.gamestgart = True
        if self.hp<=self.damage or pyxel.btn(pyxel.KEY_1):
            self.phase=Phase.GAME_CLEAR
            self.stagecount+=1
        elif self.myhp<=self.mydamage:
            self.phase=Phase.GAME_OVER

    def end(self):
        pyxel.quit()
        
    def gameover(self):
        if self.timer>=120:
            self.phase=Phase.END
            self.timer=0
    def gameclear(self):
        self.hp=1000
        self.damage=0
        self.myhp=1000
        self.mydamage=0
        self.timer2=0
        self.gamestgart=False
        self.func1attack=False
        self.func2attack=False
        self.ddx=False
        self.integral_dx=False
        self.ddx_count=0
        self.botancount==0
        self.eattack=False
       
        if self.timer>=120:
            self.stagescreen=True
            self.timer=0
            self.timer2=0
            self.phase=Phase.NORMAL_MODE
                
                
    def stagefunc1attack(self):
        pyxel.blt(33,120,1,22,146,80,16)
        self.font.draw(33, 120, "x!で攻撃！", 8, 7)
        # self.wait()
        self.waitob.wait2()
            
    def stagefunc2attack(self):
        pyxel.blt(33,120,1,22,146,80,16)
        self.font.draw(33, 120, "xで攻撃！", 8, 7)
        # self.wait()
        self.waitob.wait2()
            
    def ddxfunc(self):
        pyxel.blt(33,120,1,22,146,80,16)
        if self.phase==Phase.NORMAL_STAGE_1:
            if self.ddx_count!=4:
                self.font.draw(33, 120, "d/dxで攻撃！", 8, 7)
            else:
                self.font.draw(33, 120, "※これ以上微分できません!", 8, 7)
        elif self.phase==Phase.NORMAL_STAGE_2:
            self.font.draw(33,120,"d/dxで攻撃!",8,7)
        elif self.phase==Phase.NORMAL_STAGE_3:
            if self.ddx_count!=2:
                self.font.draw(33,120,"d/dxで攻撃!",8,7)
            else:
                self.font.draw(33,120,"※これ以上微分できません!",8,7)
        # self.wait()
        self.waitob.wait1()
        
    def integral_dxfunc(self):
        pyxel.blt(33,120,1,22,146,80,16)
        if self.phase==Phase.NORMAL_STAGE_1:
            if self.ddx_count!=-4:
                self.font.draw(33, 120, "∫dxで攻撃！", 8, 7)
            else:
                self.font.draw(33,120,"※これ以上積分できません!",8,7)
        elif self.phase==Phase.NORMAL_STAGE_2:
            self.font.draw(33,120,"∫dxで攻撃!",8,7)
        elif self.phase==Phase.NORMAL_STAGE_3:
            if self.ddx_count!=-2:
                self.font.draw(33,120,"∫dxで攻撃!",8,7)
            else:
                self.font.draw(33,120,"※これ以上積分できません!",8,7)
        # self.wait()
        self.waitob.wait2()
        
    def attackbotanfunc(self):
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
            self.stagefunc1attack()
        elif self.func2attack==True:
            self.stagefunc2attack()
        elif self.ddx==True:
            self.ddxfunc()
        elif self.integral_dx==True:
            self.integral_dxfunc()
            
    def itembotanfunc(self):
        if self.item1flag==False and self.item2flag==False and self.item3flag==False:
            pyxel.blt(0, 8, 2, 0, 67, 38, 11, pyxel.COLOR_BLACK)
            if self.y0==True:
                pyxel.blt(1,41,1,0,184,48,8,pyxel.COLOR_BLACK)
            elif self.y1==True:
                pyxel.blt(1,57,1,0,184,48,8,pyxel.COLOR_BLACK)
            elif self.y2==True:
                pyxel.blt(1,73,1,0,184,48,8,pyxel.COLOR_BLACK)
                
        
    def retirebotanfunc(self):
        pyxel.blt(0, 0, 2, 0, 60, 38, 9, pyxel.COLOR_BLACK)
        
    def sabilitybotanfunc(self):
        pyxel.blt(0, 16, 2, 0, 75, 38, 12, pyxel.COLOR_BLACK)
        
    def hpfunc(self):
        pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
        pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#[
        pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        self.font.draw(76,20,f"{self.hp-self.damage:.0f}/{self.hp}",8,7)
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
            
    def myhpfunc(self):
        pyxel.blt(104,100,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
        pyxel.blt(75,100,2,144,0,8,8,pyxel.COLOR_BLACK)#[
        pyxel.blt(83,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        pyxel.blt(90,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        pyxel.blt(97,100,2,161,0,8,8,pyxel.COLOR_BLACK)#=
        self.font.draw(76,92,f"{self.myhp-self.mydamage:.0f}/{self.myhp}",8,7)
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
            
    def stage1ddx_count(self):
        if self.ddx_count==1:
            pyxel.blt(59, 40, 2, 40, 56, 16, 16, pyxel.COLOR_BLACK)#2
        elif self.ddx_count==2:
            pyxel.blt(59, 40, 2, 56, 56, 16, 16, pyxel.COLOR_BLACK)#4
        elif self.ddx_count==3:
            pyxel.blt(59, 40, 2, 40, 72, 16, 16, pyxel.COLOR_BLACK)#8
        elif self.ddx_count==4:
            pyxel.blt(59, 40, 2, 56, 72, 16, 16, pyxel.COLOR_BLACK)#16
        elif self.ddx_count==-1:
            pyxel.blt(64, 48, 0, 0, 16, 5, 8, pyxel.COLOR_BLACK)#2
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-2:
            pyxel.blt(64, 48, 0, 5, 16, 5, 8, pyxel.COLOR_BLACK)#4
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-3:
            pyxel.blt(64, 48, 0, 10, 16, 5, 8, pyxel.COLOR_BLACK)#8
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
        elif self.ddx_count==-4:
            pyxel.blt(62, 48, 0, 0, 24, 8, 8, pyxel.COLOR_BLACK)#16
            pyxel.blt(59, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
    def stage3ddx_count(self):
        if self.ddx_count==-1:
            pyxel.blt(75, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
            pyxel.blt(75, 48, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)#x
        elif self.ddx_count==-2:
            pyxel.blt(75,40,2,147,16,18,14,pyxel.COLOR_BLACK) #ln
            pyxel.blt(95,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
            pyxel.blt(96,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
            pyxel.blt(107,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
            
        elif self.ddx_count==0:
            pyxel.blt(75, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
            pyxel.blt(75, 48, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)#x
            pyxel.blt(89, 45, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)#2
            pyxel.blt(68, 48, 0, 4, 87, 7, 2, pyxel.COLOR_BLACK)#-
            pyxel.blt(65, 40, 0, 23, 80, 2, 24, pyxel.COLOR_BLACK)#たてぼう
            pyxel.blt(93, 40, 0, 23, 80, 2, 24, pyxel.COLOR_BLACK)#たてぼう
        elif self.ddx_count==1:
            pyxel.blt(75, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
            pyxel.blt(75, 48, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)#x
            pyxel.blt(89, 45, 0, 5, 75, 3, 5, pyxel.COLOR_BLACK)#3
        elif self.ddx_count==2:
            pyxel.blt(75, 40, 2, 64, 32, 16, 16, pyxel.COLOR_BLACK)#1/
            pyxel.blt(75, 48, 2, 0, 0, 16, 16, pyxel.COLOR_BLACK)#x
            pyxel.blt(89, 45, 0, 6, 19, 4, 5, pyxel.COLOR_BLACK)#4
            pyxel.blt(68, 48, 0, 4, 87, 7, 2, pyxel.COLOR_BLACK)#-
            pyxel.blt(65, 40, 0, 23, 80, 2, 24, pyxel.COLOR_BLACK)#たてぼう
            pyxel.blt(93, 40, 0, 23, 80, 2, 24, pyxel.COLOR_BLACK)#たてぼう
        elif self.ddx_count==3:
            pyxel.blt(75,40,2,145,16,18,16,pyxel.COLOR_BLACK) #ln
            pyxel.blt(95,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
            pyxel.blt(96,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
            pyxel.blt(107,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
        elif self.ddx_count==4:
            pyxel.blt(75,40,2,145,16,18,16,pyxel.COLOR_BLACK) #ln
            pyxel.blt(95,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
            pyxel.blt(96,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
            pyxel.blt(107,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
        elif self.ddx_count==-3:
            pyxel.blt(75,40,2,145,16,18,16,pyxel.COLOR_BLACK) #ln
            pyxel.blt(95,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
            pyxel.blt(96,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
            pyxel.blt(107,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
        elif self.ddx_count==-4:
            pyxel.blt(75,40,2,145,16,18,16,pyxel.COLOR_BLACK) #ln
            pyxel.blt(95,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
            pyxel.blt(96,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
            pyxel.blt(107,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
            
    def nomalscreenfunc(self):
        if self.botancount==1:
            pyxel.cls(0)
            pyxel.blt(0, 0, 1, 0, 24, 150, 150, pyxel.COLOR_BLACK)  # 対戦画面を表示
            self.font.draw(1,41,f"HP+100 {self.item1}/5",8,7)
            self.font.draw(1,57,f"HP+200 {self.item2}/2",8,7)
            self.font.draw(1,73,f"HP+500 {self.item3}/1",8,7)
            self.font.draw(0, 0, "リタイア", 8, 7)
            self.font.draw(0, 10, "アイテム", 8, 7)
            self.font.draw(0, 18, "特殊能力", 8, 7)
            self.font.draw(0, 28, "こうげき", 8, 7)
            self.font.draw(73, 5, "あいて", 8, 7)
        else:
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
            self.font.draw(0, 0, "リタイア", 8, 7)
            self.font.draw(0, 10, "アイテム", 8, 7)
            self.font.draw(0, 18, "特殊能力", 8, 7)
            self.font.draw(0, 28, "こうげき", 8, 7)
            self.font.draw(73, 5, "あいて", 8, 7)
        
    def stage1screenfunc(self):
        pyxel.blt(75, 40, 2, 32, 0, 16, 16, pyxel.COLOR_BLACK)  # e
        pyxel.blt(88, 37, 0, 2, 19, 3, 5, pyxel.COLOR_BLACK)  # ^2を表示
        pyxel.blt(92, 37, 2, 31, 44, 5, 5, pyxel.COLOR_BLACK)  # ^xを表示
        self.font.draw(33, 120, "e^2xが現れた！", 8, 7)
    def stage2screenfunc(self):
        pyxel.blt(75,40,2,112,0,32,16, pyxel.COLOR_BLACK) #tan
        pyxel.blt(107,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
        pyxel.blt(113,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
        pyxel.blt(129,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
        self.font.draw(33, 120, "tan(x)が現れた！", 8, 7)
        
    def stage3screenfunc(self):
        self.stage3ddx_count()
        self.font.draw(33, 120, "1/x^2が現れた！", 8, 7)
        
    def stage4screenfunc(self):
        pyxel.blt(59,40,2,145,16,18,16,pyxel.COLOR_BLACK) #ln
        pyxel.blt(79,40,2,80,16,6,16,pyxel.COLOR_BLACK) #(
        pyxel.blt(116,40,2,0,0,16,16,pyxel.COLOR_BLACK) #x
        pyxel.blt(127,40,2,106,16,6,16,pyxel.COLOR_BLACK) #)
        pyxel.blt(84,38,2,120,32,31,16,pyxel.COLOR_BLACK) #cot
        self.font.draw(33,120,"ln(cot(x))が現れた!",8,7)
        
class wait(App):
    def wait1(self):
        self.timer+=1
        if self.timer>=60:
            self.func1attack=False
            self.func2attack=False
            self.ddx=False
            self.integral_dx=False
            self.botancount=4
            self.eattack=True
            self.timer=0
            
    def wait2(self):
        self.timer2+=1
        if self.timer2>=60:
            self.botancount=0
            self.eattack=False
            self.timer2=0
            
        

App()
