import tkinter
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

marK = ()
dicT = {}
chapterList = []
urL = "https://8book.com/"
optioN=webdriver.ChromeOptions()
optioN.add_argument('--headless')
wwW=webdriver.Chrome(options  = optioN)


#------------------------------設定按鈕功能
#查詢
def _find():
    global marK,dicT,chapterList
    if finDentrY.get() is not None:
        listboX.delete(0,tkinter.END)
        dicT = {}
        chapterList = []
        try:        
            wwW.get(urL+"search/?key="+finDentrY.get())
            wwW.implicitly_wait(15)
            contenT = wwW.find_elements(By.CLASS_NAME,"col-12.col-sm-12.col-md-6.col-lg-4.p-2")

            for coN in contenT:
                #將Webelement轉為html 找href 
                soup = BeautifulSoup(coN.get_attribute('innerHTML'),"html5lib")
                hreF = soup.find("a",href = True)["href"]
                
                #找小說名稱，並與href加入字典
                finDtitlEp = coN.find_elements(By.CLASS_NAME,"nowraphide")
                authoR = finDtitlEp[0].text
                finDtitlE = finDtitlEp[2].text.replace("\n", "--")
                dicT[finDtitlE] = hreF
                
                #寫入listbox
                listboX.insert(tkinter.END,finDtitlE)
                listboX.insert(tkinter.END,authoR )
                listboX.insert(tkinter.END, '-'*80)
            marK = "find"
        except:
            return
    else:
        tkinter.messagebox.showinfo("提示","請輸入要查詢的小說")

#雙擊開啟小說目錄/章節
def _Double_click(event):
    global marK,dicT,chapterList,currenT
    chapterList = []
    if marK == "find":
        try:
            object = event.widget
            indeX = object.curselection()
            wwW.get(urL+dicT[listboX.get(indeX)])
            wwW.implicitly_wait(15)
            contenT = wwW.find_elements(By.CLASS_NAME,"col-6.col-md-4.col-lg-3.py-2")
            listboX.delete(0,tkinter.END)
            dicT = {}
            for coN in contenT:
                #將Webelement轉為html 找href 
                soup = BeautifulSoup(coN.get_attribute('innerHTML'),"html5lib")
                hreF = soup.find("a",href = True)["href"]
                
                #找章節名稱，並與href加入字典
                finDtitlE = coN.find_element(By.CLASS_NAME,"episode_li.d-block").text
                dicT[finDtitlE] = hreF
                
                #寫入listbox
                listboX.insert(tkinter.END,finDtitlE)
                listboX.insert(tkinter.END, '-'*80)
            marK = "novel"
        except:
            tkinter.messagebox.showinfo("提示","請點擊小說名稱")
            
            

    elif marK == "novel":
        try:
            object = event.widget
            indeX = object.curselection()
            currenT = dicT[listboX.get(indeX)]
            wwW.get(urL+currenT)
            wwW.implicitly_wait(15)
            _reaD()
        except:
            tkinter.messagebox.showinfo("提示","請點擊小說名稱")

            
    lisT = list(dicT.values())
    for lE in range(len(lisT)):
        chapterList.append(lisT[lE])


#小說頁面       
def _reaD():
    global marK
    try:
        contenT = wwW.find_elements(By.CLASS_NAME,"text")
        contenTx = contenT[0].text.split("\n")
        listboX.delete(0,tkinter.END)
    except:
        tkinter.messagebox.showinfo("提示","載入失敗")
    try:
        for coN in contenTx:
            if len(coN)>55:
                for cN in range(math.ceil(len(coN)/55)):
                    straT = cN*55
                    enD = (int(cN)+1)*55                
                    listboX.insert(tkinter.END,coN[int(straT):int(enD)])     
            else:
                listboX.insert(tkinter.END,coN)           
    except:
        tkinter.messagebox.showinfo("提示","讀取失敗")
        marK = "read"


#上一章
def _last_chapter():
    global currenT
    if marK == "read":
        if chapterList.index(currenT)>0:
            wwW.get(urL+chapterList[chapterList.index(currenT)-1])
            wwW.implicitly_wait(15)
            _reaD()
        else:
            tkinter.messagebox.showinfo("提示","沒有上一章")
    else:
        tkinter.messagebox.showinfo("提示","這邊沒有上一章")

#上一頁
def _last_page():
    return

