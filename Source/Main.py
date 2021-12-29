import os
import googletrans
import pyocr
import sys
from tkinter import *
from tkinter import Entry, Frame, Tk, filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import pyocr.builders
import PIL.Image
from PIL import ImageTk
from tkinter import scrolledtext
import deepl
import tkinter.simpledialog as simpledialog
from googletrans import Translator

global img

# json読み込み
try:
    json_file = open(".\\path.json",'r')
    json_obj = json.load(json_file)    
    DeepL_Token = json_obj['api_key']['Deepl_Token']
except Exception:
    messagebox.showerror("Error","jsonが読み込めませんでした")
    sys.exit()
# pyocrツール読み込み
try:    
    tools = pyocr.get_available_tools()
    tool = tools[0]
except Exception:
    messagebox.showerror("ツールが見つかりませんでした")
    sys.exit()

#langs = tool.get_available_languages()

lang_list_deepl = ['JA:日本語','EN-US:英語','DE:ドイツ語','ES:スペイン語','FR:フランス語','IT:イタリア語','ZH:中国語']
lang_list_google = ['ja:日本語','en:英語','fr:フランス','de:ドイツ語','es:スペイン語','nl:オランダ語','sv:スウェーデン語','he:ヘブライ語']
pyocr_list = ['eng:英語','jpn:日本語','rus:ロシア語','kor:韓国語','hun:ハンガリー語','ita:イタリア語','chi_sim:簡体字(中国語)']
trans_list = ['1:DeepL','2:Google翻訳']

def translation():
    txt = Detection_Scrolled.get("1.0","end-1c")
    lang_deepl = str(combobox_text_deepl.get())
    target_language_deepl = lang_deepl[0:2]
    lang_gogle = str(combobox_text_google.get())
    target_language_google = lang_gogle[0:2]
    trans = str(combobox2_text.get())
    trans_genre = trans[0:1]
    if not txt or not lang_deepl or not lang_list_google:
        messagebox.showerror("Error","テキストボックス、または翻訳先の言語が設定されていません")
        exit_app()
    elif int(trans_genre) == 1:    #Deeplの場合
        if not lang_deepl:
            messagebox.showerror("Error","翻訳先の言語が設定されていません")
            exit_app()
        else:
            translator_deepl = deepl.Translator(DeepL_Token)
            if str(target_language_deepl) == "EN":
                target_language_deepl+="-US"
            usage = translator_deepl.get_usage() #文字制限か調べる
            if usage.character.limit_exceeded:
                messagebox.showerror("Error","Character limit exceeded.")
                sys.exit()
            else:
                # print(f"Character usage: {usage.character}")
                character_limit.set(f"Character usage: {usage.character}")
                result_text = translator_deepl.translate_text(txt,target_lang=target_language_deepl)  # 英語の場合 EN-US 日本語の場合 JA
                Translation_Scrolled.insert("1.0",result_text.text)
    elif int(trans_genre) == 2:     #Google翻訳の場合
        if not lang_gogle:
            messagebox.showerror("Error","翻訳先の言語が設定されていません")
            exit_app()
        else:
            try:
                translator_google = googletrans.Translator()
            except Exception:
                messagebox.showerror("Error","インスタンスが生成できませんでした")
                sys.exit()
            Translation_text = translator_google.translate(txt,dest=target_language_google)
            Translation_Scrolled.insert("1.0",Translation_text.text)
    else:
        messagebox.showerror("Error","コンボボックスが正しく設定されていません")
        exit_app()

def exit_app():
  ret = messagebox.askyesno('確認', 'ウィンドウを閉じますか？')
  if ret == True:
        sys.exit()

def Reference():
    typ = [('画像ファイル',"*.png;*.jpg;*.jpeg;*.gif;*.webp:*.ico;*.bmp")] 
    dir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    if not filepath:
        return
    else:
        entry_text.set(filepath)
        
def set_image():
    global img
    name = entry_text.get()
    img = PIL.Image.open(name)
    img = ImageTk.PhotoImage(img)
    images_on_canvas = canvas.create_image(0,0,anchor='nw',image=img,)

