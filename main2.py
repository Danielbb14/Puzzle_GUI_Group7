#!/usr/bin/env python3
"""
main2.py

This file launches a word puzzle game with a difficulty selection window.
After the user selects a difficulty (Easy, Medium, or Hard), the game board appears.
The chosen difficulty is displayed at the bottom left of the game window.

Required libraries:
  - tkinter (for the GUI)
  - random (for random choices)
  - array2d (your custom module; ensure array2d.py is in the same directory)
"""

from tkinter import Tk, Button, Label, Frame
import random
from array2d import Array2D

# ------------------------------
# Original Puzzle Game Code
# ------------------------------
class Application():
    def __init__(self):
        self.startGame()  

    def startGame(self):
        self.word2DArray = Array2D(10, 10)
        self.selectedWords = ['carrot', 'potato', 'fish']
        self.word2DArray.populate(self.selectedWords)
        self.found_words = []
        self.current_coords = []
        self.current_word = ""
        self.total_words = len(self.selectedWords)
        self.words_to_find_labels = []
        self.found_count = 0
        self.remaining_lives = 3
        self.time_left = 600
        self.build()

    def restartGame(self):
        self.root.destroy()
        self.startGame()

    def build(self):
        self.root = Tk()
        self.root.title("Word Search")
        self.root.configure(bg='white')
        self.root.minsize(width=400, height=500)
        
        # Main UI group component
        control_panel = Frame(self.root, bg='white', pady=10)
        control_panel.grid(row=0, column=0, sticky='ew')        
        
        # Hint button
        hint_btn = Button(
            control_panel,
            text="HINT",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.show_hint
        )
        hint_btn.grid(row=0, column=0, padx=10)

        # Found words label
        self.found_words_label = Label(
            control_panel,
            text=f"FOUND\n{self.found_count}/{self.total_words}",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            padx=20,
            pady=5
        )
        self.found_words_label.grid(row=0, column=1, padx=10)
        
        # Timer label
        self.timer_label = Label(
            control_panel,
            text="08:42",
            font=('Arial', 16, 'bold'),
            bg='#FFD700',
            fg='black',
            padx=40,
            pady=5
        )
        self.timer_label.grid(row=0, column=2, padx=10)
        
        # Lives label
        self.heart_labels = []
        lives_frame = Frame(control_panel, bg='#4285F4', padx=20, pady=5)
        lives_frame.grid(row=0, column=3, padx=10)
        for i in range(3):
            heart = Label(
                lives_frame,
                text="♥",
                font=('Arial', 14),
                fg='red' if i < self.remaining_lives else 'gray',
                bg='#4285F4'
            )
            heart.pack(side='left', padx=2)
            self.heart_labels.append(heart)
        
        # Quit button
        quit_btn = Button(
            control_panel,
            text="QUIT",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.destroyGame
        )
        quit_btn.grid(row=0, column=4, padx=10)

        # Restart button
        restart_btn = Button(
            control_panel,
            text="RESTART",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.restartGame
        )
        restart_btn.grid(row=0, column=5, padx=10)
        
        # Word search grid
        self.searchGrid = self.displayWordSearch()
        self.searchGrid.grid(row=1, column=0)
        
        # Words to find section
        self.words_frame = Frame(self.root, bg='white', pady=20)
        self.words_frame.grid(row=2, column=0)
        Label(
            self.words_frame,
            text="Words to select",
            font=('Arial', 20),
            fg="black",
            bg='white',
            pady=10
        ).pack()
        bordered_frame = Frame(
            self.words_frame,
            bg='white',
            highlightbackground='black',
            highlightthickness=1,
            padx=20,
            pady=10
        )
        bordered_frame.pack(pady=10)
        Label(
            bordered_frame,
            text="Words to find",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack()
        word_list_frame = Frame(bordered_frame, bg='white', pady=10)
        word_list_frame.pack()
        for i, word in enumerate(self.selectedWords):
            l = Label(
                word_list_frame,
                text=word,
                font=('Arial', 12),
                fg="black",
                bg='white',
                padx=10
            )
            l.grid(row=0, column=i)
            self.words_to_find_labels.append(l)
        
        self.update_timer()
        self.root.mainloop()
    
    def displayWordSearch(self):
        self.WordSearchFrame = Frame(self.root, padx=20, pady=20)
        x = self.word2DArray.numrows()
        y = self.word2DArray.numcols()
        self.Buttons = Array2D(x, y)
        for i in range(x):
            for j in range(y):
                text = self.word2DArray[i, j]
                but = Button(
                    self.WordSearchFrame, 
                    text=text, 
                    width=2, 
                    height=1,
                    font=('Arial', 12),
                    bg='white',
                    fg='black',
                    disabledforeground='black',
                    border=0,
                    command=lambda i=i, j=j: self.submitData((i, j))
                )
                but.grid(row=i, column=j, padx=1, pady=1)
                self.Buttons[i, j] = but
        return self.WordSearchFrame

    def udpate_found_words_label(self):
        self.found_words_label.configure(text=f"FOUND\n{self.found_count}/{self.total_words}")

    def update_lives_display(self):
        for i, heart in enumerate(self.heart_labels):
            heart.configure(fg='red' if i < self.remaining_lives else 'gray')
        if self.remaining_lives <= 0:
            self.show_game_result(self.words_frame, False)

    def submitData(self, coords):
        row, col = coords
        button = self.Buttons[row, col]
        self.current_word += button['text']
        print("clicked for curr word: {}".format(self.current_word))
        self.current_coords.append([row, col])
        button.config(bg="orange", activebackground="orange", relief="solid", highlightbackground="orange")
        if self.current_word in self.selectedWords:
            print(f"Word found: {self.current_word}")
            self.found_words.append(self.current_word)
            print("updated found words: {}".format(self.found_words))
            self.found_count += 1
            self.udpate_found_words_label()
            self.cross_found_word(self.current_word)
            for coords in self.current_coords:
                btn = self.Buttons[coords[0], coords[1]]
                btn.config(bg="green", activebackground="green", relief="solid", highlightbackground="green")
            if self.found_count == len(self.selectedWords):
                print("YOU WON!!!:-)")
                self.show_game_result(self.words_frame, True)
            self.resetSelection()
        elif not any(word.startswith(self.current_word) for word in self.selectedWords):
            print(f"Invalid word: {self.current_word}")
            for coords in self.current_coords:
                btn = self.Buttons[coords[0], coords[1]]
                btn.config(bg="white", activebackground="white", relief="solid", highlightbackground="black")
            self.resetSelection()
            self.remaining_lives -= 1
            self.update_lives_display()
            if self.remaining_lives == 0:
                print("YOU LOST:-(")
                self.show_game_result(self.words_frame, False)

    def cross_found_word(self, word):
        for l in self.words_to_find_labels:
            if l['text'] == word:
                l.configure(bg='green')
                return

    def resetSelection(self):
        self.current_word = ""
        self.current_coords = []

    def update_timer(self):
        if self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="00:00")
            self.show_game_result(self.words_frame, False)

    def show_game_result(self, frame, won=True):
        for widget in frame.winfo_children():
            widget.destroy()
        self.time_left = 0
        message = "🎉 You Won!!! 🎉" if won else "❌ You Lost, Better Luck Next Time!"
        text_color = "green" if won else "red"
        result_label = Label(
            frame, 
            text=message, 
            font=("Arial", 20, "bold"), 
            fg=text_color
        )
        result_label.pack(expand=True)

    def destroyGame(self):
        self.root.destroy()

    def show_hint(self):
        missing_words = [word for word in self.selectedWords if word not in self.found_words]
        if not missing_words:
            return
        chosen_word = random.choice(missing_words)
        coords_list = self.word2DArray.placements.get(chosen_word, [])
        if not coords_list:
            return
        hint_coord = random.choice(coords_list)
        row, col = hint_coord
        hint_button = self.Buttons[row, col]
        original_bg = hint_button.cget("bg")
        hint_button.config(bg="blue")
        self.root.after(2000, lambda: hint_button.config(bg=original_bg))

