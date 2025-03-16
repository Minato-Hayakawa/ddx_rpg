import pyxel
import time
import math
import random
import sympy as sym
class App:
    def _init_(self):
        self.updown=False
        pyxel.init(160,120,title="The Integral War")
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update,self.draw)
        self.itembotan=False
        self.retirebotan=True
        self.sabilitybotan=False
        self.attackbotan=False
        self.nabla=False
        self.delta=False
        self.round_x=False
        self.round_y=False
        self.lim_00=False
        self.lim_mm=False
        self.ddx=False
        self.ddy=False
        self.integral_dx=False
        self.integral_dy=False
        self.lim_x0=False
        self.lim_y0=False
        self.z=random.randrange(6)
        self.x0=True
        self.x1=False
        self.x2=False
        self.y0=True
        self.y1=False
        self.y2=False
        self.rulet[16]={}
        self.myhp=100
        self.hp=100
        self.myfunc1=math.factorial(self.z)
        self.func1=math.e^2*self.z
        self.attackpower1=self.func1
    def botan(self):
        for i in range(4):
            if self.retirebotan==True:
                if pyxel.btnp(pyxel.KEY_DOWN):
                    self.itembotan=True
                    self.retirebotan=False
                elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                    self.gameover()
                    
            if self.itembotan==True:
                if pyxel.btnp(pyxel.KEY_UP):
                    self.itembotan=False
                    self.retirebotan=True
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.itembotan=False
                    self.sabilitybotan=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.item1[0]=False
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x1==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.item2[0]=False
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.item3[0]=False
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y0=True
                            self.y1=False
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                    elif self.x1==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.item4[0]=False
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
                elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.nabla=True
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x1==True and self.y0==0:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.delta=True
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x1=False
                            self.x0=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                    elif self.x0==True and self.y1==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
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
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
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
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.lim_00=True
                        elif pyxel.btnp(pyxel.KEY_UP):
                            self.y2=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                    elif self.x1==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_KP_ENTER):
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
                elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                    self.x0=True
                    self.y0=True
                    if self.x0==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.ddx=True
                    elif self.x1==True and self.y0==True:
                        if pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                        elif pyxel.btnp(pyxel.KEY_DOWN):
                            self.y0=False
                            self.y1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
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
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
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
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.integral_dy=True
                    elif self.x0==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.y0=False
                            self.y1=True
                            self.y2=False
                        elif pyxel.btnp(pyxel.KEY_RIGHT):
                            self.x0=False
                            self.x1=True
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.lim_x0=True
                    elif self.x1==True and self.y2==True:
                        if pyxel.btnp(pyxel.KEY_UP):
                            self.y1=True
                            self.y0=False
                            self.y2=False
                        elif pyxel.btnp(pyxel.KEY_LEFT):
                            self.x0=True
                            self.x1=False
                        elif pyxel.btnp(pyxel.KEY_KP_ENTER):
                            self.lim_y0=True
                        
            
    
    def start(self):
        pyxel.blt(0,0,0,0,0,160,120,pyxel.COLOR_BLACK) #スタート画面を表示
        if pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.menu()
            
    def menu(self):
        pyxel.blt(0,0,0,0,0,160,120)
        if pyxel.btnp(pyxel.KEY_UP):
            self.updown=False
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.updown=True
        
        if self.updown==False:
            if pyxel.btnp(pyxel.KEY_KP_ENTER):
                self.nomalmode()
        elif self.updown==True:
            if pyxel.btnp(pyxel.KEY_KP_ENTER):
                self.easiymode()
                
    def nomalmode(self):
        self.item1=[True]*5
        self.item2=[True]*5
        self.item3=[True]*5
        self.item4=[True]*5
        self.startsec=time.time
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(2)
        self.nomalstage1()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        self.nomalstage2()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.nomalstage3()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.nomalstage4()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.nomalstage5()
        self.end()
    def easiymode(self):
        self.items=[True]*1000000
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ1を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(2)
        self.easiystage1()
        
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ3を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.easiystage3()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ4を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.easiystage4()
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #ステージ5を表示
        time.sleep(0.5)
        pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
        time.sleep(0.5)
        self.easiystage5()
        self.end()
    
    def nomalstage1(self):
        pyxel.blt(0,0,0,0,0,160,120)#敵を表示
        pyxel.blt(0,0,0,0,0,160,120)#対戦画面を表示
        while self.hp<=0 or self.myhp<=0:
            self.botan()
            if self.ddx==True:
                self.func1=sym.Derivative(self.func1)
                self.hp=self.hp*2
            if self.item1[0]==False:#自分のHPを50回復
                self.items-=1
                self.myhp+=50
            if self.item2[0]==False:#自分のHPを100回復
                self.items-=1
                self.myhp+=100
            if self.item3[0]==False:#相手のターンを一回無視
                self.items-=1
                #相手のターンを無視する処理
            if self.item4[0]==False:#"アイデアがほしいです"
                self.items-=1
            self.z=random.randrange(10) #←ここの確率を調整してください。出やすさ:2>3>4>1>5>6
            self.myfunc1=math.factorial(self.z)
            self.hp=self.hp-self.myfunc1
            
            #敵の攻撃
            self.z=random.randrange(6)
            self.func1=math.e^self.z*2
            self.myhp-=self.func1
        if self.myhp<=0:
            self.gameover()
        elif self.hp<=0:
            pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ0を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #ステージ2を表示
            time.sleep(0.5)
            pyxel.blt(0,0,0,0,0,160,120) #真っ黒を表示
            self.easiystage2()
        elif self.hp<=0 and self.myhp<=0:
            self.gameover()
        
    def nomalstage2(self):
        
    def nomalstage3(self):
        
    def nomalstage4(self):
        
    def nomalstage5(self):
    
    def easiystage1(self):
    
    def easiystage2(self):
        
    def easiystage3(self): 
        
    def easiystage4(self): 
        
    def easiystage5(self):     
    def end(self):
        
    def gameover(self):
        

App()