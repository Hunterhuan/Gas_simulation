import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import math
import numpy as np
import string
from random import randint, uniform
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import collision3D


demdata=[]# the demon energy of every steps
vdata=[]  #the velocity data of the particles in the final experiment(whose visual is True)
f2_type=1 # the type of fig2, 1 for histogram 0 for plot graph
#This is creating the main window
root=Tk()
#set the title of the window
root.title("Stimulate the gas")
#set the transparency of the window.
root.attributes("-alpha",0.9)
#set the size.
root.geometry('1440x920')
#set the place of window when it start
root.resizable(0,0)
#set the iconbitmap
root.iconbitmap('Gas simulation.ico')

# Creat the Figure 1 2 3
f1 = Figure(figsize=(5,4),dpi=100)
fig1 = f1.add_axes([0.20, 0.2, 0.7, 0.6])

f2 = Figure(figsize=(5,4),dpi=100)
fig2 = f2.add_axes([0.20, 0.2, 0.7, 0.6])

f3 = Figure(figsize=(5,4),dpi=100)
fig3 = f3.add_axes([0.20, 0.2, 0.7, 0.6])

def thread_it(func,*args):
    """
    creat the new thread to run the function
    :param func: the funtion which is need to run in the new thread
    :param *args: the variables
    """
    t = threading.Thread(target=func,args=args)
    t.setDaemon(True)
    t.start()

def draw_vlo (data,colnum):
    """
    draw Final partical velocity distribution
    :param data: Vdata
    :param colnum: the number of columns
    """
    f2.clf()
    s2=v2.get()# get whether the user wants to show the graph
    if s2==1:
        fig2 = f2.add_axes([0.20, 0.2, 0.7, 0.6])
        fig2.hist(data, bins=colnum, normed=True)
        fig2.set_ylabel('Frequency')
        fig2.set_xlabel('V')
        fig2.set_title('Final partical velocity distribution')
    canvs2.draw()

def draw_dem(data,colnum):
    """
        draw a graph about demon energy according to the type mode, if type mode ==0, call dvt to draw a graph about time
        :param data: demdata
        :param colnum: the number of columns
    """
    global f2_type
    if f2_type==0:
        draw_dvt(data)
        return
    f3.clf()
    s3=v3.get()# get whether the user wants to show the graph
    if s3==1:
        fig3 = f3.add_axes([0.20, 0.2, 0.7, 0.6])
        fig3.hist(data, bins=colnum, normed=True)
        fig3.set_ylabel('Frequency')
        fig3.set_xlabel('Demon Energy')
        fig3.set_title('Demon Energy Histogram')
    canvs3.draw()

def draw_dvt(data):
    """
    draw the graph about demon energy vs time
    :param demdata:
    """
    f3.clf()
    s3=v3.get()# get whether the user wants to show the graph
    if s3==1:
        fig3 = f3.add_axes([0.20, 0.2, 0.7, 0.6])
        y=range(len(data))
        fig3.plot(y,data,)
        fig3.set_ylabel('Demon Energy')
        fig3.set_xlabel('steps')
        fig3.set_title('Time vs.Energy')
    canvs3.draw()


def drawplot(x,y):
    """
        draw a plot N vs.Energy
        :param data: demdata
        :param colnum: the number of columns
    """
    f1.clf()
    s1=v1.get() # get whether the user wants to show the graph
    if s1==1:
        fig1 = f1.add_axes([0.20, 0.2, 0.7, 0.6])
        fig1.plot(x,y)
        fig1.set_ylabel('Energy')
        fig1.set_xlabel('N')
        fig1.set_title('N vs.Energy')
    canvs1.draw()

def check_vari (number,energy,steps,state):
    """
    check whether the input values are suitable for running the program
    and give feedback is the input is not so good
    run if the inputs are good
    """
    result=True
    message=""
    for a in[number,energy,steps]:
        if a.isdigit():
            a=int(a)
            if (a<=0)or(type(a)!=int):
                result=False
                message+="{0} is not a possitive integer please input another\n".format(a)
        else:
            result=False
            message+="{0} is not a possitive integer please input another\n".format(a)
    if state==0:
        result=False
        message+="please choose one state\n"
    if result==False:
        messagebox.showwarning("Wrong Input",message)
    else: #start running
        if int(number)<100:
            messagebox.showwarning("Wrong Input", "number of verticles are too small for a exhaustive graph")
        v.set("The program is running. Please wait...")
        run(int(number),int(energy),int(steps),state)


