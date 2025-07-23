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
current_card = {}

#------------------- DATA LOADING ---------------------#
try:
    data = pd.read_csv("./data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
    print("Loaded words from words_to_learn.csv")


except FileNotFoundError:
    # If the file does not exist, load the full list from the original CSV files
    # This assumes that the original CSV files are present in the specified path
    data_1 = pd.read_csv("./data/french_words_pt_1.csv")
    data_2 = pd.read_csv("./data/french_words_pt_2.csv")
    to_learn = pd.concat([data_1, data_2], ignore_index=True).to_dict(orient="records")
    print("File not found. Loading the full list of words.")



#------------------- FUNCTIONS ---------------------#
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  # Cancel the previous flip timer

    current_card = random.choice(to_learn)
    # Update the card image to the front
    canvas.itemconfig(card, image=card_front_img)
    # Update the French word
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    window.after(3000, func=flip_card)

    


def flip_card():
    global current_card
    # Change the card image to the back of the card
    canvas.itemconfig(card, image=card_back_img)
    # Update the French word to the English meaning
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def add_to_list():
    global current_card, to_learn

    # Remove the current card from the list of words to learn
    to_learn.remove(current_card)
    # Save the updated list to a CSV file
    pd.DataFrame(to_learn).to_csv("./data/words_to_learn.csv", index=False)
    next_card()  # Show the next card after adding the current one to the list

#------------------- WINDOW SETUP ---------------------#
window = Tk()
window.title("French Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)

flip_timer = window.after(3000, func=flip_card)  # Wait for 3 seconds before showing the English meaning

#------------------- CANVAS SETUP ---------------------#
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file=CARD_FRONT)
card_back_img = PhotoImage(file=CARD_BACK)
card = canvas.create_image(410, 273, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"), fill="black")
card_word = canvas.create_text(400, 250, text="", font=(FONT_NAME, 60, "bold"), fill="black")


#------------------- BUTTONS SETUP ---------------------#
correct_img = PhotoImage(file=CORRECT_IMAGE)
incorrect_img = PhotoImage(file=INCORRECT_IMAGE)
correct_button = Button(image=correct_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
incorrect_button = Button(image=incorrect_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=add_to_list)
correct_button.grid(row=1, column=1)
incorrect_button.grid(row=1, column=0)


next_card()  # Show the first card when the program starts





window.mainloop()