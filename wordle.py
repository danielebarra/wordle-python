from tkinter import *
from random import *
from time import sleep


win_width = "450"
win_height = "650"

win = Tk()
win.title("Wordle in Python")
win.geometry(win_width + "x" + win_height)
win.resizable(False, False)



file = open("60000_parole_italiane.txt", "r", encoding="utf-8")
text = file.read()
file.close()

words = text.splitlines() # Divide il testo in una lista di parole
words = [word for word in words if len(word) == 5]  # Prende solo le parole di 5 lettere


def tksleep(self, time:float) -> None:

    # Emulating `time.sleep(seconds)`

    self.after(int(time*1000), self.quit)
    self.mainloop()
Misc.tksleep = tksleep


def canvas_entry():
    global cnv_entry
    
    cnv_entry = Canvas(win, width= win_width, height= win_height, bg="white")
    
    entry_lbl1 = cnv_entry.create_text(int(win_width) / 2, 80, text="Benvenuto in WORDLE!", fill="black", font='Lexend 20 bold')
    entry_lbl2 = cnv_entry.create_text(int(win_width) / 2, 140, text="Indovina la parola di 5 lettere in 6 tentativi.", fill="black", font='Lexend 15 bold')
    entry_lbl3 = cnv_entry.create_text(int(win_width) / 2, 220, text="Dopo ogni tentativo ti verrà detto \n quale lettera è nella posizione giusta \n o se è nella posizione sbagliata.", fill="black", font='Lexend 15 bold', justify="center")
    entry_lbl4 = cnv_entry.create_text(int(win_width) / 2, 370, text="Buona fortuna!", fill="black", font='Lexend 20 bold')
    entry_lbl5 = cnv_entry.create_text(int(win_width) - 30, int(win_height) - 20, text="danny", fill="black", font='Lexend 10 bold')
    
    
    entry_btn = Button(cnv_entry, text="INIZIA", command= entrybtn_clicked, width=15, height=2, font='Lexend 12 bold')
    cnv_entry.create_window(int(win_width) / 2, 450, window=entry_btn)
    
    cnv_entry.pack()


def canvas_game():
    global cnv_game
    global label_grid
    global rect_grid
    
    label_grid = list()
    rect_grid = list()
    
    cnv_game = Canvas(win, width= win_width, height= win_height, bg="white")

    title_lbl = cnv_game.create_text(int(win_width) / 2, 50, text="WORDLE", fill="black", font='Lexend 20 bold')

    x = 20
    y = 100
    width = 75
    height = 75

    for i in range (0, 6):
        label_row = list()
        rect_row = list()
        
        for j in range (0, 5):
            
            rect = cnv_game.create_rectangle(x, y, x + width, y + height, fill="white", outline="dark gray", width=1.5)
            rect_row.append(rect)
            label = cnv_game.create_text(x + (width / 2), y + (height / 2), text= "", fill="black", font='Lexend 20 bold')
            label_row.append(label)
            x = x + width + 10

        label_grid.append(label_row)
        rect_grid.append(rect_row)
        
        x = 20
        y = y + height + 15


    start_game()
    
    cnv_game.pack()


