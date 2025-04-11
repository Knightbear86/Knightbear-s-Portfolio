#pip install tkinter
#pip install pandas
import tkinter
from tkinter import ttk
import pandas


#########################----def Main bottom

def _treeview():
    global dF,columList
    
    treevieW.delete(*treevieW.get_children())

    _optionUpdate()

    treevieW["column"] = list(dF.columns)
    treevieW["show"] = "headings"
    for column in treevieW["column"]:
        treevieW.heading(column, text = column)
        
    df_rows = dF.to_numpy().tolist()
    for row in df_rows:
        treevieW.insert("","end",value = row)
    return None

def _optionUpdate():
    global columNmenu,columList,columNvalue
    
    columNmenu["menu"].delete(0,"end")
    columList = list(dF.columns)
    for col in columList:
        columNmenu["menu"].add_command(label = col, command = lambda x=col: columNvalue.set(x))

def _loaD():
    global dF
    try:
        
        try:
            dF = pandas.read_csv(enteRurl.get())
        except:
            dF = pandas.read_json(enteRurl.get())
    
    except:
        tkinter.messagebox.showerror("格式錯誤","無法開啟檔案")
        return None
    _treeview()
    
def _savE():
    global dF
    dF.to_csv(enteRsave.get()+".csv", encoding = 'utf-8',index = False)
    
def _quiT():
    qQ=tkinter.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()

#########################-----def List bottom

def _dropna():
    global dF

    dF.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
    dF.dropna(axis=1, how='all', thresh=None, subset=None, inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","已刪除空欄列")
    
def _median():
    global dF,columNvalue
    
    dF[columNvalue.get()].fillna(value = dF[columNvalue.get()].median(), inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","已將"+columNvalue.get()+"中的空值換成中位數")
    
def _mean():
    
    global dF
    dF[columNvalue.get()].fillna(value = dF[columNvalue.get()].mean(), inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","已將"+columNvalue.get()+"中的空值換成平均數")
    
def _droPcol():
    
    global dF
    dF.drop(columns = columNvalue.get(), inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","已將"+columNvalue.get()+"刪除")
    
def _droPind():
    
    global dF
    droPind = str(treevieW.focus()).lstrip('I')
    dF.drop(index = int(droPind), inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","已將此列刪除")

def _duplicated():
    
    global dF
    dF.drop_duplicates(inplace=True)
    _treeview()
    tkinter.messagebox.showinfo("提示","檔案已無重複值")
    
#########################-----Window set

wiN = tkinter.Tk()
wiN.title("Welcome!!!")
wiN.geometry("800x450")
#wiN.resizable(0,0)

#########################-----排版

enteYframE = tkinter.Frame(wiN)
enteYframE.pack()
bottoMframE = tkinter.Frame(wiN)
bottoMframE.pack()

lisTframE = tkinter.LabelFrame(wiN, text='表單')
lisTframE.pack(fill='both', expand=1)


treevieWframE = tkinter.Frame(lisTframE)
treevieWframE.pack(side='left', fill='both', expand=1)
bottoMframEL = tkinter.Frame(lisTframE)
bottoMframEL.pack(side='left')

#########################-----Entry

labeLurl = tkinter.Label(enteYframE,text='開啟檔案：', font=("Arial", 14), background='#0c9')
labeLurl.grid(column=0, row=0)

labeLsave = tkinter.Label(enteYframE,text='存檔名稱：', font=("Arial", 14), background='#0c9')
labeLsave.grid(column=0, row=1)

enteRurl=tkinter.Entry(enteYframE,font=("Arial",14),bd=5)
enteRurl.grid(column=1, row=0)

enteRsave=tkinter.Entry(enteYframE,font=("Arial",14),bd=5)
enteRsave.grid(column=1, row=1)

#########################-----Main bottom

loaD = tkinter.Button(bottoMframE, text="載入", font=("Arial", 12), width=6, height=1, background='#0c9', command=_loaD)
loaD.pack(side='left')

savE = tkinter.Button(bottoMframE, text="存檔", font=("Arial", 12), width=6, height=1, command=_savE)
savE.pack(side='left')

quiT = tkinter.Button(bottoMframE, text="關閉程式", font=("Arial", 12), width=10, height=1,activebackground='#f00', command=_quiT)
quiT.pack(side='left')

#########################-----Treeview

sBarY=tkinter.Scrollbar(treevieWframE, orient='vertical')
sBarY.pack(side="right",fill="y")

sBarX=tkinter.Scrollbar(treevieWframE, orient='horizontal')
sBarX.pack(side="bottom",fill="x")

treevieW=ttk.Treeview(treevieWframE, xscrollcommand=sBarX.set, yscrollcommand=sBarY.set)
treevieW.pack(fill='both', expand=1)

sBarY.config(command=treevieW.yview)
sBarX.config(command=treevieW.xview)

#########################-----List bottom


columList = ['']

columNvalue = tkinter.StringVar()                                        # 取值
columNvalue.set(columList[0])

columNmenu = tkinter.OptionMenu(bottoMframEL, columNvalue, *columList)                # 第二個參數是取值，第三個開始是選項，使用星號展開
columNmenu.pack()


dropnA = tkinter.Button(bottoMframEL, text="刪除空欄列", font=("Arial", 12), width=10, height=1, background='#0c9', command=_dropna)
dropnA.pack()
mediaN = tkinter.Button(bottoMframEL, text="中位數填空", font=("Arial", 12), width=10, height=1, command=_median)
mediaN.pack()
meaN = tkinter.Button(bottoMframEL, text="平均數填空", font=("Arial", 12), width=10, height=1, command=_mean)
meaN.pack()
droPcol = tkinter.Button(bottoMframEL, text="刪除欄", font=("Arial", 12), width=10, height=1, command=_droPcol)
droPcol.pack()
droPind = tkinter.Button(bottoMframEL, text="刪除列", font=("Arial", 12), width=10, height=1, command=_droPind)
droPind.pack()
duplicateD = tkinter.Button(bottoMframEL, text="刪除重複值", font=("Arial", 12), width=10, height=1, command=_duplicated)
duplicateD.pack()

#########################

wiN.mainloop()