def image_resize():
    global img
    name = entry_text.get()
    if not name:
        messagebox.showerror("Error","pathが空白です")
        exit_app()
    else:
        inputdata = simpledialog.askstring("Input Box","1:xだけ,2:yだけ,3:通常リサイズ")
        img = PIL.Image.open(name)
        w = img.width
        h = img.height
        if int(inputdata) == 1:
            img = img.resize(( int(w * (500/w)),260))
            img = ImageTk.PhotoImage(img)
            images_on_canvas = canvas.create_image(0,0, image=img,anchor='nw')
        elif  int(inputdata) == 2:
            img = img.resize((500,int(h * (260/w)) ))
            img = ImageTk.PhotoImage(img)
            images_on_canvas = canvas.create_image(0,130-(h*(260/w)/2), image=img,anchor='nw')
        elif int(inputdata) == 3: 
            img = img.resize(( int(w * (500/w)), int(h * (260/w)) ))
            img = ImageTk.PhotoImage(img)
            images_on_canvas = canvas.create_image(0,130-(h*(260/w)/2), image=img,anchor='nw')
        else:
            img = ImageTk.PhotoImage(img)
            images_on_canvas = canvas.create_image(0,0,anchor='nw',image=img,)

def zoom():
    path = entry_text.get()
    if not path:
        messagebox.showerror("Error","pathが空白です")
        exit_app()
    else:
        imgs = PIL.Image.open(path)
        img_window = Toplevel(window)
        img_window.title("Images")
        img_window.geometry("500x500")
        can_frame = tk.Frame(img_window,bg="#19191a",width=500,height=500)
        can_frame.grid()
        canvas_image = tk.Canvas(can_frame,bg="#19191a",width=imgs.width,height=imgs.height)
        img = PIL.Image.open(path)
        canvas_img = ImageTk.PhotoImage(img)
        on_images = canvas_image.create_image(0,0,image=canvas_img,anchor='nw')
        canvas_image.grid()
        img_window.mainloop()

def String_Output():
    pyocr_lang =str(combobox_text_pyocr.get())
    recognition_lang =pyocr_lang[0:3]
    filepath = entry_text.get()
    if not filepath or not pyocr_lang:
        messagebox.showerror("Error","ファイルまたは認識先の言語が設定されていません")
        exit_app()
    else:
        if str(recognition_lang) == "chi":
            recognition_lang+="_sim"
        set_image()
        txt = tool.image_to_string(
            image = PIL.Image.open(filepath),
            lang=recognition_lang,
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        Detection_Scrolled.insert('1.0',txt)
      

# GUI部分
window =tk.Tk()
window.title("IMG-Translator")
window.geometry("800x755")
window.config(bg="#19191a")
window.attributes("-alpha",0.9)
window.resizable(width=False,height=False)
icon = ".\\Images\\Icon.ico"
window.iconbitmap(default=icon)
# フレームの設定
frame = tk.Frame(window,bg="#19191a",width=300,height=35)
frame.pack(anchor="e")
button_frame = tk.Frame(window,bg="#19191a",width=800,height=175)
button_frame.pack(anchor="e")
img_frame  = tk.Frame(window,bg="white",width=500,height=260)
img_frame.place(x=30,y=35)
frame4 = tk.Frame(window,bg="#19191a",width=800,height=90)
frame4.pack()

label_frame =  tk.Frame(window,bg="#19191a",width=300,height=25)
label_frame.pack()
scrolled_frame = tk.Frame(window,bg="#19191a",width=800,height=200)
scrolled_frame.pack()
frame5  = tk.Frame(window,bg="#19191a",width=800,height=150)
frame5.pack()

# 各種ウィジェットの作成
loadimage = tk.PhotoImage(file=".\\Images\\Reference.png")
roundedbutton = tk.Button(button_frame,image=loadimage,height=45,width=145,command=lambda:Reference())
roundedbutton["bg"] = "#19191a"
roundedbutton["border"] = "0"

loadimage1 = tk.PhotoImage(file=".\\Images\\execute.png")
button_execute = tk.Button(button_frame, image=loadimage1,height=45,width=145,command=lambda:String_Output())
button_execute["bg"] = "white"
button_execute["border"] = "0"

loadimage2 = tk.PhotoImage(file=".\\Images\\Translation.png")
button_translation = tk.Button(button_frame, image=loadimage2,height=45,width=145,command=lambda:translation())
button_translation["bg"] = "white"
button_translation["border"] = "0"

loadimage3 = tk.PhotoImage(file=".\\Images\\zoom.png")
button_zoom = tk.Button(window, image=loadimage3,height=45,width=145,command=lambda:zoom())
button_zoom["bg"] = "white"
button_zoom["border"] = "0"

loadimage4 = tk.PhotoImage(file=".\\Images\\resize.png")
button_resize = tk.Button(window, image=loadimage4,height=45,width=145,command=lambda:image_resize())
button_resize["bg"] = "white"
button_resize["border"] = "0"

combobox_text_pyocr = StringVar()
pyocr_combobox = ttk.Combobox(frame5,textvariable=combobox_text_pyocr,values=pyocr_list,background="#19191a",foreground="black")
combobox_text_deepl = StringVar()
lang_combobox = ttk.Combobox(frame5,textvariable=combobox_text_deepl,values=lang_list_deepl,background="#19191a",foreground="black")
combobox_text_google = StringVar()
lang_combobox_google = ttk.Combobox(frame5,textvariable=combobox_text_google,values=lang_list_google,background="#19191a",foreground="black")
combobox2_text = StringVar()
trans_combobox = ttk.Combobox(frame5,textvariable=combobox2_text,values=trans_list,background="#19191a",foreground="black")
entry_text = StringVar()
entry1=ttk.Entry(window,textvariable=entry_text,width=30)
character_limit = StringVar()
character_limit_entry = ttk.Entry(frame5,textvariable=character_limit,width=57)


Translation_Scrolled = scrolledtext.ScrolledText(
    scrolled_frame,
    height=8,
    width=25,
    font=("03スマートフォント",15),)
Detection_Scrolled= scrolledtext.ScrolledText(
    scrolled_frame,
    height=8,
    width=25,
    font=("03スマートフォント",15),)

label1 = ttk.Label(
    label_frame,
    text="検出(翻訳する)されたテキスト　　　　　　　　　　　翻訳したテキスト",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,10))