# ------------------------------
# Subclass to Add Difficulty Level Display
# ------------------------------
class ApplicationWithDifficulty(Application):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        super().__init__()

    def build(self):
        self.root = Tk()
        self.root.title("Word Search")
        self.root.configure(bg='white')
        self.root.minsize(width=400, height=500)
        
        control_panel = Frame(self.root, bg='white', pady=10)
        control_panel.grid(row=0, column=0, sticky='ew')
        
        hint_btn = Button(
            control_panel,
            text="HINT",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.show_hint
        )
        hint_btn.grid(row=0, column=0, padx=10)
        
        self.found_words_label = Label(
            control_panel,
            text=f"FOUND\n{self.found_count}/{self.total_words}",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            padx=20,
            pady=5
        )
        self.found_words_label.grid(row=0, column=1, padx=10)
        
        self.timer_label = Label(
            control_panel,
            text="08:42",
            font=('Arial', 16, 'bold'),
            bg='#FFD700',
            fg='black',
            padx=40,
            pady=5
        )
        self.timer_label.grid(row=0, column=2, padx=10)
        
        self.heart_labels = []
        lives_frame = Frame(control_panel, bg='#4285F4', padx=20, pady=5)
        lives_frame.grid(row=0, column=3, padx=10)
        for i in range(3):
            heart = Label(
                lives_frame,
                text="♥",
                font=('Arial', 14),
                fg='red' if i < self.remaining_lives else 'gray',
                bg='#4285F4'
            )
            heart.pack(side='left', padx=2)
            self.heart_labels.append(heart)
        
        quit_btn = Button(
            control_panel,
            text="QUIT",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.destroyGame
        )
        quit_btn.grid(row=0, column=4, padx=10)

        restart_btn = Button(
            control_panel,
            text="RESTART",
            font=('Arial', 12, 'bold'),
            bg='#4285F4',
            fg='white',
            border=0,
            padx=20,
            pady=5,
            command=self.restartGame
        )
        restart_btn.grid(row=0, column=5, padx=10)
        
        self.searchGrid = self.displayWordSearch()
        self.searchGrid.grid(row=1, column=0)
        
        self.words_frame = Frame(self.root, bg='white', pady=20)
        self.words_frame.grid(row=2, column=0)
        Label(
            self.words_frame,
            text="Words to select",
            font=('Arial', 20),
            fg="black",
            bg='white',
            pady=10
        ).pack()
        bordered_frame = Frame(
            self.words_frame,
            bg='white',
            highlightbackground='black',
            highlightthickness=1,
            padx=20,
            pady=10
        )
        bordered_frame.pack(pady=10)
        Label(
            bordered_frame,
            text="Words to find",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack()
        word_list_frame = Frame(bordered_frame, bg='white', pady=10)
        word_list_frame.pack()
        for i, word in enumerate(self.selectedWords):
            l = Label(
                word_list_frame,
                text=word,
                font=('Arial', 12),
                fg="black",
                bg='white',
                padx=10
            )
            l.grid(row=0, column=i)
            self.words_to_find_labels.append(l)
        
        # Display the selected difficulty at the bottom left
        diff_label = Label(
            self.root,
            text=f"Difficulty level : {self.difficulty}",
            font=('Arial', 12),
            bg='white',
            fg='black'
        )
        diff_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        
        self.update_timer()
        self.root.mainloop()

# ------------------------------
# Difficulty Selection UI
# ------------------------------
def difficulty_selection():
    diff_root = Tk()
    diff_root.title("Select Difficulty")
    diff_root.configure(bg="white")
    
    title = Label(diff_root, text="Select Difficulty", font=("Arial", 16, "bold"), bg="white")
    title.pack(pady=20)
    
    def select_difficulty(level):
        diff_root.destroy()
        ApplicationWithDifficulty(level)
    
    btn_frame = Frame(diff_root, bg="white")
    btn_frame.pack(pady=20)
    
    Button(btn_frame, text="Easy", font=("Arial", 12), width=10, command=lambda: select_difficulty("Easy")).pack(pady=5)
    Button(btn_frame, text="Medium", font=("Arial", 12), width=10, command=lambda: select_difficulty("Medium")).pack(pady=5)
    Button(btn_frame, text="Hard", font=("Arial", 12), width=10, command=lambda: select_difficulty("Hard")).pack(pady=5)
    
    diff_root.mainloop()

if __name__ == '__main__':
    difficulty_selection()