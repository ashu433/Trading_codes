from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as tmsg

####################################### Labels examples #################################################

# # Important Label Options
# # text - adds the text
# # bd - background
# # fg - foreground
# # font - sets the font
# # 1. font=("comicsansms", 19, "bold")
# # 2. font="comicsansms 19 bold"
# # padx - x padding
# # pady - y padding
# # relief - border styling - SUNKEN, RAISED, GROOVE, RIDGE


# # Important Pack options
# # anchor = nw
# # side = top, bottom, left, right
# # fill
# # padx
# # pady
# # title_label.pack(side=BOTTOM, anchor ="sw", fill=X)



# GUI_root=Tk()

# min_width=644
# min_height=788

# GUI_root.minsize(min_width,min_height)
# GUI_root.title("OI Parameters charts")

# name=Label(text="OI chart data Representation",bg="red",fg="white",padx=13,pady=14,font="comicsansms 19 bold",borderwidth=3,relief=SUNKEN)
# name.pack(side=TOP,pady=2)

# image = Image.open("stock_market.jpg")
# photo = ImageTk.PhotoImage(image)
# varun_label = Label(image=photo)
# varun_label.pack(side=BOTTOM,anchor='sw')



# GUI_root.mainloop()



# ####################################### Frame Button #################################################

def print1():
    print("The Other parameters are coming soon")

GUI_root=Tk()

GUI_root.geometry("644x744")
GUI_root.minsize(644,788)
GUI_root.title("Option Chain GUI")
title=Label(text="Charts",bg="black",fg="white",font="comicsansms 19 bold",padx=13,pady=14,borderwidth=4,relief=SUNKEN)
title.pack(side=TOP,pady=4)
f1=Frame(GUI_root,bg="grey",borderwidth=6,relief=SUNKEN)
f1.pack(side=LEFT,fill="y")
b1=Button(f1,fg="red",text="Print Now",font="comicsansms 19 bold",command=print1)
b1.pack(side=LEFT)
b3=Button(f1,fg="red",text="Print Now",font="comicsansms 19 bold",command=print1)
b3.pack(side=LEFT,padx=10)

f2=Frame(GUI_root,bg="grey",borderwidth=6,relief=SUNKEN)
f2.pack(side=RIGHT,fill='y')
b2=Button(f2,fg="red",text="Print Now",font="comicsansms 19 bold",command=print1)
b2.pack(side=LEFT)

l1=Label(f1,text="Other Parameters of the OI",font="comicsansms 19 bold")
l1.pack(pady=10,anchor='nw',padx=100)

l2=Label(f2,text="Live Update of the other data",font="comicsansms 19 bold")
l2.pack(pady=10,anchor='ne')

GUI_root.mainloop()


########################################### widget and grid ######################################################

# def get_all_values():
#     print(f"the name of the user is: {name_entry.get()}")

#     with open("input_file.txt",'a') as file:
#         file.write(f"{name_entry.get()} {gender_entry.get()} {Phone_entry.get()} {Payment_entry.get()} \n")

# GUI=Tk()


# width=566
# height=666

# GUI.geometry(f"{width}x{height}")
# GUI.title("Gym Form")
# Label(GUI, text="Welcome to Ashutosh Gym", font="comicsansms 13 bold", pady=4).grid(row=0, column=1)
# l1=Label(GUI,text="User Name", font="comicsansms 9 bold")
# l1.grid(row=4,column=0)
# l2=Label(GUI,text="Gender", font="comicsansms 9 bold")
# l2.grid(row=5,column=0)
# l3=Label(GUI,text="Phone Number", font="comicsansms 9 bold")
# l3.grid(row=6,column=0)
# l4=Label(GUI,text="Payment mode", font="comicsansms 9 bold")
# l4.grid(row=7,column=0)

# name_value=StringVar()
# gender_value=StringVar()
# Phone_value=StringVar()
# Payment_value=StringVar()
# Day_time=IntVar()
# Evening_time=IntVar()

# name_entry=Entry(GUI,textvariable=name_value)
# gender_entry=Entry(GUI,textvariable=gender_value)
# Phone_entry=Entry(GUI,textvariable=Phone_value)
# Payment_entry=Entry(GUI,textvariable=Payment_value)

# name_entry.grid(row=4,column=1)
# gender_entry.grid(row=5,column=1)
# Phone_entry.grid(row=6,column=1)
# Payment_entry.grid(row=7,column=1)

# Day_time_entry=Checkbutton(GUI,text="Day Slot",font="comicsansms 9 bold", variable=Day_time)
# Day_time_entry.grid(row=8,column=1)

# Evening_time_entry=Checkbutton(GUI,text="Evening Slot",font="comicsansms 9 bold", variable=Evening_time)
# Evening_time_entry.grid(row=9,column=1)

# b1=Button(GUI,text="Submit",command=get_all_values)
# b1.grid(row=10,column=1)



# GUI.mainloop()

# ################# Event ####################


