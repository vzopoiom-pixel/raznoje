import  tkinter as tk

bomb = 100# timer
score = 0
press_return = True


root = tk.Tk()


root.title("Game")

root.geometry("600x600+500+400")

root.iconbitmap("bomb.ico")

root.mainloop()

# root.resizable(False, False)
# root.minsize()
# root.maxsize()



label_1 = tk.Lable(root, text="Hello wordl", font=("Cosmic Sans MS", 14),  bg="red")
label.pack()

label_bomb = tk.Lable(root, text=f"time: {str(bomb)}", font=("Cosmic Sans MS", 14),  bg="red")
label_bomb.pack()

label_bomb = tk.Lable(root, text=f"score: {str(score)}", font=("Cosmic Sans MS", 14),  bg="red")
score_lable.pack()

img_1 = tk.PhotoImage(file="1.gif")
img_2 = tk.PhotoImage(file="2.gif")
img_3 = tk.PhotoImage(file="3.gif")
img_4 = tk.PhotoImage(file="4.gif")

bomb_lable =  tk.Label(image=img_1)
bomb_lable.pack()

def is_alive():
    global bomb
    global press_return
    if bomb <= 0:
        bomb = 0
        label.config(text="Boom!")
        press_return = true
        return False
    else:
        return True
    def click():
        global bomb
        if  is_alive():
            bomb += 1



    def start():
        global press_return
        if not press_return:
            pass
    else:


    def update_bomb():
        global  bomb
        bomb -= 20
        if is_alive():
            label_bomb.after(400, update_bomb())

def update_score():
    global score
    if is_alive():
        score += 1
        score_lable.after(1000, update_score())

def update



click_button = tk.Button(root, text="Click me", width=15, fg="white", bg="black")


root.mainloop()


