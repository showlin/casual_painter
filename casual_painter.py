# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:36:42 2020

@author: LIN
"""

 
import os, sys, random
import pygame 


from pygame.locals import *
 
from draw import *
from define_variable import *




class Image(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, window_width, window_height,image):
        super().__init__()
        # 載入圖片
        self.raw_image = pygame.image.load(image)#.convert_alpha()
        # 縮小圖片
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        # 回傳位置
        self.rect = self.image.get_rect()
        # 定位
        self.rect.topleft = (x,y)
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height

def randRGB(range1=150,range2=230):
    r = random.randint(range1,range2)
    g = random.randint(range1,range2)
    b = random.randint(range1,range2)
    return r,g,b


# 視窗大小.
canvas_width = 1400
canvas_height = 750
 
# 顏色.
background = (245,245,245)    #100 0 0 咖啡色
color_type = "random"   #/choose

# 磚塊數量串列.
bricks_list = []
# 線條數量串列.
lines_list = []
# 圓形數量串列.
circles_list = []
# 三角形數量串列.
triangles_list = []
#預設圖-動態
shapes_list = []
#複製欄
copy_list=[]
copy_object=0

color_r = 137
color_g = 127
color_b = 117
 
# 點數目.      0:等待   1:點1次 2:點2次
m = 0

# 刪除狀態.      0:等待   1:刪除
d = 0

#工具狀態:
tool = "brick" # circle,line,triangle,paint,delete,back_ground,camara,copy,background
draw = 1

copy_mode=0

#按鈕狀態        0沒按   1:有案
click = 0



#-------載入圖片
circle_image = Image(image_width, image_height, 5,500 , canvas_width,canvas_height,"圓.png")
triangle_image = Image(image_width, image_height, 5,550 , canvas_width,canvas_height,"三角形.png")
brick_image = Image(image_width, image_height, 5,600 , canvas_width,canvas_height,"長方形.png")
hand_image = Image(image_width, image_height, 60,650 , canvas_width,canvas_height,"手.png")
line_image = Image(image_width, image_height, 5,650 , canvas_width,canvas_height,"線.png")
cut_image = Image(image_width, image_height, 60,600 , canvas_width,canvas_height,"剪刀.png")
copy_image = Image(image_width, image_height, 60,550 , canvas_width,canvas_height,"拷貝.png")
paint_image = Image(image_width, image_height, 60,500 , canvas_width,canvas_height,"油漆.png")
camara_image = Image(image_width, image_height, 60,430 , canvas_width,canvas_height,"相機.png")
background_image = Image(image_width, image_height, 60,380 , canvas_width,canvas_height,"版面.png")
music_image = Image(image_width, image_height, 60,330 , canvas_width,canvas_height,"音樂.png")
#方塊編號
i=0 
i1=0
i2=0
i3=0
i4=0
#-------------------------------------------------------------------------
# 函數:秀字.
#-------------------------------------------------------------------------
def showFont( text, x, y):
    global canvas    
    text = font.render(text, 1, (255, 180, 180)) 
    canvas.blit( text, (x,y))
 
#-------------------------------------------------------------------------
# 函數:碰撞判斷.
#   x       : x 
#   y       : y 
#   boxRect : 矩形
#-------------------------------------------------------------------------
def isCollision( x, y, shape):
    if(type(shape)==Box ):
        if (x >= shape.rect[0] and x <= shape.rect[0] + shape.rect[2] and y >= shape.rect[1] and y <= shape.rect[1] + shape.rect[3]):
            return True;          
        return False;  
    if(type(shape)==Circle ):
        if (  ((x-shape.pos[0])**2+(y-shape.pos[1])**2)**0.5 <=shape.radius   ):
            return True;          
        return False;  
    if(type(shape)==Line ):
        if( (shape.pos1[0]==shape.pos2[0])  ):  #防止下面算斜率跑出無限大
            if((shape.pos1[0]==x) and( (shape.pos1[1]<=y<= shape.pos2[1]) or (shape.pos2[1]<=y<= shape.pos1[1]) )):
                return True
            else:
                return False
        
        
        elif(     (shape.pos1[0]<=x<= shape.pos2[0]) or(shape.pos2[0]<=x<= shape.pos1[0])                 ) :
            
            if((shape.pos1[1]<=y<= shape.pos2[1]) or(shape.pos2[1]<=y<= shape.pos1[1])    ):
                
                slope =  (shape.pos2[1]-shape.pos1[1])/(shape.pos2[0]-shape.pos1[0])
                #print("slope:",slope)
                #print(y,int(shape.pos1[1]+slope*(x-shape.pos1[0]) ))
                #如果沒有這行，下面有時候斜率太大會出包
                if(abs(slope)>5 ):
                    if abs(y-int(shape.pos1[1]+slope*(x-shape.pos1[0]) ))<abs(slope)*3 :
                        return True
                #下面==右邊 *上斜率基本上不會式整數 = =，找很久...
                elif(int(shape.pos1[1]+slope*(x-shape.pos1[0]))-2<=y <= int(shape.pos1[1]+slope*(x-shape.pos1[0]))+2  ):
                    
                    return True
       
        return False;  
    
    if(type(shape)==Triangle ):
        #!!!判斷點是否在三角形內的公式
        a = shape.pos1
        b = shape.pos2
        c = shape.pos3
        m = [x,y]
        ma=[m[0]-a[0],m[1]-a[1]]
        mb=[m[0]-b[0],m[1]-b[1]]
        mc=[m[0]-c[0],m[1]-c[1]]
        
        ans1 = ma[0]*mb[1]-ma[1]*mb[0]
        ans2 = mb[0]*mc[1]-mb[1]*mc[0]
        ans3 = mc[0]*ma[1]-mc[1]*ma[0]

        if ( (ans1>0 and ans2>0 and ans3>0) or (ans1<0 and ans2<0 and ans3<0) ):
            return True;          
        return False;  

#-------------------------------------------------------------------------
# 函數:初始遊戲.
#-------------------------------------------------------------------------
def resetGame():
    #呼叫全域變數
    global bricks_list,lines_list,circles_list,triangles_list,color_type,shapes_list,copy_list
    global brick_num,m,d,click,line_num,circle_num,triangle_num,x,y
    global tool,i,i1,i2,i3,i4,copy_mode,music_color,background
    
    sound_background.stop()
    
    # 清空^^
    bricks_list.clear()
    lines_list.clear()
    circles_list.clear() 
    triangles_list.clear() 
    shapes_list.clear()
    copy_list.clear()

    color_type = "random"
    tool = "brick"
    # 磚塊數量.
    brick_num = 0  
    m = 0
    d = 0
    click = 0
    i=0 
    i1=0
    i2=0
    i3=0
    i4=0 
    line_num = 0
    circle_num = 0
    triangle_num = 0
    background = (245,245,245) 

    x =100
    y =100
    copy_mode=0
    music_color = deep_pink
   

# 初始.
pygame.init()
pygame.mixer.init()
#音效
sound_click = pygame.mixer.Sound("music1.ogg")
sound_background = pygame.mixer.Sound("sound_background.ogg")
pygame.mixer.music.set_volume(1)
# 顯示Title.
pygame.display.set_caption(u"休閒小畫家")
# 建立畫佈大小.
canvas = pygame.display.set_mode((canvas_width, canvas_height))
# 時脈.
clock = pygame.time.Clock()
 
# 設定字型-黑體.
font = pygame.font.SysFont('simhei', 28)

 
# 物件數目
brick_num = 0
line_num = 0
circle_num = 0
triangle_num = 0

x =100
y =100
music_color = deep_pink
# 初始遊戲.
resetGame()
 

#bricks_list.append (Box(pygame, canvas, "brick_0", [  500,400, 58, 58], [255,255,255]))
     


#-------------------------------------------------------------------------    
# 主迴圈.
#-------------------------------------------------------------------------
running = True
while running:
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False
        # 判斷按下按鈕
        if event.type == pygame.KEYDOWN:
            # 判斷按下ESC按鈕
            if event.key == pygame.K_ESCAPE:
                running = False
                
        # 判斷Mouse.
        if event.type == pygame.MOUSEMOTION:
            move_x = pygame.mouse.get_pos()[0] 
            move_y = pygame.mouse.get_pos()[1] 
            if((m!=0) and move_x<145):
                m=0
                shapes_list.clear()
                copy_list.clear()
                copy_mode = 0
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            x=pygame.mouse.get_pos()[0]
            y=pygame.mouse.get_pos()[1]
                       
            if(x<145):
                draw = 0
                
                    #red條        
                if x>4 and x<19 and y>220 and y<475:
                    color_r = 475-y
                    #green條        
                if x>22 and x<37 and y>220 and y<475:
                    color_g = 475-y
                    #blue條        
                if x>40 and x<55 and y>220 and y<475:
                    color_b = 475-y
                    
                #圖標檢測  
                if x>5 and x<50 and y>500 and y<545:
                    tool = "circle"  
                    sound_click.play()
                if x>5 and x<50 and y>600 and y<645:
                    tool = "brick"  
                    sound_click.play()
                if x>5 and x<50 and y>550 and y<595:
                    tool = "triangle" 
                    sound_click.play()
                if x>60 and x<105 and y>650 and y<695:
                    tool = "hand"  
                    sound_click.play()
                if x>5 and x<50 and y>650 and y<695:
                    tool = "line"  
                    sound_click.play()
                if x>60 and x<105 and y>600 and y<645:
                    tool = "cut"  
                    sound_click.play()
                if x>60 and x<105 and y>550 and y<595:
                    tool = "copy"  
                    sound_click.play()
                if x>60 and x<105 and y>500 and y<545:
                    tool = "paint"  
                    sound_click.play()
                if x>60 and x<105 and y>430 and y<475:
                    tool = "camara"
                    sound_click.play()
                if x>60 and x<105 and y>380 and y<425:
                    tool = "background"
                    sound_click.play()
                if x>60 and x<105 and y>330 and y<375:
                    tool = "music"
                    sound_click.play()
                    
                if(tool=="camara"):
                    times = times+1
                    pygame.image.save(canvas,"camara"+str(times)+".png" )
                    
                    #重新遊戲
                if x<130 and y>canvas_height-50:
                    resetGame()
                    continue
            else:
            
                
                #觸碰改動文字
                if(x>404 and x<481 and y<26):
                    
                    
                    if(color_type =="random"):
                        color_type = "choose"
                    else:
                        color_type = "random"
                        
                else:
                    draw = 1
                    
            
            
            
            click = 1
 
    #--------------------------------------------------------------------- 

    
    #滑動感應變色
    if(move_x>130 or move_y<canvas_height-50):
        Reset_botton  = True
    else:
        Reset_botton  = False
        
    if(move_x<404 or move_x>481 or move_y>26 ):
        color_choose  = True
    else:
        color_choose  = False
       
    #----------------------------------------------------------
    # 清除畫面.
    canvas.fill(background)
    if(m==0):
        r,g,b =  randRGB(150,250)
    if(color_type=="choose"):
        r,g,b = color_r,color_g,color_b
    
    if(draw==0):
        m=0
        if(tool=="background"):
            background = (color_r,color_g,color_b)
        elif(tool=="music"):
            if(click==1):
                click=0
                if(music_color == bright_green):
                    music_color = deep_pink
                    sound_background.stop() 
                elif(music_color == deep_pink):    
                    music_color = bright_green
                    sound_background.play() 
                
        
       
     
    if(draw==1 ):
        
        if(copy_mode==1): #線在式copy狀態
            copy_list.clear()
            if(type(copy_object)==Box):
                ww=round(copy_object.rect[2]/2)
                hh=round(copy_object.rect[3]/2)
                copy_list.append(Box(pygame, canvas,"brick_x",[move_x-ww,move_y-hh,copy_object.rect[2],copy_object.rect[3]],copy_object.color)) 
            
            if(type(copy_object)==Line):
                ww = round((copy_object.pos2[0]-copy_object.pos1[0])/2)
                hh = round((copy_object.pos2[1]-copy_object.pos1[1])/2)
                copy_list.append(Line(pygame, canvas,"line_x",(move_x-ww,move_y-hh),(move_x+ww,move_y+hh),copy_object.color)) 
                
            if(type(copy_object)==Circle):           
                copy_list.append(Circle(pygame, canvas,"circle_x",(move_x,move_y),copy_object.radius,copy_object.color)) 
                
            if(type(copy_object)==Triangle):
                p12 = (copy_object.pos2[0]-copy_object.pos1[0],copy_object.pos2[1]-copy_object.pos1[1])
                p13 = (copy_object.pos3[0]-copy_object.pos1[0],copy_object.pos3[1]-copy_object.pos1[1])
                p1m2 =(move_x+p12[0], move_y+p12[1])
                p1m3 =(move_x+p13[0], move_y+p13[1])
                
                copy_list.append(Triangle(pygame, canvas,"triangle_x",[move_x,move_y],p1m2,p1m3,copy_object.color)) 
        
        #下面是用來做繪畫過程中的動圖
        if(m==1): #繪畫中而且點一次了
            shapes_list.clear()
            if(tool=="brick"):
                
                if(move_x<x1):
                    x_little_m =move_x
                else:
                    x_little_m =x1
                if(move_y<y1):
                    y_little_m = move_y
                else:
                    y_little_m = y1
                shapes_list.append(Box(pygame, canvas,"brick_x",[x_little_m,y_little_m,abs(x1-move_x),abs(y1-move_y)],[r,g,b])) 
            
            if(tool=="line"):
                shapes_list.append(Line(pygame, canvas,"line_x",(x1,y1),(move_x,move_y),[r,g,b])) 
                
            if(tool=="circle"):
                radius = int (( (x1-move_x)**2+(y1-move_y)**2 )**0.5)
                shapes_list.append(Circle(pygame, canvas,"circle_x",(x1,y1),radius,[r,g,b])) 
            if(tool=="triangle"):
                shapes_list.append(Line(pygame, canvas,"line_x",(x1,y1),(move_x,move_y),[r,g,b])) 
                
        if(m==2):
            shapes_list.clear()
            if(tool=="triangle"):
                 shapes_list.append(Triangle(pygame, canvas,"triangle_x",(x1,y1),(x2,y2),(move_x,move_y),[r,g,b])) 
         
            
        if(tool == "cut"):
            m=0
            # range(0, len(num))[::-1] 這樣子可以倒著讀，就可以做到類似stack的動作!! 同一類型可以刪上層的圖，不同類型就沒辦法啦
            #而且要把原本的bricks 都改成bricks_list[bricks] 因為bricks變成數字的意思
            #下面四個回全月上面的形狀越容易被刪除
            
            #刪線
            for lines in range(0,len(lines_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, lines_list[lines])):
                        if(lines_list[lines].visivle==True):
                            lines_list[lines].visivle = False
                            line_num = line_num-1
                            click=0 
            #刪三角形
            for triangles in range(0,len(triangles_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, triangles_list[triangles])):
                        if(triangles_list[triangles].visivle==True):
                            triangles_list[triangles].visivle = False
                            triangle_num = triangle_num-1
                            click=0
            #刪圓
            for circles in range(0,len(circles_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, circles_list[circles])):
                        if(circles_list[circles].visivle==True):
                            circles_list[circles].visivle = False
                            circle_num = circle_num-1
                            click=0   
            
            #刪方塊
            for bricks in range(0,len(bricks_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, bricks_list[bricks])):
                        if(bricks_list[bricks].visivle==True):
                            bricks_list[bricks].visivle = False
                            brick_num = brick_num-1
                            click=0  #就是這裡確保了只會刪一個方塊               
                                                     
        if(tool == "paint"):
            
            m=0
            
            #改線色
            for lines in range(0,len(lines_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, lines_list[lines])): 
                        if(lines_list[lines].visivle==True):
                            click=0
                            lines_list[lines].color = r,g,b
                 
            #改三角形色
            for triangles in range(0,len(triangles_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, triangles_list[triangles])):
                        if(triangles_list[triangles].visivle==True):
                            click=0
                            triangles_list[triangles].color = r,g,b 
                        
            #改圓色
            for circles in range(0,len(circles_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, circles_list[circles])):                        
                        if(circles_list[circles].visivle==True):
                            click=0
                            circles_list[circles].color = r,g,b            
            #改方塊色
            for bricks in range(0,len(bricks_list) )[::-1]:
                if(click==1):
                    # 碰磚塊.
                    if(isCollision( x, y, bricks_list[bricks])):
                        if(bricks_list[bricks].visivle==True):
                            click=0
                            bricks_list[bricks].color = r,g,b                     
                                      
        
        
        if(tool == "copy" or tool=="hand"):
            #print("line:",len(lines_list),"  rti:",len(triangles_list),"  circle:",len(triangles_list),"  brick:",len(bricks_list))
            
            m=0
            if(copy_mode==0):
                
                for lines in range(0,len(lines_list) )[::-1]:
                    if(click==1):
                        
                        # 碰磚塊.
                        if(isCollision( x, y, lines_list[lines])): 
                            if(lines_list[lines].visivle==True):
                                click=0
                                copy_mode = 1
                                copy_object = lines_list[lines]
                                if tool=="hand":
                                    line_num = line_num-1
                                    lines_list[lines].visivle=False
    
                for triangles in range(0,len(triangles_list) )[::-1]:
                    if(click==1):
                        # 碰磚塊.
                        if(isCollision( x, y, triangles_list[triangles])):
                            if(triangles_list[triangles].visivle==True):
                                click=0
                                copy_mode = 1
                                copy_object = triangles_list[triangles]
                                if tool=="hand": 
                                    triangle_num = triangle_num-1
                                    
                                    triangles_list[triangles].visivle=False
                                                           
                for circles in range(0,len(circles_list) )[::-1]:
                    if(click==1):
                        # 碰磚塊.
                        if(isCollision( x, y, circles_list[circles])):
                            if(circles_list[circles].visivle==True):
                                click=0
                                copy_mode = 1
                                copy_object = circles_list[circles]
                                if tool=="hand":
                                    
                                    circle_num = circle_num-1
                                    circles_list[circles].visivle=False
                for bricks in range(0,len(bricks_list) )[::-1]:
                    if(click==1):
                        # 碰磚塊.
                        if(isCollision( x, y, bricks_list[bricks])):
                            if(bricks_list[bricks].visivle==True):
                                click=0
                                copy_mode = 1
                                copy_object = bricks_list[bricks]
                                if tool=="hand":
                                    brick_num = brick_num-1
                                    bricks_list[bricks].visivle=False
                            
                        
            if(copy_mode==1):
                if(click==1):
                    copy_mode=0
                    click = 0
                    if(type(copy_object)==Line):
                        i2=i2+1
                        lines_list.append(Line(pygame, canvas,"line_x",(move_x-ww,move_y-hh),(move_x+ww,move_y+hh),copy_object.color)) 
                        line_num = line_num+1
                    if(type(copy_object)==Triangle):
                        i3=i3+1
                        triangles_list.append(Triangle(pygame, canvas,"triangle_x",[move_x,move_y],p1m2,p1m3,copy_object.color))
                        triangle_num = triangle_num+1 
                    if(type(copy_object)==Circle):
                        i1=i1+1
                        circles_list.append(Circle(pygame, canvas,"circle_x",(move_x,move_y),copy_object.radius,copy_object.color))
                        circle_num = circle_num+1
                    if(type(copy_object)==Box):
                        i=i+1
                        bricks_list.append(Box(pygame, canvas,"brick_"+str(i),[x-ww,y-hh,copy_object.rect[2],copy_object.rect[3]],copy_object.color))
                        brick_num = brick_num+1
                    
                    
   
                    copy_list.clear()
                                
                        
                        
        else:copy_mode=0

            
                                           
                        
                        
                
          
        
        if(click==1):
            
            click=0     
            
            if(tool=="brick"):
                m=m+1
                if(m==1):
                    x1 = x
                    y1  =y
                
                if(m==2):   
                    shapes_list.clear()
                    if(x<x1):
                        x_little = x
                    else:
                        x_little = x1
                    if(y<y1):
                        y_little = y
                    else:
                        y_little = y1
                    
                    i=i+1
                    bricks_list.append(Box(pygame, canvas,"brick_"+str(i),[x_little,y_little,abs(x-x1),abs(y-y1)],[r,g,b])) 
                    brick_num = brick_num+1
                    m=0
                 
            if(tool=="circle"):
                m=m+1
                if(m==1):
                    x1 = x
                    y1  =y
                
                if(m==2):   
                    shapes_list.clear()
                    radius = int (( (x1-x)**2+(y1-y)**2 )**0.5)
                    
                    i1=i1+1
                    circles_list.append(Circle(pygame, canvas,"circle_"+str(i1),[x1,y1] ,radius, [r,g,b]))
                    circle_num = circle_num+1
                    m=0
                    
            if(tool=="line"):
                m=m+1
                if(m==1):
                    x1 = x
                    y1  =y
                
                if(m==2):   
                    shapes_list.clear()
                    i2=i2+1
                    lines_list.append(Line(pygame, canvas,"line_"+str(i2),[x1,y1],[x,y], [r,g,b]))
                    
                    line_num = line_num+1
                    m=0
            if(tool=="triangle"):
                m=m+1
                if(m==1):
                    x1 = x
                    y1  =y
                    
                if(m==2):
                    x2 = x
                    y2 = y
                
                if(m==3):   
                    shapes_list.clear()
                    i3=i3+1
                    triangles_list.append(Triangle(pygame, canvas,"triangle_"+str(i2),[x1,y1],[x2,y2],[x,y], [r,g,b]))
                    
                    triangle_num = triangle_num+1
                    m=0
                    
                    
                    
                    
                    
                    
    
        
    #-------------------------繪製圖案
    #下面的順序式塗層的優先順序，愈上面的玉底層
    
    for bricks in (bricks_list ):
        bricks.update()    
    for circles in (circles_list ):
        circles.update()    
    for triangles in (triangles_list ):
        triangles.update()
    for lines in (lines_list ):
        lines.update()
    for shapes in (shapes_list ):
        shapes.update()
    for copys in (copy_list ):
        copys.update()
        
  
    #顏色選擇框
    if(color_choose):
        ColorChoose_color = light_green 
    else:
        ColorChoose_color = bright_green
    pygame.draw.rect( canvas,ColorChoose_color , (404,2,77,24) )
        
        
    
    showFont( u"color_type:"+color_type,   300, 2)
    
    #顏色選擇條
    #pygame.draw.rect( canvas,(color_r,0,0) , (4,220,15,256) )
    for ii in range(256):
        pygame.draw.rect( canvas,(255-ii,0,0) , (4,220+ii,15,1) )#red
        pygame.draw.rect( canvas,(0,255-ii,0) , (22,220+ii,15,1) )#green
        pygame.draw.rect( canvas,(0,0,255-ii) , (40,220+ii,15,1) )#blue
        
    pygame.draw.rect( canvas,White , (4,475-color_r,15,3) )#red
    pygame.draw.rect( canvas,White, (22,475-color_g,15,3) )#green
    pygame.draw.rect( canvas,White , (40,475-color_b,15,3) )#blue
    pygame.draw.rect( canvas,(color_r,color_g,color_b) , (4,185,51,30) )#調色盤
        
    
    
    
    brick_color = light_green
    circle_color = light_green
    triangle_color = light_green
    line_color = light_green
    hand_color = light_green
    camara_color = light_green
    background_color = light_green
 
    cut_color = light_green
    paint_color = light_green
    copy_color = light_green
    if(tool=="brick"):
        brick_color = bright_green
    elif(tool=="circle"):
        circle_color = bright_green
    elif(tool=="triangle"):
        triangle_color = bright_green
    elif(tool=="line"):
        line_color = bright_green
    elif(tool=="hand"):
        hand_color = bright_green
    elif(tool=="camara"):
        camara_color = bright_green
    elif(tool=="background"):
        background_color = bright_green
    elif(tool=="cut"):
        cut_color = bright_green
    elif(tool=="paint"):
        paint_color = bright_green
    elif(tool=="copy"):
        copy_color = bright_green
    
        
    if(copy_mode==1):    #for copy mode!
        if(tool=="copy"):
            copy_color = deep_pink
        else:
            hand_color = deep_pink
    pygame.draw.rect( canvas,circle_color , (5,500,45,45) )
    pygame.draw.rect( canvas,brick_color , (5,600,45,45) )
    pygame.draw.rect( canvas,triangle_color , (5,550,45,45) )
    pygame.draw.rect( canvas,hand_color , (60,650,45,45) )
    pygame.draw.rect( canvas,line_color , (5,650,45,45) )
    pygame.draw.rect( canvas,cut_color , (60,600,45,45) )
    pygame.draw.rect( canvas,copy_color , (60,550,45,45) )
    pygame.draw.rect( canvas,paint_color , (60,500,45,45) )
    pygame.draw.rect( canvas,camara_color , (60,430,45,45) )
    pygame.draw.rect( canvas,background_color , (60,380,45,45) )
    pygame.draw.rect( canvas,music_color , (60,330,45,45) )
        
        
    
    
    
    
    
    #重新畫布   之後如果有找到按鈕的在改，線在這樣不太好@@
    if(Reset_botton):
        ResetCanvas_color = light_green
    else:
        ResetCanvas_color = bright_green
    pygame.draw.rect( canvas,ResetCanvas_color , ResetCanvas_block )
    showFont("ResetCanvas!",10,720) 
    
    #畫框
    pygame.draw.line( canvas,Black,(145,0),(145,canvas_height) )
    

    # 顯示提示文字
    showFont( u"rectangle:"+str(brick_num),   8, 38)
    showFont( u"circle:"+str(circle_num),   8, 56)
    showFont( u"line:"+str(line_num),   8, 74)
    showFont( u"triangle:"+str(triangle_num),   8, 92)
    
    showFont("point:"+str(m),8,20) 
    showFont( u"FPS:" + str("%.4f"%clock.get_fps()), 8, 2) 
    
    canvas.blit(brick_image.image, brick_image.rect)
    canvas.blit(hand_image.image, hand_image.rect)
    canvas.blit(circle_image.image, circle_image.rect)
    canvas.blit(triangle_image.image, triangle_image.rect)
    canvas.blit(line_image.image, line_image.rect)
    canvas.blit(cut_image.image, cut_image.rect)
    canvas.blit(copy_image.image, copy_image.rect)
    canvas.blit(paint_image.image, paint_image.rect)
    canvas.blit(camara_image.image, camara_image.rect)
    canvas.blit(background_image.image,background_image.rect)
    canvas.blit(music_image.image,music_image.rect)
   
    # 更新畫面.
    pygame.display.update()
    clock.tick(60)
    

 
# 離開遊戲.
pygame.quit()
quit()