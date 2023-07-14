from tkinter import *

def GUIStartup():
    global img
    global label2
    global label1
    img = PhotoImage(file = 'Images/MAESymbol.png')
    label0 = Label(root , text = "Halo Gravity Treatment" , anchor = N , font = ("Arial Bold" , 15))
    label1 = Label(root , image = img , anchor = CENTER)
    label2 = Label(root , text = "NCSU MAE" , anchor = S , font = ("Arial Bold" , 25))
    label0.pack()
    label1.pack()
    label2.pack()
    root.after(5000 , GUImain)
    #btn = Button(root, text = "Press Here To Start" , command = GUImain).pack()

def GUImain():
    global num
    global check
    if (num < 1):
        label2.destroy()
        label1.destroy()
    else:
        check.destroy()
    num = num + 1
    #check.destroy()
    check = Label(root , text = num , anchor = N)
    check.pack()
    root.after(1000 , GUImain)

if __name__ == "__main__":
    root = Tk()
    global num
    num = 0
    root.title("Halo Gravity Traction Control")
    root.geometry("800x480")

    GUIStartup()

    root.mainloop()