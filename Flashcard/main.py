from tkinter import *
import pandas
from random import choice
from csv import DictWriter

current_char = {}
jpcharlist = {}

BACKGROUND_COLOR = "#913228"
FLIPTEXT = "white"
TEXT = "black"

BACKCARD = "/Users/DeWhi/OneDrive/Documents/Programing/Respository code/Shakyy/Flashcard/image/back_card.png"
FRONTCARD = "/Users/DeWhi/OneDrive/Documents/Programing/Respository code/Shakyy/Flashcard\image/front_card.png"
CROSS = "/Users/DeWhi/OneDrive/Documents/Programing/Respository code/Shakyy/Flashcard/image/cross.png"
MARK = "/Users/DeWhi/OneDrive/Documents/Programing/Respository code/Shakyy/Flashcard/image/mark.png"

try:
    data = pandas.read_csv("data/word_to_learn.csv")
except FileNotFoundError:
    original = pandas.read_csv("data/Frequentwords(3061).csv")
    print(original)
    jpcharlist = original.to_dict(orient="record")
else:
    jpcharlist = data.to_dict(orient="records") 
    
#-----------------RandomWord-------------------#
def nextcard():
   global current_char, flip_timer 
   window.after_cancel(flip_timer)
   current_char = choice(jpcharlist)
   canvas.itemconfig(card_title, text="Japanese", fill=TEXT, font=("Ariel", 48, "italic"))
   canvas.itemconfig(card_word, text=current_char["japanese"], fill=TEXT, font=("Ariel", 68, "bold"))
   canvas.itemconfig(card_image, image=card_font_image)
   flip_timer = window.after(3000, func=flip)
   
#------------------Flip------------------------#
def flip():   
    canvas.itemconfig(card_title, text="English", fill=FLIPTEXT)
    canvas.itemconfig(card_word, text=current_char["english"], fill=FLIPTEXT)
    canvas.itemconfig(card_image, image=card_back_image) 
    

#----------------Is known----------------------#
def is_known():
    # Add have_learn to new csv file
    field_names = ["japanese", "english"]
    with open("data/word_have_learned.csv", mode="a", encoding='utf-8') as data_file:
        dictwriter_object = DictWriter(data_file, fieldnames= field_names)
        dictwriter_object.writerow(current_char)
        data_file.close()
    
    # Remove from pool
    jpcharlist.remove(current_char)
    print(len(jpcharlist))
    data = pandas.DataFrame(jpcharlist)
    data.to_csv("data/word_to_learn.csv", index=False)

    nextcard()

#------------------UI---------------------#

window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip)

#Text box
canvas = Canvas(width=1100, height=650)
card_back_image = PhotoImage(file=BACKCARD)
card_font_image = PhotoImage(file=FRONTCARD)
card_image = canvas.create_image(560, 320, image=card_font_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(560, 200, text="", fill="black", font=("Ariel", 52, "bold"))
card_word = canvas.create_text(560, 370, text="", fill="black", font=("Ariel", 35, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

#Button
cross_img = PhotoImage(file=CROSS)
unknow_but = Button(image=cross_img, highlightthickness=0, command=nextcard) 
unknow_but.grid(row=1, column=0)

mark_img = PhotoImage(file=MARK)
known_but = Button(image=mark_img, highlightthickness=0, command=is_known)
known_but.grid(row=1, column=1)

nextcard()

window.mainloop()