from datetime import *
from tkinter.ttk import *
from tkinter import *
import time
import json
from tkinter import messagebox
from PIL import ImageTk,Image

people = {}
peopleaddr = {}
dperson = {"Thane(W)":["Rakesh","rk12"],"Thane(E)":["Jagdish","j23"],"Kalyan(E)":["Punit","pn31"],"Kalyan(W)":["Parth","pt56"],
           "Dombivli(W)":["Kamal","kml21"], "Dombivli(E)":["Rajesh","rsh41"],"Badlapur(E)":["Dilip","dp23"], "Badlapur(W)":["Kalpesh","kp24"]}
ppd = {}
med = {"Medicine":{"Crocin":25,"Azee 500":20,"Combiflam":30,"Digene":10,"Diclogem":20,"Rantac":30,"O2":20,"Vitamin B":30},
      "Cream":{"Volini":20,"Soframycin":10,"Zole F":25},"Syrup":{"Meftal P":20,"Cyclopam":12,"Benadryl":20}}

try:
    with open("pl.json",'r') as f:
        people = json.load(f)
    with open("pladdr.json",'r') as a:
        peopleaddr = json.load(a)
    with open("delinfo.json",'r') as d:
        ppd = json.load(d)

        
except:
    print("File not found")


def Save():
    with open("pl.json",'w') as f:
        json.dump(people,f,indent=2)
    with open("pladdr.json",'w') as a:
        json.dump(peopleaddr,a,indent=2)
    with open("delinfo.json",'w') as d:
        json.dump(ppd,d,indent=2)

def curtime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return str(current_time)

