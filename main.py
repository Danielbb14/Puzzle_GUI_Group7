from tkinter import Tk, messagebox, Button, Label, Entry, Frame
from array2d import Array2D


class Application():
    def __init__(self):
        self.btnList = [[], [], [], [], [], [], [], [], [], []]
        
        Array2D.__init__(self,10,10)
        self.word2DArray = Array2D(10,10)
        self.word2DArray.populate()
        self.b = Array2D(10,10)
        self.selectedWords = ['carrot','potato', 'fish']

        self.build()



    # For Building Game
    def build(self):
        self.root = Tk()
        self.root.title("Word Search")
        self.root.minsize(width=400, height=500)
        self.labelH = Label(self.root, text="Word Search", font='Arial 15 bold')
        self.labelH.grid(row=0)
        self.label1 = Label(self.root, text=f"Remaining Chances: {3}", font="Arial 10 bold", fg='red')
        self.label1.grid(row=1,pady=(0,10))
        f = self.displayWordSearch()
        f.grid(row=2, column=0)
        self.frame1 = Frame(self.root)
        for i,n in enumerate(self.selectedWords):
            lab = Label(self.frame1, text=n, font='Arial 10 bold')
            lab.grid(row=i//5,column=i%5,padx=8)
        self.frame1.grid(row=3, column=0,pady=10)
        self.exitButton = Button(self.root, text="Exit", command=self.destroyGame, fg="white",bg="red", font="Arial 10 bold")
        self.exitButton.grid(row=5,ipadx=5,pady=(0,5))
        self.root.mainloop()


    

    # For Ending Game
    def destroyGame(self):
        self.root.destroy()


    def displayWordSearch(self):
        self.WordSearchFrame = Frame(self.root)
        x=self.word2DArray.numrows()
        y=self.word2DArray.numcols()
        self.Buttons = Array2D(x,y)
        for i in range(x):
            for j in range(y):
                text = self.word2DArray[i,j]

                but = Button(self.WordSearchFrame, text=text, height=2, width=5, 
             fg="black", font=("Arial", 15, "bold"), 
             command=lambda coords=(i, j): self.submitData(coords))
                
                self.btnList[i-1].append(but)
                but.grid(row=i,column=j)
        return self.WordSearchFrame






Application()