def ideal_gas(N,totalenergy, steps,state,visuals=True):
    """
    :param N: Number of particles
    :param totalenergy: total of demon and system energy
    :param steps: number of simulation steps
    :param state: Initial state
    :param visuals: plot histogram?
    :return: the average energy of this experiment
    """
    v0=math.sqrt(2.0*totalenergy/N)
    deltaV=v0/10
    avenergy=0 #store the energy data to calculate the average
    avstep=30 #collect a energy data every 30 steps
    avtimes=0 #the times of the collection
    global demdata
    global vdata
    demdata=[] #used to store the domon energy after each step
    if state==1:
        v=[v0]*N
        systemenergy=float(totalenergy)
        demonenergy=0.0
    elif state==2:
        v=[0.0]*N
        systemenergy=0.0
        demonenergy=float(totalenergy)
    else:
        print ('State value error:state =1 or 2')
        return
    for k in range(steps):
        for i in range(N):
            dv=uniform(-deltaV,deltaV)                            #a random velocity change(temporary)
            rani=randint(0,N-1)                                   #choose a random number
            Vnew=v[rani]+dv                                       #assume the v[rani] is changed
            deltaenergy=0.5*(Vnew**2-v[rani]**2)                  #calculate the delta energy
            if deltaenergy<demonenergy:                           #under the condition (delta energy<demon energy):
                v[rani]=Vnew                                      #the assuption of the change of volecity make effact
                systemenergy=systemenergy+deltaenergy             #calculation of the new system energy
                demonenergy=demonenergy-deltaenergy               #calculation of the demon energy
        if visuals:
            demdata.append(demonenergy)                                #after one step, store the domon energy
        if avstep==0:
            avstep=30
            avenergy+=systemenergy
            avtimes+=1
        else:
            avstep-=1 #count 30 times for a nother collection
    if visuals:
        vdata=v
        n1=N1.get()
        n2=N2.get()
        draw_vlo (vdata,n2)
        draw_dem (demdata,n1)
    return avenergy/avtimes


def change_f1():
    """
    change the number of columns
    """
    global demdata
    n1=N1.get()
    draw_dem(demdata,n1)

def change_f2():
    """
    change the number of columns
    """
    global vdata
    n2=N2.get()
    draw_vlo(vdata,n2)


def change_f3():
    """
    change the graph type of f3
    """
    global f2_type
    if f2_type==0:
        Scale_figure1.place(x = 220,y = 820,height = 100,width = 300)
        T.set("change to E vs T")
    else:
        Scale_figure1.place_forget()
        T.set("change to E & F")
    f2_type=1-f2_type
    change_f1()





