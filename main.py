#------------------- IMPORTS ---------------------#
from tkinter import *
import random
import pandas as pd

#------------------- CONSTANTS ---------------------#
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
CARD_FRONT = "./images/card_front.png"
CARD_BACK = "./images/card_back.png"
CORRECT_IMAGE = "./images/right.png"
INCORRECT_IMAGE = "./images/wrong.png"

#------------------- WINDOW SETUP ---------------------#
window = Tk()
window.title("French Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)

#------------------- CANVAS SETUP ---------------------#
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file=CARD_FRONT)
card_back_img = PhotoImage(file=CARD_BACK)
canvas.create_image(410, 273, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
canvas.create_text(400, 150, text="French Word", font=(FONT_NAME, 40, "italic"), fill="black")
canvas.create_text(400, 250, text="English Meaning", font=(FONT_NAME, 60, "bold"), fill="black")

#------------------- BUTTONS SETUP ---------------------#
correct_img = PhotoImage(file=CORRECT_IMAGE)
incorrect_img = PhotoImage(file=INCORRECT_IMAGE)
correct_button = Button(image=correct_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR)
incorrect_button = Button(image=incorrect_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR)
correct_button.grid(row=1, column=1)
incorrect_button.grid(row=1, column=0)

#------------------- FUNCTIONS ---------------------#
def show_next_card():
    global current_card
    current_card = random.choice(data)
    canvas.itemconfig(canvas.find_withtag("text")[0], text=current_card["French"])
    canvas.itemconfig(canvas.find_withtag("text")[1], text=current_card["English"])
    canvas.itemconfig(canvas.find_withtag("image")[0], image=card_front_img)
    window.after(3000, flip_card)
def flip_card():
    canvas.itemconfig(canvas.find_withtag("text")[0], text=current_card["English"])
    canvas.itemconfig(canvas.find_withtag("text")[1], text=current_card["French"])
    canvas.itemconfig(canvas.find_withtag("image")[0], image=card_back_img)
def mark_as_correct():
    data.remove(current_card)
    if data:
        show_next_card()
    else:
        canvas.itemconfig(canvas.find_withtag("text")[0], text="No more cards!")
        canvas.itemconfig(canvas.find_withtag("text")[1], text="")
        canvas.itemconfig(canvas.find_withtag("image")[0], image=card_front_img)
        correct_button.config(state="disabled")
        incorrect_button.config(state="disabled")
def mark_as_incorrect():
    canvas.itemconfig(canvas.find_withtag("text")[0], text=current_card["French"])
    canvas.itemconfig(canvas.find_withtag("text")[1], text=current_card["English"])
    canvas.itemconfig(canvas.find_withtag("image")[0], image=card_front_img)
    window.after(3000, show_next_card)



#------------------- DATA LOADING ---------------------#
try:
    # Loads all the words from the CSV files
    data_1 = pd.read_csv("./data/french_words_pt_1.csv")
    data_2 = pd.read_csv("./data/french_words_pt_2.csv")
    
    # Concatenates the two DataFrames into one
    data = pd.concat([data_1, data_2], ignore_index=True)
    
except FileNotFoundError:
    data = pd.DataFrame(columns=["French", "English"])  
data = data.to_dict(orient="records")
#------------------- FUNCTIONS ---------------------#








window.mainloop()