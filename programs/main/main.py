import pyxel
import time
import math
import random
import sympy as sym
import PyxelUniversalFont as puf
class App:
    def __init__(self):

        self.updown=False
        self.itembotan=False
        self.retirebotan=True
        self.sabilitybotan=False
        self.attackbotan=False
        #self.nabla=False
        #self.delta=False
        #self.round_x=False
        #self.round_y=False
        #self.lim_00=False
        #self.lim_mm=False
        self.ddx=False
        #self.ddy=False
        self.integral_dx=False
        self.C={1,2,3,4,5,6,7,8,9,10}#10は無限大扱い
        #self.integral_dy=False
        self.lim_x0=False
        #self.lim_y0=False
        self.z=random.randrange(1,6)
        
        self.font=puf.Writer("misaki_gothic.ttf")  #フォントを指定
        
        #ゲームの操作用座標
        self.x0=True
        self.x1=False
        self.x2=False
        self.y0=True
        self.y1=False
        self.y2=False
        self.phase="start"
        
        #アイテム
        self.item1=5
        self.item2=5
        self.item3=5
        self.item4=5
        
        self.rulet = {16: {}}
        self.myhp=100  #自分のhp
        self.hp=100  #敵のhp
        self.myfunc1=math.factorial(self.z)  #x!
        self.func1=math.e**2*self.z  #ステージ1の敵
        self.attackpower1=self.func1
        
        pyxel.init(160, 120, title="The Integral War")
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)
        
        
        
        
    def update(self):
        if self.phase=="start":
            self.start()
        elif self.phase=="menu":
            self.menu()
        elif self.phase=="nomalmode":
            self.nomalmode()
        elif self.phase=="easiymode":
            self.easiymode()
        elif self.phase=="nomalstage1":
            self.nomalstage1()
        elif self.phase=="gameclear":
            self.gameclear()
        elif self.phase=="end":
            self.end()
        
        
        
        
    
    def botan(self):
        for i in range(4):
            if self.retirebotan==True:
                if pyxel.btnp(pyxel.KEY_DOWN):
                    self.itembotan=True
                    self.retirebotan=False
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.end()
                    
            if self.itembotan==True:
                if pyxel.btnp(pyxel.KEY_UP):
                    self.itembotan=False
                    self.retirebotan=True
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.itembotan=False
                    self.sabilitybotan=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.item1-=1
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x1==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.item2-=1
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.item3-=1
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y0=True
                            self.y1=False
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.item4-=1
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y0=True
                            self.y1=False
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        
                            
            if self.sabilitybotan==True:
                if pyxel.btnp(pyxel.KEY_UP):
                    self.sabilitybotan=False
                    self.itembotan=True
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.sabilitybotan=False
                    self.attackbotan=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.nabla=True
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x1==True and self.y0==0:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.delta=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x1=False
                            self.x0=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x0==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.round_x=True
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y1=False
                            self.y0=True
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y1=False
                            self.y2=True
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.round_y=True
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y1=False
                            self.y0=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x1=False
                            self.x0=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y1=False
                            self.y2=True
                    elif self.x0==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.lim_00=True
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y2=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                    elif self.x1==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.lim_mm=True
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y2=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                            
            if self.attackbotan==True:
                if pyxel.btnp(pyxel.KEY_UP):
                    self.attackbotan=False
                    self.sabilitybotan=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.ddx=True
                    elif self.x1==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.ddy=True
                    elif self.x0==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.y0=True
                            self.y1=False
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x1=True
                            self.x0=False
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=False
                            self.y2=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.integral_dx=True
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y0=True
                            self.y1=False
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=False
                            self.y2=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.integral_dy=True
                    elif self.x0==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.y0=False
                            self.y1=True
                            self.y2=False
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.lim_x0=True
                    elif self.x1==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.y1=True
                            self.y0=False
                            self.y2=False
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                            self.lim_y0=True
                        
            
    
    def start(self):
        pyxel.blt(0,0,0,0,0,160,120,pyxel.COLOR_BLACK) #スタート画面を表示
        if pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.phase="menu"
            
    def menu(self):
        pyxel.blt(0,0,0,0,0,160,120)
        if pyxel.btnp(pyxel.KEY_UP):
            self.updown=False
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.updown=True
        
        if self.updown==False:
            if pyxel.btnp(pyxel.KEY_KP_ENTER):
                self.phase="nomalmode"
        elif self.updown==True:
            if pyxel.btnp(pyxel.KEY_KP_ENTER):
                self.phase="easiymode"
                
    def nomalmode(self):
        
        #self.startsec=time.time
        pyxel.blt(0,72,0,0,0,80,16) #ステージを表示(矢印なし)
        time.sleep(0.5)
        pyxel.blt(0,72,0,0,0,80,16) #ステージ1を表示
        pyxel.blt(24,18,1,0,0,16,16)#矢印
        time.sleep(0.5)
        pyxel.blt(0,72,0,0,0,80,16) #ステージを表示(矢印なし)
        time.sleep(0.5)
        pyxel.blt(0,72,0,0,0,80,16) #ステージ1を表示
        pyxel.blt(24,18,1,0,0,16,16)#矢印
        time.sleep(0.5)
        pyxel.blt(0,72,0,0,0,80,16) #ステージを表示(矢印なし)
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,16,160,120) #真っ黒を表示
        time.sleep(2)
        self.phase="nomalstage1"
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # self.nomalstage2()
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.nomalstage3()
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.nomalstage4()
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.nomalstage5()
        # self.end()
    # def easiymode(self):
    #     self.items=[True]*1000000
    #     pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
    #     time.sleep(0.5)
    #     pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
    #     time.sleep(2)
    #     self.easiystage1()
        
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.easiystage3()
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.easiystage4()
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        # time.sleep(0.5)
        # pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        # time.sleep(0.5)
        # self.easiystage5()
        # self.end()
    
    def nomalstage1(self):
        pyxel.blt(0,0,0,0,0,160,120)#敵を表示
        pyxel.blt(0,0,0,0,0,160,120)#対戦画面を表示
        while self.hp>0 and self.myhp>0:
            self.botan()
            if self.ddx==True:
                self.func1=sym.Derivative(self.func1).doit()
                self.hp=self.hp*2
            if self.integral_dx==True:
                self.func1=sym.integrate(self.func1)
                self.hp=self.hp/2
                if self.C[random.randrange(10)]!=10:
                    self.hp+=self.C[random.randrange(10)]#積分定数Cの値だけhpが増加
                else:
                    self.hp=0
            if self.item1:#自分のHPを50回復
                self.items-=1
                self.myhp+=50
            if self.item2:#自分のHPを100回復
                self.items-=1
                self.myhp+=100
            if self.item3:#相手のターンを一回無視
                self.items-=1
                #相手のターンを無視する処理
            if self.item4:#"アイデアがほしいです"
                self.items-=1
                
            #自分の攻撃
            self.z=random.randrange(10) #←ここの確率を調整してください。出やすさ:2>3>4>1>5>6
            self.myfunc1=math.factorial(self.z)#このときの自分の関数:x!
            self.hp=self.hp-self.myfunc1
            
            #敵の攻撃
            self.z=random.randrange(6)
            self.func1=math.e**self.z*2
            self.myhp-=self.func1
        if self.myhp<=0:
            self.phase="end"
        elif self.hp<=0 or (self.hp<=0 and self.myhp<=0):
            self.phase="gameclear"
            

        
    # def nomalstage2(self):
        
    # def nomalstage3(self):
        
    # def nomalstage4(self):
        
    # def nomalstage5(self):
    
    # def easiystage1(self):
    
    # def easiystage2(self):
        
    # def easiystage3(self): 
        
    # def easiystage4(self): 
        
    # def easiystage5(self):   
    
    def gameclear(self):
        pyxel.blt(0,0,0,0,0,160,120) #対戦画面を表示
        self.font.draw(0,0, "game clear!", 50, 13) #テロップにgame clear!と表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        for i in range(3):
            pyxel.blt(0,72,0,0,0,80,16) #ステージを表示(矢印なし)
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示(矢印あり)
            pyxel.blt(24,18,1,0,0,16,16)#矢印
            time.sleep(0.5)  
        self.end()
            
    def end(self):
        pyxel.blt(0,0,0,0,16,160,120) #真っ黒を表示
        self.start()
        

App()