# ボタン用
label2 = ttk.Label(
    button_frame,
    text="     ",
    background="#19191a",
    foreground="#19191a",
    font=("03スマートフォントUI","15"),
    padding=(5,10))
label3 = ttk.Label(
    button_frame,
    text="　　 ",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,10))
label4 = ttk.Label(
    button_frame,
    text="　　 ",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,10))
label5 = ttk.Label(
    button_frame,
    text="     ",
    background="#19191a",
    foreground="#19191a",
    font=("03スマートフォントUI","15"),
    padding=(5,5))
label6 = ttk.Label(
    button_frame,
    text="　　 ",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,10))


label7 = ttk.Label(
    window,
    text="ファイルパス",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","14"),
    padding=(5,5))
label8 = ttk.Label(
    frame5,
    text="翻訳先の言語:DeepL",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","14"),
    padding=(4,4))
label9 = ttk.Label(
    frame5,
    text="翻訳先の言語:Google",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","14"),
    padding=(5,5))
label10 = ttk.Label(
    frame5,
    text="翻訳機の種類",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,5))

label11 = ttk.Label(
    frame5,
    text="検出先の言語",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","14"),
    padding=(4,4))
label12 = ttk.Label(
    frame5,
    text="利用可能文字数:DeepL",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","14"),
    padding=(4,4))

# ScrolledText用
label_Scrolled = ttk.Label(
    scrolled_frame,
    text="　",
    background="#19191a",
    foreground="white",
    font=("03スマートフォントUI","15"),
    padding=(5,10))

image_filepath = PIL.Image.open(".\\images\\original.png")
canvas = tk.Canvas(img_frame,bg="#19191a",width=500,height=260)
canvas.photo = ImageTk.PhotoImage(image_filepath)
images_on_canvas = canvas.create_image(0,0,anchor='nw', image=canvas.photo)



#ウィジェットの配置
label7.place(x=590,y=260)

button_zoom.place(x=50,y=295)
button_resize.place(x=220,y=295)

label1.grid(row=0,column=0)
canvas.pack()

entry1.place(x=530,y=305)

label2.grid(row=0,column=2)
roundedbutton.grid(row=0,column=0)
label3.grid(row=1,column=0)
label4.grid(row=2,column=2)
button_execute.grid(row=2,column=0)
label5.grid(row=3,column=0)
label6.grid(row=4,column=2)
button_translation.grid(row=4,column=0)

Detection_Scrolled.pack(ipadx=50,ipady=30,side=LEFT)
Translation_Scrolled.pack(ipadx=50,ipady=30,side=RIGHT)

label_Scrolled.pack()
lang_combobox.place(x=606,y=40)
label8.place(x=610,y=0)
trans_combobox.place(x=30,y=40)
label10.place(x=60,y=0)
lang_combobox_google.place(x=330,y=40)
label9.place(x=330,y=0)
pyocr_combobox.place(x=30,y=105)
label11.place(x=60,y=70)
character_limit_entry.place(x=330,y=105)
label12.place(x=450,y=70)

window.mainloop()