def canvas_end(result, answer):
    global cnv_end
    
    cnv_game.destroy()
    cnv_end = Canvas(win, width= win_width, height= win_height, bg="white")
    
    end_lbl_bg = cnv_end.create_text(int(win_width) / 2, 100, text="", fill="black", font='Lexend 30 bold')
    end_lbl_fg = cnv_end.create_text((int(win_width) / 2) + 2, 101, text="", fill="black", font='Lexend 30 bold')
    
    if result:
        cnv_end.itemconfig(end_lbl_fg, text= "HAI VINTO!", fill="green")
        cnv_end.itemconfig(end_lbl_bg, text= "HAI VINTO!", fill="black")
    else:
        cnv_end.itemconfig(end_lbl_fg, text= "HAI PERSO!", fill="red")
        cnv_end.itemconfig(end_lbl_bg, text= "HAI PERSO!", fill="black")
    
    end_lbl2 = cnv_end.create_text(int(win_width) / 2, 200, text= f"La risposta era {answer.upper()}", fill="black", font='Lexend 20 bold')
    end_lbl3 = cnv_end.create_text(int(win_width) / 2, 400, text= "Vuoi rigiocare?", fill="black", font='Lexend 20 bold')
    
    end_btn = Button(cnv_end, text="RICOMINCIA", command= endbtn_clicked, width=15, height=2, font='Lexend 12 bold')
    cnv_end.create_window((int(win_width) / 2) +  (int(win_width) / 4), 480, window=end_btn)
    
    quit_btn = Button(cnv_end, text="ESCI", command= quitbtn_clicked, width=15, height=2, font='Lexend 12 bold')
    cnv_end.create_window(int(win_width) / 4, 480, window=quit_btn)
    
    cnv_end.pack()


def entrybtn_clicked():
    cnv_entry.destroy()
    canvas_game()
    
def endbtn_clicked():
    cnv_end.destroy()
    canvas_entry()
    
def quitbtn_clicked():
    win.destroy()

def get_random_word(words):
    i = randint(0, len(words))
    return words[i]

def start_game():
    
    grid_x = 0
    grid_y = 0
    guess = ""
    
    # Ottiene una parola casuale dalla lista
    answer_word = get_random_word(words)
    answer = [ele for ele in answer_word]


    # Gestisce l'inserimento di un tasto
    def on_key_press(event):
        nonlocal guess
        nonlocal grid_x
        nonlocal grid_y
        
        letter = event.char.lower()
        
        # Se il tasto è una lettera dell'alfabeto 
        if letter.isalpha() and len(letter) == 1 and len(guess) < 5:
            
            
            cnv_game.itemconfig(label_grid[grid_y][grid_x], text=letter.upper())
            guess += str(letter)
        
            grid_x += 1

        # Se il tasto è BackSpace allora cancella l'ultimo carattere
        if event.keysym == 'BackSpace' and len(guess) > 0:
            guess = guess[:-1]
            
            grid_x -= 1
            cnv_game.itemconfig(label_grid[grid_y][grid_x], text="")
        
        # Se il tasto è Invio allora confermi la risposta
        if event.keysym == 'Return' and len(guess) == 5:
            guess_complete()
    
    
    # Gestisce la conferma della guess
    def guess_complete():
        nonlocal guess
        nonlocal grid_x
        nonlocal grid_y
        
        win.unbind("<Key>")
        
        
        green_letters = dict()
        yellow_letters = dict()
        
        used_indices = set()
        
        for i in range(len(guess)):
            if answer[i] == guess[i]:
                green_letters[i+1] = guess[i]
                used_indices.add(i)
        
        for i in range(len(guess)):
            if i not in used_indices and guess[i] in answer:
                for j in range(len(answer)):
                    if answer[j] == guess[i] and j not in used_indices:
                        yellow_letters[i+1] = guess[i]
                        used_indices.add(j)
                        break
        
        
        for i in range(0, 5):
            if i+1 in green_letters:
                cnv_game.itemconfig(rect_grid[grid_y][i], fill="green")
            elif i+1 in yellow_letters:
                cnv_game.itemconfig(rect_grid[grid_y][i], fill="yellow")
            else:
                cnv_game.itemconfig(rect_grid[grid_y][i], fill="gray")
            tksleep(win, 0.18)
        
        
        
        if guess == answer_word:
            tksleep(win, 0.5)
            canvas_end(True, answer_word)
        else:
            if grid_y < 5:
                grid_x = 0
                grid_y += 1
                guess = ""
                
                win.bind("<Key>", on_key_press)
            else:
                canvas_end(False, answer_word)
        
        
    win.bind("<Key>", on_key_press)
    


canvas_entry()

win.mainloop()