def delper_gui(name):
    
    global per
    login.destroy()
    per = Tk()
    per.geometry("600x400+360+200")
    per.title("Welcome "+name)
    bg1 = Image.open("bgor.jpeg")
    bg1 = bg1.resize((600,400),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(bg1)
    lbg = Label(per,image =photo,highlightthickness = 0)
    lbg.photo = photo
    
    def address():
        l = litem.curselection()
        nt = litem.get(l)
        total = 0
        for i in ppd:
            if(i == nt):
                for j in range(len(ppd[i])):
                    total += ppd[i][j][2]
        s = peopleaddr[nt] + "\n  Total = "+ str(total)
        linfo.configure(text =s)

    def delv():
        l = litem.curselection()
        nt = litem.get(l)
        for i in ppd:
            if(i == nt):
                for j in range(len(ppd[i])):
                    ppd[i][j][1] = 1
        Save()
    
    def generate():
        nonlocal name
        
        litem.delete(0,END)
        f = 0
        for i in dperson:
            if(dperson[i][0] == name):
                city = i
                break
        for i in ppd:
            for j in range(len(ppd[i])):
                if(ppd[i][j][0] == city and ppd[i][j][1] == -1):
                    f = 1
                    litem.insert(END,i)
        if(f == 0):
            s = "No Delivery"
            linfo.configure(text =s)
    
    lname = Label(per,bg = "white",height = 1,width =20,text = "Name",fg = "darkblue")
    litem = Listbox(per,width = 25,height = 13,bg = "darkblue",fg = "lightblue")
    linfo = Label(per,bg = "darkblue",height = 5,width =25,fg = "lightblue")
    btngen = Button(per,text = "Generate",command = generate)
    btnaddr = Button(per,text = "Address",command = address)
    btndelivered = Button(per,text = "Delivered",command = delv)
    lbg.place(x = 0,y =0)
    lname.place(x = 50 , y= 100)
    litem.place(x = 70 ,y = 140 )
    linfo.place(x = 300,y = 230)
    btngen.place(x = 300,y = 90)
    btnaddr.place(x = 300, y =130)
    btndelivered.place(x = 300, y =170)
    

def delivery_gui(name,ch):
    global dper
    if(ch == 0):
        login.destroy()
    else:
        crt.destroy()
    dper = Tk()
    dper.geometry("600x400+360+200")
    dper.title("Welcome "+name)
    t = 0    
    
    def sub():
        nonlocal t
        nonlocal name
        lcat.place_forget()
        lpr.place_forget()
        lq.place_forget()
        combo1.place_forget()
        combo2.place_forget()
        btnsub.place_forget()
        btnadd.place_forget()
        btnorder.place_forget()
        eq.place_forget()
        #s = "Hello " + name
        #lname = Label(dper,text = s,bg ="darkblue",height =2,width = 45,font = ("bold"),justify = CENTER,fg = "lightblue")
        litem.configure(height = 12 , width = 25 )
        linfo = Label(dper,bg ="darkblue",fg="lightblue",height = 8,width = 20,font=(20))
        btnok.configure(command = dper.destroy)
        s = "    Total = " + str(t)
        litem.insert(END,s)
        #lname.place(x= 60,y =60)
        litem.place(x =60,y =120)
        linfo.place(x = 300,y= 200)
        btnok.place(x = 300 , y = 360)
        city = people[name][2]
        if(name not in ppd):
            ppd.update({name:[[city,-1,t]]})
        else:
            ppd[name].append([city,-1,t])
        if(curtime() <= "20:00:00"):
            s = "Your Order Will be \ndelivered today to \n" + peopleaddr[name] + " by\n" + dperson[city][0]
            linfo.configure(text = s)
        elif(curtime() <= "24:00:00"):
            s = "Your Order Will be \ndelivered tomorrow to \n" + peopleaddr[name] + " by\n" + str(dperson[city][0])
            linfo.configure(text = s)
        Save()
                
        
    def add():
        nonlocal t
        ch = combo1.get()
        pr = combo2.get()
        q = eq.get()
        val = med[ch][pr] * int(q)
        s = str(pr) + " x " + str(q) + " = " + str(val)
        litem.insert(END,s)
        t = t + int(val)
        combo2.set("")
        combo1.set("")
        eq.delete(0,len(eq.get()))

  
    def product():
        if(combo1.get() == "Medicine" ):
            combo2['values']= ("Crocin","Azee 500","Combiflam","Digene","Diclogem","Rantac","O2","Vitamin B")
        elif(combo1.get() == "Cream" ):
            combo2['values']= ("Volini","Soframycin","Zole F")
        elif(combo1.get() == "Syrup" ):
            combo2['values']= ("Meftal P","Cyclopam","Benadryl")

    def order():
        def back():
            lv.place_forget()
            btnback.place_forget()
            btnsub.place(x = 400 , y = 350)

        btnsub.place_forget()
        nonlocal name
        lv = Label(dper,bg = "lightblue" ,height =18,width = 64)
        lv.place(x = 40, y =40)
        btnback = Button(dper,text = "Back",command = back)
        btnback.place(x = 400,y = 312)
        f = 0
        t = 1
        s = ""
        for i in ppd:
            if(i == name):
                for j in range(len(ppd[i])):
                    f = 1
                    s = s + str(t)+". Name : " 
                    s = s + name + "\n Address :"+peopleaddr[name] + "," + ppd[i][j][0]
                    if(ppd[i][j][1] == -1):
                        s = s + "     Not Delivered\n\n"
                    else:
                        s = s + "     Delivered\n\n"
                    t+=1
        if(f == 0):
            s = "No Order"
        lv.configure(text = s)        
            
    bg1 = Image.open("bgor.jpeg")
    bg1 = bg1.resize((600,400),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(bg1)
    lbg = Label(dper,image =photo,highlightthickness = 0)
    lbg.photo = photo
    
    #lv1 = Label(dper,bg = "#2980B9",height =22,width = 72)
    #lv2 = Label(dper,bg = "#6DD5FA",height =20,width = 68)
    #lv3 = Label(dper,bg = "lightblue" ,height =18,width = 64)
    lcat = Label(dper,text= "Category",fg = "darkblue",bg = "white" ,height =3,width = 20,justify = RIGHT)
    lpr = Label(dper,text= "Product",fg = "darkblue",bg = "white" ,height =3,width = 20)
    lq = Label(dper,text= "Quantity",fg = "darkblue",bg = "white" ,height =3,width = 20)
    eq = Entry(dper,width = 20)
    btnok = Button(dper,text = "OK" , command = product)
    btnadd = Button(dper,text = "Add Item" , command = add)
    btnsub = Button(dper, text = "Submit" , command = sub)
    btnorder = Button(dper,text = "Your Order",command = order)
    combo1 = Combobox(dper)
    combo1['values']= ("Medicine","Cream","Syrup")
    combo2 = Combobox(dper)
    litem = Listbox(dper,width = 22,height = 10,bg = "darkblue",fg = "lightblue")
    #lv1.place(x = 10,y = 5)
    #lv2.place(x = 25, y =20)
    #lv3.place(x = 40, y =40)
    lbg.place(x =0 ,y =0)
    btnadd.place(x = 150,y = 270)    
    btnok.place(x = 200,y = 140)
    btnsub.place(x = 400 , y = 350)
    btnorder.place(x = 50 , y = 312)
    lcat.place(x = 40 , y = 90)
    lpr.place(x = 40 , y = 165)
    lq.place(x = 40 , y = 215)
    combo1.place(x = 155, y = 105)
    combo2.place(x = 155 , y = 180)
    eq.place(x = 155 , y = 230)
    litem.place(x = 350,y = 150 )
    
def login_gui():
    def loguser():
        f = 0
        delp = 0 
        name = euser.get()
        pwd = epwd.get()
        for i in dperson:
            if(dperson[i][0] == name):
                delp = 1
                if(dperson[i][1] == pwd):
                    messagebox.showinfo('LogIn', 'Logged In')
                    delper_gui(name)
                else:
                    messagebox.showerror('Error', 'Password is incorrect')
        if(delp == 0):
            for i in people:
                if(i == name):
                    f = 1
                    if(people[i][0] == pwd):
                        messagebox.showinfo('LogIn', 'Logged In')
                        delivery_gui(name,0)
                    else:
                        messagebox.showerror('Error', 'Password is incorrect')
            if(f == 0):
                messagebox.showerror('Error', 'Username not present')
                 
    global login
    login = Tk()
    login.geometry("600x400+360+200")
    login.title("login")
    bg1 = Image.open("bg.png")
    bg1 = bg1.resize((600,400),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(bg1)
    lbg = Label(login,image =photo,highlightthickness = 0)
    lbg.photo = photo
    
    bg2 = Image.open("lbtn.png")
    bg2 = bg2.resize((133,35),Image.ANTIALIAS)
    lb = ImageTk.PhotoImage(bg2)

    bg3 = Image.open("crbtn.png")
    bg3 = bg3.resize((230,25),Image.ANTIALIAS)
    crb = ImageTk.PhotoImage(bg3)
    
    euser = Entry(login,width = 30,highlightthickness=6,highlightbackground="black",border = 3)
    epwd = Entry(login,width =30,highlightthickness=6,highlightbackground="black",border = 3)
    btnslots = Button(login,image = lb,bg = "darkblue",fg = "lightblue",command =loguser)
    btnslots.photo = lb    
    btncreate = Button(login,image = crb,bg = "white",fg = "lightblue",command = create_gui,highlightthickness=0,border = 0)
    btncreate.photo = crb
   
    lbg.place(x = 0, y =0)

    euser.place(x = 203,y = 201)
    epwd.place(x = 203,y = 248)
    btnslots.place(x = 232,y = 306)
    btncreate.place(x = 310,y = 360)
    #login.mainloop()


def create_gui():
    def create():
        error = 0
        name = euser.get()
        pwd = epwd.get()
        ph = eph.get()
        addr = taddr.get("1.0",END)
        city = combo.get()
        if(len(ph) == 10):
            if(len(people) == 0):
                error = 0
                people.update({name:[pwd,ph,city]})
                peopleaddr.update({name:addr})
                messagebox.showinfo('Account', 'Created')
                delivery_gui(name,1)
            else:
                if(name not in people):
                    error = 0
                    people.update({name:[pwd,ph,city]})
                    peopleaddr.update({name:addr})
                    messagebox.showinfo('Account', 'Created')
                    delivery_gui(name,1)
                else:
                    if(people[name][0] == pwd):
                        error = 1
                        messagebox.showerror('Error', 'Username/Password present')
        else:
            error = 1
            messagebox.showerror('Error', 'Phone Number Should be Correct')
        if(error == 0):
            Save()
        
                
    global crt
    login.destroy()
    crt = Tk()
    crt.geometry("600x400+360+200")
    crt.title("Create")
    bg1 = Image.open("bgor.jpeg")
    bg1 = bg1.resize((600,400),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(bg1)
    lbg = Label(crt,image =photo,highlightthickness = 0)
    lbg.photo = photo
    luser = Label(crt,text= "Username",fg = "darkblue",bg = "white" ,height =2,width = 20)
    euser = Entry(crt)
    lpwd = Label(crt,text= "Password",fg = "darkblue",bg = "white" ,height =2,width = 20)
    epwd = Entry(crt)
    lph = Label(crt,text= "Phone Number",fg = "darkblue",bg = "white" ,height =2,width = 20)
    eph = Entry(crt)
    laddr = Label(crt,text= "Address",fg = "darkblue",bg = "white" ,height =2,width = 20)
    taddr = Text(crt,height = 3,width = 20)
    combo = Combobox(crt)
    combo['values']= ("Thane(E)","Thane(W)","Kalyan(E)","Kalyan(W)", "Dombivli(E)", "Dombivli(W)", "Badlapur(E)", "Badlapur(W)")
    #combo.current(5)
    larea = Label(crt,text= "City",fg = "darkblue",bg = "white" ,height =2,width = 18)
    btnslots = Button(crt,text = "Create",width =  15,command = create,bg = "lightblue",fg = "black",font = ("bold"),highlightthickness=3,highlightbackground="blue")
    lbg.place(x = 0,y =0)
    luser.place(x = 100, y =100)
    lpwd.place(x = 100, y =150)
    lph.place(x = 100 , y = 200)
    laddr.place(x = 100 , y =250)
    larea.place(x = 100 , y = 310)
    euser.place(x = 250,y = 105)
    epwd.place(x = 250,y = 155)
    eph.place(x = 250,y = 205)
    taddr.place(x = 250,y = 255)
    combo.place(x = 250,y = 330)
    btnslots.place(x = 200,y = 360)
    #crt.mainloop()


Save()  
login_gui()
login.mainloop()