#下一頁
def _next_page():
    return

#下一章
def _next_chapter():
    global currenT
    if marK == "read":
        if chapterList.index(currenT)==len(chapterList)-1:
            tkinter.messagebox.showinfo("提示","沒有下一章")
        else:
            wwW.get(urL+chapterList[chapterList.index(currenT)+1])
            wwW.implicitly_wait(15)
            _reaD()
    else:
        tkinter.messagebox.showinfo("提示","這邊沒有下一章")

#離開
def _quiT():
    qQ=tkinter.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()


#------------------------------主畫面
wiN = tkinter.Tk()
wiN.title("8book!!!")
wiN.geometry("800x450")


#------------------------------框架排版
lisTframE = tkinter.LabelFrame(wiN, background='#09c')
lisTframE.pack(fill='both',side='left', expand=1)

besidEframE = tkinter.Frame(wiN)
besidEframE.pack(fill='y',side='right')

enteYframE = tkinter.Frame(besidEframE)
enteYframE.pack()
bottoMframE = tkinter.Frame(besidEframE)
bottoMframE.pack(fill='y')


#------------------------------表單框
sBarY=tkinter.Scrollbar(lisTframE, orient='vertical')
sBarY.pack(side="right",fill="y")

sBarX=tkinter.Scrollbar(lisTframE, orient='horizontal')
sBarX.pack(side="bottom",fill="x")

listboX = tkinter.Listbox(lisTframE,font=("Helvetica",20), xscrollcommand=sBarX.set, yscrollcommand=sBarY.set) 
listboX.pack(fill='both', expand=1)

listboX.insert(tkinter.END, '歡迎!!!請輸入想要查詢的小說名稱。')
listboX.bind("<Double-Button-1>", _Double_click)

sBarY.config(command=listboX.yview)
sBarX.config(command=listboX.xview)


#------------------------------輸入框
finDlabeL = tkinter.Label(enteYframE,text='小說名稱：', font=("Arial", 10), background='#0c9')
finDlabeL.grid(column=0, row=0)

finDentrY=tkinter.Entry(enteYframE,font=("Arial",10),bd=5)
finDentrY.grid(column=1, row=0)

finDbottoM = tkinter.Button(enteYframE, text="查詢", font=("Arial", 10), width=4, height=1, background='#0c9', command=_find)
finDbottoM.grid(column=2, row=0)


#------------------------------按鈕框
#留天
toPframE = tkinter.Frame(bottoMframE)
toPframE.grid(column=0, row=0,ipady=20)

#上框
lasTframE = tkinter.Frame(bottoMframE)
lasTframE.grid(column=0, row=1,ipady=20)
#上一章
lastchapteRbuttoN = tkinter.Button(lasTframE, text="上一章", font=("Arial", 12), width=10, height=1, background='#0c9', command=_last_chapter)
lastchapteRbuttoN.pack()
#上一頁
lastpagEbuttoN = tkinter.Button(lasTframE, text="上一頁", font=("Arial", 12), width=10, height=1, background='#0c9', command=_last_page)
lastpagEbuttoN.pack()

#標籤
labeLframE = tkinter.Frame(bottoMframE)
labeLframE.grid(column=0, row=2,ipady=20)
#章節與頁數
chapteRlabeL = tkinter.Label(labeLframE,text='章節', font=("Arial", 14), background='#0c9')
chapteRlabeL.pack()
pagElabeL = tkinter.Label(labeLframE,text='頁數', font=("Arial", 20), background='#0c9')
pagElabeL.pack()

#下框
nexTframE = tkinter.Frame(bottoMframE)
nexTframE.grid(column=0, row=3,ipady=20)
#下一頁
nextpagEbuttoN = tkinter.Button(nexTframE, text="下一頁", font=("Arial", 12), width=10, height=1, background='#0c9', command=_next_page)
nextpagEbuttoN.pack()
#下一章
nextchapteRbuttoN = tkinter.Button(nexTframE, text="下一章", font=("Arial", 12), width=10, height=1, background='#0c9', command=_next_chapter)
nextchapteRbuttoN.pack()

#離開
quiT = tkinter.Button(bottoMframE, text="關閉程式", font=("Arial", 12), width=10, height=1,activebackground='#f00', command=_quiT)
quiT.grid(column=0, row=4)

 
#------------------------------主畫面迴圈
wiN.mainloop()