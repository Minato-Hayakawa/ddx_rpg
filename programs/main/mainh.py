import pyxel
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
        self.stagescreen=False
        self.gamestgart=False
        self.botanstart=False
        self.ddx=False
        #self.ddy=False
        self.integral_dx=False
        self.C={1,2,3,4,5,6,7,8,9,10}#10は無限大扱い
        #self.integral_dy=False
        self.lim_x0=False
        #self.lim_y0=False
        self.z=random.randrange(1,6)
        self.timer=0
        self.timer2=0
        
        self.font=puf.Writer("misaki_gothic.ttf")  #フォントを指定
        
        #ゲームの操作用座標
        self.x0=False
        self.x1=False
        self.x2=False
        self.y0=False
        self.y1=False
        self.y2=False
        self.y3=False
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
        
        pyxel.init(150, 150, title="The Integral War")
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)
        
        
        
        
    def update(self):
        if self.phase=="start":
            self.start()
        elif self.phase=="menu":
            self.menu()
        elif self.phase=="nomalmode":
            self.timer+=1
            self.timer2+=1
            self.nomalmode()
        elif self.phase=="easiymode":
            self.easiymode()
        elif self.phase=="nomalstage1":
            self.nomalstage1()
            if self.gamestgart==True:
                self.botan()
                #self.itemfunc()
        elif self.phase=="nomalstage2":
            self.nomalstage2()
            self.botan()
        elif self.phase=="gameclear":
            self.gameclear()
        elif self.phase=="end":
            self.end()
        
        
        
        
        
        
        
        
        
        
        
    
    def botan(self):
        if self.retirebotan==True:
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.itembotan=True
                self.retirebotan=False
            elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.end()
                
        elif self.itembotan==True:
            if pyxel.btnp(pyxel.KEY_UP):
                self.itembotan=False
                self.retirebotan=True
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.itembotan=False
                self.sabilitybotan=True
            elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.attackbotan=False
                self.x0=True
                self.y0=True
                if self.x0==True and self.y0==True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item1-=1
                    elif pyxel.btnp(pyxel.KEY_DOWN) and self.y0==True:
                        self.y0=False
                        self.y1=True
                elif self.x0==True and self.y1==True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item2-=1
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y1=False
                        self.y2=True
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y1=False
                        self.y0=True
                elif self.x0==True and self.y2==True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item3-=1
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y1=True
                        self.y2=False
                    elif pyxel.btnp(pyxel.KEY_DOWN):
                        self.y3=True
                        self.x2=False
                elif self.x0==True and self.y3==True:
                    if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                        self.item4-=1
                    elif pyxel.btnp(pyxel.KEY_UP):
                        self.y2=True
                        self.y3=False
            
                    
                        
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
            elif self.botanstart==False and (pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN)):
                self.x0=True
                self.y0=True
                self.botanstart=True
            elif self.x0==True and self.y0==True and (self.botanstart==True or self.botanstart==False):
                if pyxel.btnp(pyxel.KEY_RIGHT):
                    self.x0=False
                    self.x1=True
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0=False
                    self.y1=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    #x!をtrue
                    self.botanstart=False
            elif self.x1==True and self.y0==True and (self.botanstart==True or self.botanstart==False):
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.x0=True
                    self.x1=False
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.y0=False
                    self.y1=True
                elif pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                    self.ddx=True
                    self.botanstart=False
            elif self.x0==True and self.y1==True and (self.botanstart==True or self.botanstart==False):
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
                    #xをtrue
                    self.botanstart=False
            elif self.x1==True and self.y1==True and (self.botanstart==True or self.botanstart==False):
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
                    self.integral_dx=True
                    self.botanstart=False
                        
            
    
    def start(self):
        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
            self.phase="menu"
            
    def menu(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.updown=False
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.updown=True
        
        if self.updown==False:
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.phase="nomalmode"
                self.stagescreen=True
        elif self.updown==True:
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.phase="easiymode"
                self.stagescreen=True
        
                
    def nomalmode(self):
        if self.timer2>=145:
            self.stagescreen=False
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.phase="nomalstage1"
    
    def nomalstage1(self):
        self.gamestgart=True
            
            
            

        
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
    #     self.phase="end"
            
    # def end(self):
    #     pyxel.blt(30,0,0,0,16,50,120) #真っ黒を表示
    #     self.start()
        
    def draw(self):
        if self.phase=="start":
            pyxel.blt(10,15,0,96,0,140,80,pyxel.COLOR_BLACK) #スタート画面を表示
            pyxel.blt(42,79,1,16,0,65,16,pyxel.COLOR_BLACK)
            self.font.draw(22, 43, "∫積分伝説〜勇者とdxの旅〜",8, 13)
            self.font.draw(46,83,"Enterでスタート",8,13)
        elif self.phase=="menu":
            pyxel.cls(0)
            pyxel.blt(10,15,0,96,0,140,120,pyxel.COLOR_BLACK) #スタート画面を表示
            self.font.draw(22, 43, "∫積分伝説〜勇者とdxの旅〜",8, 13)
            self.font.draw(58,83,"ノーマル",8,13)
            self.font.draw(59,115,"イージー",8,13)
            if self.updown==False:
                pyxel.blt(42,79,1,16,0,65,16,pyxel.COLOR_BLACK)
            elif self.updown==True:
                pyxel.blt(42,111,1,16,0,65,16,pyxel.COLOR_BLACK)
        elif self.phase=="nomalmode":
            if self.stagescreen==True:
                pyxel.cls(0)
                for i in range(3):
                    pyxel.blt(35,67,0,0,0,80,16,pyxel.COLOR_BLACK) #ステージを表示(矢印なし)
                    if 45>=self.timer>=30: #1秒後
                        pyxel.blt(35,67,0,0,0,80,16,pyxel.COLOR_BLACK) #ステージを表示(矢印なし)
                        pyxel.blt(35,85,1,0,14,16,16,pyxel.COLOR_BLACK)#矢印
                    elif self.timer>=45: #1秒後
                        pyxel.cls(0)
                        pyxel.blt(35,67,0,0,0,80,16,pyxel.COLOR_BLACK) #ステージを表示(矢印なし)
                        self.timer=0
            else:
                self.font.draw(100,140,"Push return",8,7)
        elif self.phase=="nomalstage1" and self.gamestgart==True:
            pyxel.cls(0)
            pyxel.blt(0,0,1,0,24,150,150,pyxel.COLOR_BLACK)#対戦画面を表示
            pyxel.blt(1,41,2,0,0,16,16,pyxel.COLOR_BLACK)#xを表示
            pyxel.blt(17,41,2,0,36,3,16,pyxel.COLOR_BLACK)#!を表示
            pyxel.blt(1,72,2,0,0,16,16,pyxel.COLOR_BLACK)#xを表示
            pyxel.blt(24,41,2,0,0,16,16,pyxel.COLOR_BLACK)#xを表示
            pyxel.blt(40,41,0,2,19,3,5,pyxel.COLOR_BLACK)#^2を表示
            #↑微分に変える
            pyxel.blt(22,72,0,0,32,16,16,pyxel.COLOR_BLACK)#∫d
            pyxel.blt(33,72,2,0,0,16,16,pyxel.COLOR_BLACK)#xを表示
            pyxel.blt(75,40,2,32,0,16,16,pyxel.COLOR_BLACK)#e
            pyxel.blt(88,37,0,2,19,3,5,pyxel.COLOR_BLACK)#^2を表示
            pyxel.blt(92,37,2,31,44,5,5,pyxel.COLOR_BLACK)#^xを表示
            
            
            self.font.draw(0,0,"リタイア",8,7)
            self.font.draw(0,10,"アイテム",8,7)
            self.font.draw(0,18,"特殊能力",8,7)
            self.font.draw(0,28,"こうげき",8,7)
            self.font.draw(73,5,"あいて",8,7)
            self.font.draw(33,120,"e^2xが現れた！",8,7)
            pyxel.blt(75,28,2,144,0,8,8,pyxel.COLOR_BLACK)#HPを表示
            pyxel.blt(83,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(90,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(97,28,2,161,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(104,28,2,184,8,16,8,pyxel.COLOR_BLACK)#HPを表示
            pyxel.blt(76,28,2,176,0,8,8,pyxel.COLOR_BLACK)#緑を表示
            pyxel.blt(84,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(92,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            pyxel.blt(96,28,2,176,0,8,8,pyxel.COLOR_BLACK)
            if self.retirebotan==True:
                pyxel.blt(0,0,2,0,60,38,9,pyxel.COLOR_BLACK)
            elif self.itembotan==True:
                pyxel.blt(0,8,2,0,67,38,11,pyxel.COLOR_BLACK)
            elif self.sabilitybotan==True:
                pyxel.blt(0,16,2,0,75,38,12,pyxel.COLOR_BLACK)
            elif self.attackbotan==True:
                pyxel.blt(0,27,2,0,93,38,11,pyxel.COLOR_BLACK)
                if self.x0==True and self.y0==True:
                    pyxel.blt(1,41,0,16,16,16,16,pyxel.COLOR_BLACK)
                elif self.x1==True and self.y0==True:
                    pyxel.blt(24,41,0,16,16,16,16,pyxel.COLOR_BLACK)
                elif self.x0==True and self.y1==True:
                    pyxel.blt(1,72,0,16,16,16,16,pyxel.COLOR_BLACK)
                elif self.x1==True and self.y1==True:
                    pyxel.blt(24,72,0,16,16,16,16,pyxel.COLOR_BLACK)
            # elif self.itembotan==True:
            #     pyxel.blt(0,8,2,0,67,38,11,pyxel.COLOR_BLACK)
            #     if self.x0==True and self.y0==True:
            #         pyxel.cls(0)
            #         pyxel.blt(0,0,1,0,24,150,150,pyxel.COLOR_BLACK)#対戦画面を表示
            #         pyxel.blt(0,27,2,0,93,38,11,pyxel.COLOR_BLACK)
            #         self.font.draw(1,41,"+50かいふく",8,7)
            #         self.font.draw(1,50,"+100かいふく",8,7)
            #         self.font.draw(1,60,"ターン無視",8,7)
            #         self.font.draw(1,70,"位相ずらし",8,7)
            #         self.font.draw(0,0,"リタイア",8,7)
            #         self.font.draw(0,10,"こうげき",8,7)
            #         self.font.draw(0,18,"特殊能力",8,7)
            #         self.font.draw(0,28,"アイテム",8,7)
            #         pyxel.blt(0,41,2,0,104,48,16,pyxel.COLOR_BLACK)
            #     elif self.x0==True and self.y1==True:
            #         pyxel.cls(0)
            #         pyxel.blt(0,0,1,0,24,150,150,pyxel.COLOR_BLACK)#対戦画面を表示
            #         pyxel.blt(0,27,2,0,93,38,11,pyxel.COLOR_BLACK)
            #         self.font.draw(1,41,"+50かいふく",8,7)
            #         self.font.draw(1,50,"+100かいふく",8,7)
            #         self.font.draw(1,60,"ターン無視",8,7)
            #         self.font.draw(1,70,"位相ずらし",8,7)
            #         self.font.draw(0,0,"リタイア",8,7)
            #         self.font.draw(0,10,"こうげき",8,7)
            #         self.font.draw(0,18,"特殊能力",8,7)
            #         self.font.draw(0,28,"アイテム",8,7)
            #         pyxel.blt(0,50,2,0,104,48,16,pyxel.COLOR_BLACK)
            #     elif self.x0==True and self.y2==True:
            #         pyxel.cls(0)
            #         pyxel.blt(0,0,1,0,24,150,150,pyxel.COLOR_BLACK)#対戦画面を表示
            #         pyxel.blt(0,27,2,0,93,38,11,pyxel.COLOR_BLACK)
            #         self.font.draw(1,41,"+50かいふく",8,7)
            #         self.font.draw(1,50,"+100かいふく",8,7)
            #         self.font.draw(1,60,"ターン無視",8,7)
            #         self.font.draw(1,70,"位相ずらし",8,7)
            #         self.font.draw(0,0,"リタイア",8,7)
            #         self.font.draw(0,10,"こうげき",8,7)
            #         self.font.draw(0,18,"特殊能力",8,7)
            #         self.font.draw(0,28,"アイテム",8,7)
            #         pyxel.blt(0,60,2,0,104,48,16,pyxel.COLOR_BLACK)
            #     elif self.x0==True and self.y3==True:
            #         pyxel.cls(0)
            #         pyxel.blt(0,0,1,0,24,150,150,pyxel.COLOR_BLACK)#対戦画面を表示
            #         pyxel.blt(0,27,2,0,93,38,11,pyxel.COLOR_BLACK)
            #         self.font.draw(1,41,"+50かいふく",8,7)
            #         self.font.draw(1,50,"+100かいふく",8,7)
            #         self.font.draw(1,60,"ターン無視",8,7)
            #         self.font.draw(1,70,"位相ずらし",8,7)
            #         self.font.draw(0,0,"リタイア",8,7)
            #         self.font.draw(0,10,"こうげき",8,7)
            #         self.font.draw(0,18,"特殊能力",8,7)
            #         self.font.draw(0,28,"アイテム",8,7)
            #         pyxel.blt(0,70,2,0,104,48,16,pyxel.COLOR_BLACK)
                #if self.x0==True and self.y0==True:
                #self.font.draw()#文字を表示
        # elif self.phase=="nomalstage2":
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
            
    # def itemfunc(self):
    #     if self.item1:#自分のHPを50回復
    #                 self.item1-=1
    #                 self.myhp+=50
    #     if self.item2:#自分のHPを100回復
    #                 self.item2-=1
    #                 self.myhp+=100
    #     if self.item3:#相手のターンを一回無視
    #                 self.item3-=1
    #                 #相手のターンを無視する処理
    #     if self.item4:#"相手の関数の位相を+π/4ずらす"
    #                 self.item4-=1
    #                 self.z+=math.pi/4
    #                 self.func1=math.e**2*self.z
                    
    def battlemode(self):
        if self.hp>=0 and self.myhp>=0:
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

                    
                #自分の攻撃
                self.z=random.randrange(10) #←ここの確率を調整してください。出やすさ:2>3>4>1>5>6
                self.myfunc1=math.factorial(self.z)#このときの自分の関数:x!
                self.hp=self.hp-self.myfunc1
                
                #敵の攻撃
                self.z=random.randrange(6)
                self.func1=math.e**self.z*2
                self.myhp-=self.func1
        elif self.myhp<=0:
            self.phase="end"
        elif self.hp<=0 or (self.hp<=0 and self.myhp<=0):
            self.phase="gameclear"
                
                
            
        

App()