# def func_1(event):
#     print("You pressed the button 3")

# GUI=Tk()

# GUI.geometry("688x788")
# GUI.title("Ashutosh GUI")

# events_handling=Button(GUI,text="Click me please")
# events_handling.grid()

# closing=Button(GUI,text="Quit")
# closing.grid(row=1)



# events_handling.bind('<Button-3>',func_1)
# closing.bind('<Double-1>',quit)


# GUI.mainloop()

# ######################## menues,dropdown menue, sub menues, scroll bars, message box #################################

# def my_func():
#     print("The menu is ready")

# def Rate_us():
#     print("Rate Us")
#     value=tmsg.askquestion("Please share your experience","Was your experience Good")

#     if value=="yes":
#         msg="Great! thatnks for your feedback"
#     else:
#         msg="We'll try to improve our service"
#     tmsg.showinfo("Experience",msg)

# def divya():
#     tmsg.showinfo("Divya will become your girl friend just keep going")

# GUI=Tk()

# GUI.geometry("456x678")
# GUI.title("Ashutosh GUI")

# Ashutosh_menu=Menu(GUI)

# m1=Menu(Ashutosh_menu,tearoff=0)
# m1.add_command(label="New Project", command=my_func)
# m1.add_command(label="Save",command=my_func)
# m1.add_separator()
# m1.add_command(label="Save as",command=my_func)
# m1.add_command(label="Print",command=my_func)

# GUI.config(menu=Ashutosh_menu)

# Ashutosh_menu.add_cascade(label="File",menu=m1)

# m2=Menu(Ashutosh_menu,tearoff=0)
# m2.add_command(label="Cut", command=my_func)
# m2.add_command(label="Copy",command=my_func)
# m2.add_separator()
# m2.add_command(label="Paste",command=my_func)
# m2.add_command(label="Find",command=my_func)
# m2.add_command(label="Quit",command=quit)

# GUI.config(menu=Ashutosh_menu)
# Ashutosh_menu.add_cascade(label="Edit",menu=m2)

# text_pad=Text(GUI)
# text_pad.pack(side=LEFT,fill=Y)

# Scrollbar_1=Scrollbar(GUI)
# Scrollbar_1.pack(side=RIGHT,fill=Y)



# m3=Menu(Ashutosh_menu,tearoff=0)
# m3.add_command(label="Help",command=help)
# m3.add_command(label="Rate",command=Rate_us)
# m3.add_command(label="Befriend Divya",command=divya)

# GUI.config(menu=Ashutosh_menu)
# Ashutosh_menu.add_cascade(label="faltu",menu=m3)

# GUI.mainloop()

########################################################## Scale #######################################################

# def give():
#     tmsg.showinfo("Candies given",f"You will get {my_slider.get()} candy! go and enjoy.")

# GUI=Tk()

# GUI.geometry("766x866")
# GUI.title("My_first_GUI")

# l1=Label(text="How many candy you want please enter here on the scale",font="comicsansms 13 bold")
# l1.pack()

# my_slider=Scale(GUI,from_=0,to=100,orient=VERTICAL,tickinterval=10,length=600)

# my_slider.pack()

# b1=Button(text="Submit",command=give)
# b1.pack()


# GUI.mainloop()

# from tkinter import *

# def calculate():
#     result = my_slider.get() * 2  # Example calculation
#     result_label.config(text=f"Result: {result}")

# GUI = Tk()
# GUI.geometry("766x866")
# GUI.title("My_first_GUI")

# l1 = Label(text="How many candies do you want? Please enter here on the scale", font="comicsansms 13 bold")
# l1.pack()

# my_slider = Scale(GUI, from_=0, to=100, orient=VERTICAL, tickinterval=10, length=300)
# my_slider.pack()

# calculate_button = Button(GUI, text="Calculate", command=calculate)
# calculate_button.pack()

# result_label = Label(GUI, text="Result: ", font="comicsansms 13 bold")
# result_label.pack()

# GUI.mainloop()

# from tkinter import *

# def calculate():
#     result = my_slider.get() * 2  # Example calculation
#     result_label.config(text=f"Result: {result}")

# GUI = Tk()
# GUI.geometry("766x866")
# GUI.title("My_first_GUI")

# l1 = Label(text="How many candies do you want? Please enter here on the scale", font="comicsansms 13 bold")
# l1.grid(row=0, column=0, padx=10, pady=10)

# my_slider = Scale(GUI, from_=0, to=100, orient=VERTICAL, tickinterval=10, length=300)
# my_slider.grid(row=1, column=0, padx=10, pady=10)

# calculate_button = Button(GUI, text="Calculate", command=calculate)
# calculate_button.grid(row=2, column=0, padx=10, pady=10)

# result_label_frame = Frame(GUI)  # Create a frame for the result label
# result_label_frame.grid(row=3, column=0, padx=10, pady=10)

# result_label = Label(result_label_frame, text="Result: ", font="comicsansms 13 bold")
# result_label.pack()

# GUI.mainloop()

