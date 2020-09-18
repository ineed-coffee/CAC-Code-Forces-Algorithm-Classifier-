from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tf
import mysql.connector as mc
from mysql.connector import Error as mce
import webbrowser as wb
import os

conn = mc.connect(user='your role name',password='your password',host='127.0.0.1',database='CAC_db')
cur=conn.cursor()
cur.execute('show columns from CAC_db.prob_set')
cols = cur.fetchall()
tags = str(cols[-1][1]).replace("'","")
tags = tags[6:-2].split(",")

def tag_selected(event):
    new_tag = combo1.get()
    cur.execute(f"select name,difficulty,id from CAC_db.Prob_set where find_in_set('{new_tag}',tags) order by difficulty")
    new_value = cur.fetchall()
    combo2.config(values=[*map(lambda x: x[0]+'  |  '+str(x[1])+'  |  ('+x[2]+')',new_value)])
    combo2.current(0)

def go_solve():
    s=combo2.get()
    url_key = s.split('|')[-1]
    url_key = url_key.replace(' ','')
    url_key=url_key[1:-1]
    url=f"https://codeforces.com/problemset/problem/{url_key}"
    wb.open(url)

master = Tk()
master.title('Algorithm sorted by tags')
master.geometry('500x500+700+200')
top_frame = Frame(master,background="turquoise",relief=RIDGE,borderwidth=5);top_frame.pack(side=TOP,fill=BOTH,ipadx=30,ipady=20)
font_set = tf.Font(family="Arial", size=16, weight="bold", slant="roman")
text1 = Label(top_frame,text='Select specific tag to see Problems.',bg='turquoise',font=font_set);text1.grid(row=0,column=0)
combo1 = ttk.Combobox(top_frame,values=tags,state='readonly',width=48,height=25);combo1.grid(row=1,column=0)
combo1.bind("<<ComboboxSelected>>", tag_selected)
mid_frame = Frame(master,background="spring green",relief=RIDGE,borderwidth=5);mid_frame.pack(side=TOP,fill=BOTH,ipadx=30,ipady=25)
text2 = Label(mid_frame,text="Press 'Go' to solve selected problem.",bg='spring green',font=font_set);text2.grid(row=0,column=0)
combo2 = ttk.Combobox(mid_frame,values=['','','',''],state='readonly',width=51,height=25);combo2.grid(row=1,column=0)
go_b = Button(mid_frame,text='Go!',bg='yellow',command=go_solve);go_b.grid(row=1,column=1)

base_folder = os.path.dirname(__file__)
image_path = os.path.join(base_folder, 'img','codeforces.gif')
img = PhotoImage(file=image_path)
bg_label = Label(master,image=img);bg_label.pack()

master.mainloop()
conn.close()