import tkinter as tk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import csv
import math
import os

##########################################################

# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1<50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return 'good'
    elif f1>=50 and f2>=50 and f3<50 and f4>=50 and f5>=50:
        return 'no!!!'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5<50:
        return 'ROCK!'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return 'pink'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '2'
    elif f1>=50 and f2>=50 and f3<50 and f4<50 and f5<50:
        return 'ok'
    elif f1<50 and f2>=50 and f3<50 and f4<50 and f5<50:
        return 'ok'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        return '9'
    else:
        return ''

##########################################################

def _quiT():
    qQ=tk.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        cap.release()
        cv2.destroyAllWindows()
        wiN.destroy()

##########################################################

def _geT():
    global sampleName,handposeName,sampleCsv

    if sampleName == None and handposeName == None:
       tk.messagebox.showinfo("回報","尚未輸入樣本及手勢名稱!") 

    else:
        
        if not sampleGet == []:

            if os.path.isfile(sampleName+".csv"):              
                csvFile=open(sampleName+".csv","a",newline="",encoding="utf-8-sig")
                writeR=csv.writer(csvFile)
                
                writeR.writerow(sampleGet)
                csvFile.close()
                
                tk.messagebox.showinfo("回報","舊檔案已添加點位!")
            else:
                sampleCsv=[]
                csvFile=open(sampleName+".csv","w",newline="",encoding="utf-8-sig")
                writeR=csv.writer(csvFile)
                writeR.writerow(["handpose",
                                 "wrist",
                                 "thump_cmc","thump_mcp","thump_ip","thump_tip",
                                 "index_mcp","index_pip","index_dip","index_tip",
                                 "middle_mcp","middle_pip","middle_dip","middle_tip",
                                 "pink_mcp","pink_pip","pink_dip","pink_tip"
                                 ])
                
                writeR.writerow(sampleGet)
                csvFile.close()
                
                tk.messagebox.showinfo("回報","已建立新檔案!")
        else:
            tk.messagebox.showinfo("回報","未取得手部模型!")

##########################################################

#def _marK():
    #try:
        #tk.messagebox.showinfo("回報","!")
    #except:
        #tk.messagebox.showinfo("回報","....")

def _posE():
    global enteRsample,enteRpose,sampleName,handposeName
    
    try:
        sampleName = enteRsample.get()
        handposeName = enteRpose.get()
        tk.messagebox.showinfo("回報","已設定手勢名稱及輸入檔案!")
    except:
        tk.messagebox.showinfo("回報","未設定手勢名稱及輸入檔案!")

##########################################################

def _posEcu():
    if finger_points_for_angle:
        
        # 計算手指角度，回傳長度為 5 的串列
        finger_angle = hand_angle(finger_points_for_angle) 
        
        #將listbox清乾淨
        listBox.delete(0,tk.END)
        
        # 印出角度
        listBox.insert(tk.END, finger_angle) 
        
        # 取得手勢所回傳的內容
        text = hand_pos(finger_angle)            
        listBox.insert(tk.END, text)
        
    else:
        #將listbox清乾淨
        listBox.delete(0,tk.END)
        listBox.insert(tk.END, "當前無手勢")
        
##########################################################

mp_hands = mp.solutions.hands

########################################################## 讀取攝影機

cap = cv2.VideoCapture(0) 

########################################################## 主視窗

wiN = tk.Tk()
wiN.title('Get hand_landmarks sample!!!')
wiN.geometry('800x600')

########################################################## 分割位置
   
labelframE = tk.LabelFrame(wiN,bg="blue")
labelframE.pack()
enteYframE = tk.Frame(wiN,width=600)
enteYframE.pack()
bottoMframE = tk.Frame(wiN,bg="red")
bottoMframE.pack()

########################################################## 鏡頭位置

labeLcap = tk.Label(labelframE) 
labeLcap.pack()

########################################################## 輸入位置


labeLsample = tk.Label(enteYframE,text='樣本檔案', font=("Arial", 10), background='#0c9')
labeLsample.grid(column=0, row=0)
labeLpose = tk.Label(enteYframE,text='手勢名稱', font=("Arial", 10), background='#0c9')
labeLpose.grid(column=0, row=1)

enteRsample=tk.Entry(enteYframE,font=("Arial",16),bd=5)
enteRsample.grid(column=1, row=0, columnspan=3)
enteRpose=tk.Entry(enteYframE,font=("Arial",16),bd=5)
enteRpose.grid(column=1, row=1, columnspan=3)

sampleName = None
handposeName = None

########################################################## 按鍵設定

posE = tk.Button(bottoMframE, text="存入的檔案位置及手勢名稱", font=("Arial", 12), width=25, height=2, background='#0c9', command=_posE)
posE.pack(side='left')
geT = tk.Button(bottoMframE, text="取得點位", font=("Arial", 12), width=10, height=2, command=_geT)
geT.pack(side='left')
#marK = tk.Button(bottoMframE, text="開啟點位", font=("Arial", 12), width=10, height=2, command=_marK)
#marK.pack(side='left')
posEcu = tk.Button(bottoMframE, text="當前手勢名稱", font=("Arial", 12), width=15, height=2, command=_posEcu)
posEcu.pack(side='left')
quiT = tk.Button(bottoMframE, text="關閉程式", font=("Arial", 12), width=10, height=2,activebackground='#f00', command=_quiT)
quiT.pack(side='left')

########################################################## 檢視畫面

framE = tk.Frame(wiN)
framE.pack()

sBar=tk.Scrollbar(framE, orient='horizontal')
sBar.pack(side="bottom",fill="x")

listBox=tk.Listbox(framE,height=100,width=300, font=("Arial", 20),xscrollcommand=sBar.set)
listBox.pack(side="bottom", fill="both")
sBar.config(command=listBox.xview)

########################################################## mediapipe 啟用偵測手掌

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    if not cap.isOpened():
        listBox.insert(tk.END, "Cannot open camera")
        exit()
    w, h = 540, 310
    while True:
        if not wiN:
            break
        ret, img = cap.read()
        img = cv2.resize(img, (w,h))                 
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img3 = Image.fromarray(img2)
        tk_img = ImageTk.PhotoImage(image=img3)
        labeLcap.photo_image = tk_img
        labeLcap.configure(image=tk_img)
        wiN.update()
        #while用update更新圖片﹐以達到動態
        #使用函式的話用 label.after(ms_毫秒,函式)代表幾毫秒再呼叫一次函式，已達到動態
            
        results = hands.process(img2)                # 偵測手勢
        if results.multi_hand_landmarks:
            sampleGet = []
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points_for_angle = []                   # 記錄手指節點座標的串列
                finger_points = []
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    xA = i.x*w
                    yA = i.y*h
                    x = i.x
                    y = i.y
                    z = i.z
                    finger_points.append([x,y,z])
                    finger_points_for_angle.append((xA,yA))
                sampleGet.append([handposeName])
                for k in range(len(finger_points)):
                    sampleGet.append([finger_points[k]])
        else:
            sampleGet = []
            finger_points_for_angle = []
            finger_points = []
                
##########################################################          

wiN.mainloop()
cap.release()
cv2.destroyAllWindows()