def run(N,totalenergy,steps, state):
    """
    :param N: Number of particles
    :param totalenergy: total of demon and system energy
    :param steps: number of simulation steps
    :param state: 1 for demon energy =0 2 for the opposite
    :return:
    """
    engdata=[] #store the energy data of each experiment
    ndata=[] #store the X coordinate of the engdata
    text_result.insert(END,"\n\nEXPERIMENT:\nN:{0}\ntotalenergy:{1}\nsteps:{2}\nstate:{3}\n".format(N,totalenergy,steps,state))
    for a in range(50,N-1,50):
        eng=ideal_gas(a,totalenergy,steps,state,False)
        engdata.append(eng)
        ndata.append(a)
        v.set("program working {0}%".format(2*a//len(range(50,N-1,50)))) #refresh the prograss
        canvs1.draw()          #just for refresh the window
        text_result.insert(END,"N:{0} energy:{1:.5f}\n".format(a,eng))
    engdata.append(ideal_gas(N,totalenergy,steps,state))
    ndata.append(N)
    text_result.insert(END,"N:{0} energy:{1:.5f}\n".format(N,engdata[-1]))
    v.set("") # clear the message
    drawplot(ndata,engdata)


def main():
    """
    get the number in the entry and run the program.
    """
    Number=N.get()                        #get the number in the entry,
    Energy=E.get()
    Steps=S.get()
    State=state.get()
    check_vari(Number,Energy,Steps,State) #run the check function

def end():
    """
    close the window.
    """
    root.quit()
    root.destroy()        # destory the root and close the window

def About():
    """
    creat the toplevel of the "About".
    """
    t1=Toplevel()           #creat the toplevel
    t1.geometry('400x200')  #set the size of it
    t1.title("About")       #set the title

    Message(t1,text="Leader:Yang Chenyu    1165743522@qq.com \n"
                    "Member：Han Bing      879090429@qq.com  \n"
                    "            Copyright © 2016 YH. All rights reserved.",width=400).pack()
    #Add the Back button to back.
    Back_Button = ttk.Button(t1,text="Back",command=t1.destroy).pack()

def Top_3D():
    """
    creat the toplevel to run the 3D stimulation.

    """
    t2=Toplevel()
    t2.geometry('400x200')      #set the size
    t2.title("Which one?")      #set the title
    global Number
    Number=StringVar()
    Entry_3D = Entry(t2,textvariable=Number)
    Entry_3D.place(x=200,y=10)

    Top_label = ttk.Label(t2,text="Please input tht number:")
    Top_label.place(x= 10, y = 10)
    # Add the run and back buttons
    Top_Button_3D1 = ttk.Button(t2, text="RUN!", command=run_3D11)
    Top_Button_3D1.place(x=80, y=50)

    Back_Button2 = ttk.Button(t2, text="Back", command=t2.destroy)
    Back_Button2.place(x=180, y=50)




def run_3D11():
    """
    check the number in the entry whether is correct.
    if the number isn't correct and it will tell you and
    do not run the program
    """
    number=Number.get()
    if number.isdigit():
        Number_n=int(Number.get())
        if Number_n>0:
            thread_it(run_3D,(Number_n))
        else:
            messagebox.showwarning("Wrong Input", "input is not positive")
    else:
        messagebox.showwarning("Wrong Input", "input is not a number")


def changebg():
    """
    change the background.
    """
    color=v4.get()
    root["bg"]=color

# Sava the figures and data to where you want.
def save_Figure1():
    """
    save the figure1 to other place.
    """
    F1 = filedialog.asksaveasfilename(title='Save Figure1', initialdir='d:\mywork', initialfile='Figure1.png')
    f1.savefig(F1)

def save_Figure2():
    """
    save the figure2 to other place.
    """
    F2 = filedialog.asksaveasfilename(title='Save Figure2', initialdir='d:\mywork', initialfile='Figure2.png')
    f2.savefig(F2)
def save_Figure3():
    """
    save the figure3 to other place.
    """
    F3 = filedialog.asksaveasfilename(title='Save Figure3', initialdir='d:\mywork', initialfile='Figure3.png')
    f3.savefig(F3)
def save_Data():
    """
    save the data to other place.
    """
    D = filedialog.asksaveasfilename(title='Save Data', initialdir='d:\mywork', initialfile='Run Results.txt')
    Data=text_result.get("0.0","end")   #get the data
    f = open(D,"w")
    f.write(Data)                       #write the data to the txt
    f.close()

def run_3D(n):
    """
    run the another py.
    :param n: Number of particles
    """
    collision3D.main(n)


#Some widgets
mainmenu = Menu(root)                      #creat the mainmenu
menu_figure=Menu(mainmenu,tearoff = 0)     #creat the "figure" menu to the mainmenu
menu_save=Menu(mainmenu,tearoff = 0)       #creat the "save" menu to the mainmenu
menu_color=Menu(mainmenu,tearoff = 0)      #creat the "color" menu to the mainmenu
menu_about=Menu(mainmenu,tearoff = 0)      #creat the "about" menu to the mainmenu

#Add checkbutton to the "Figure" menu
mainmenu.add_cascade(label="Figure",menu = menu_figure)
v1=IntVar()
v1.set(1)
v2=IntVar()
v2.set(1)
v3=IntVar()
v3.set(1)
menu_figure.add_checkbutton(label="Figure1",variable=v1,)
menu_figure.add_checkbutton(label="Figure2",variable=v2)
menu_figure.add_checkbutton(label="Figure3",variable=v3)

#Add cascade to the "save" menu
mainmenu.add_cascade(label="Save",menu = menu_save)
menu_save.add_cascade(label="Save Figure1",command=save_Figure1)
menu_save.add_cascade(label="Save Figure2",command=save_Figure2)
menu_save.add_cascade(label="Save Figure3",command=save_Figure3)
menu_save.add_cascade(label="Save the data",command=save_Data)

# Add radiobutton to the "color" menu
mainmenu.add_cascade(label="Color",menu = menu_color)
v4=StringVar()
menu_color.add_radiobutton(label="Gray",value="Gray",variable=v4,command=changebg)
menu_color.add_radiobutton(label="Red",value="Red",variable=v4,command=changebg)
menu_color.add_radiobutton(label="Green",value="Green",variable=v4,command=changebg)
menu_color.add_radiobutton(label="Blue",value="Blue",variable=v4,command=changebg)
menu_color.add_radiobutton(label="White",value="White",variable=v4,command=changebg)

#Add cascade to the "about" menu to open the toplevel
mainmenu.add_cascade(label="About",menu = menu_about)
menu_about.add_cascade(label="About",command=About)
root["menu"] = mainmenu

#creat the main Frame to the main widgets.
main_Frame=LabelFrame(height= 400 ,width= 480 ,text="Main")
main_Frame.place(x = 220,y = 10)

#Add the picture to the window
img=PhotoImage(file="cebian.gif")
label_img=Label(root,image=img)
label_img.place(x = 0,y = 0)

#Add the message to explain how to use the program
message_use=Message(main_Frame,text="Please input the reasonable number and this program will give the "
                                    "gas simulation' results and draw the figures. You can choose which"
                                    " one figure will be shown in the menu.",width = 450)
message_use.place(x = 20,y = 310)

#Add the text to show the results and textbar
text_result=Text(root,width = 200)
text_result.place(x = 1230,y = 0,height = 900, width = 200)
text_bar=Scrollbar(root)
text_bar.pack(side = RIGHT,fill = Y)
text_result["yscrollcommand"] = text_bar.set
text_bar["command"] = text_result.yview

#Add the tiplabel
v=StringVar()
v.set("")
Tip_Label=Label(main_Frame,textvariable=v,fg="red")
Tip_Label.place(x = 220,y = 220)

# the label of number of atoms
label_N=ttk.Label(main_Frame,text="Please input the number of atoms:")
label_N.place(x = 20,y = 20)
# the label of energy of atoms
label_E=ttk.Label(main_Frame,text="Please input the energy of atoms:")
label_E.place(x = 20,y = 70)
# the label of steps
label_S=ttk.Label(main_Frame,text="Please input the step you want to go:")
label_S.place(x = 20,y = 120)

# the entry of number of atoms
N=StringVar()
Entry_N=ttk.Entry(main_Frame,textvariable=N)
Entry_N.place(x = 250,y = 20)
# the entry of energy of atoms
E=StringVar()
Entry_E=ttk.Entry(main_Frame,textvariable=E)
Entry_E.place(x = 250,y = 70)
# the steps of the stimulation
S=StringVar()
Entry_S=ttk.Entry(main_Frame,textvariable=S)
Entry_S.place(x = 250,y = 120)

# the radiobutton to choose which pattern to run.
state = IntVar()
Radiobutton_demon=ttk.Radiobutton(main_Frame,text="Give all the energy to demon",value=1,variable = state)
Radiobutton_demon.place(x = 20,y = 170)

Radiobutton_energy=ttk.Radiobutton(main_Frame,text="Give all the energy to system",value=2,variable = state)
Radiobutton_energy.place(x = 20,y = 220)

#Add the run Button to run the program
Button_run=ttk.Button(main_Frame,text="Start and Show",command=lambda:thread_it(main,))
Button_run.place(x = 70,y = 270,height = 30,width = 150)

#Add the quit Button to quit the program
Button_quit=ttk.Button(main_Frame,text="Quit",command=end)
Button_quit.place(x = 250,y = 270,height = 30,width = 150)

#Add the 3D button to open the 3D stimulation。
Button_3D=ttk.Button(main_Frame,text="Open the 3D",command=Top_3D)
Button_3D.place(x=250,y=170,width = 150,height = 30)

# Add the scale to adjust the figure1
N1=IntVar()
Scale_figure1=Scale(root,from_=5,to=15,orient=HORIZONTAL,variable=N1,label="Please choose the column's number")
Scale_figure1.place(x = 220,y = 820,height = 100,width = 300)
Scale_figure1.set(10)
# button to change
Button_change1=ttk.Button(root,text="Change the figure",command=change_f1)
Button_change1.place(x = 550,y = 820)

# the button to change the figure to another
T=StringVar() # the caption of the label
T.set("change to E vs. T")
Button_change3=ttk.Button(root,textvariable=T,command=change_f3)
Button_change3.place(x = 550,y = 850)

# Add the scale to adjust the figure2
N2=IntVar()
Scale_figure2=Scale(root,from_=5,to=15,orient=HORIZONTAL,variable=N2,label="Please choose the column's number")
Scale_figure2.place(x = 720,y = 820,height = 100,width = 300)
Scale_figure2.set(10)
# Button to change the figure.
Button_change2=ttk.Button(root,text="Change the figure",command=change_f2)
Button_change2.place(x = 1050,y = 820)

# add 3 canvses to show figures.
canvs1 = FigureCanvasTkAgg(f1,root)
canvs1.get_tk_widget().place(x = 720,y = 20,height = 400,width = 500)

canvs2 = FigureCanvasTkAgg(f2,root)
canvs2.get_tk_widget().place(x = 720,y = 420,height = 400,width = 500)

canvs3 = FigureCanvasTkAgg(f3,root)
canvs3.get_tk_widget().place(x = 220,y = 420,height = 400,width = 500)

# Add the toolbar to adjust the figure.
toolbar1 = NavigationToolbar2TkAgg(canvs1,root)
toolbar1.update()
toolbar1.place(x = 720,y = 20)

toolbar2 = NavigationToolbar2TkAgg(canvs2,root)
toolbar2.update()
toolbar2.place(x = 720,y = 420)

toolbar3 = NavigationToolbar2TkAgg(canvs3,root)
toolbar3.update()
toolbar3.place(x = 220,y = 420)

root.mainloop()