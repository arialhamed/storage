import os
import tkinter as tk
import tkinter.font as TkFont

class HomeActivity(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.title("File organizer")
        # self.wm_attributes("-transparentcolor", self['bg'])
        self.wm_attributes("-topmost", True)
        self.update_idletasks()
        self.resizable(False, False)
        defaultFont = TkFont.nametofont("TkDefaultFont")
        defaultFont.configure(size=20, family="Arial")
        self.bind_all("<KeyPress>", self.getKeyPress)
        self.textlol = ""

        # Variables
        windowWidth, windowHeight, borderThickness = 800, 600, 2
        cellWidth, cellHeight = windowWidth * .2, windowHeight * .1
        bg, fg = "#222222", "white"

        # Canvas
        self.mainCanvas = tk.Canvas(self, bg=bg, width=windowWidth, height=windowHeight)
        self.mainCanvas.grid(row=0, column=0, sticky="NW")
        self.mainCanvas.bind("<ButtonPress-1>", self.windowMoveStart)
        self.mainCanvas.bind("<ButtonRelease-1>", self.windowMoveStop)
        self.mainCanvas.bind("<B1-Motion>", self.windowMoveDo)
        
        # Micron logo
        imageMicronLogo = tk.PhotoImage(file="logo.png")
        self.mainCanvas.create_image(0, 0, image=imageMicronLogo, anchor="nw")

        # Header text
        textHeader = self.mainCanvas.create_text(windowWidth*.5, cellHeight*.5, text="File organizer", fill="white")

        # Exit label
        iconLeave = tk.Button(self.mainCanvas, text="\u00d7", fg=fg, bg=bg, font=("Arial", 24), command=self.destroy, borderwidth=0)
        iconLeave.place(x=windowWidth-cellWidth*.25+borderThickness, y=borderThickness, width=cellWidth*.25, height=cellWidth*.25)

        # Main info text
        self.textMainInfo = self.mainCanvas.create_text(windowWidth*.5, windowHeight*.8, text="File organizer", fill="white", font=("Arial", 10), justify="left")

        # Text input
        self.inputTextPlaceholder = "Enter folders to sort files here into, like the following:\nC:\\Users\\arihamed\\Pictures\nC:\\Users\\arihamed\\Videos"
        self.inputText = tk.Text(self.mainCanvas, fg="gray")
        self.inputText.insert(tk.INSERT, self.inputTextPlaceholder)
        self.inputText.bind("<FocusIn>", self.inputTextFocusIn)
        self.inputText.bind("<FocusOut>", self.inputTextFocusOut)
        self.inputText.place(x=50, y=cellHeight, width=windowWidth-100, height=windowHeight*.5)
        
    def windowMoveStart(self, e): self.x, self.y = e.x, e.y
    def windowMoveStop(self, e): self.x, self.y = None, None
    def windowMoveDo(self, e): self.geometry(f"+{self.winfo_x() + (e.x - self.x)}+{self.winfo_y() + (e.y - self.y)}")
    def getKeyPress(self, e): 
        match e.keycode:
            case 8: self.textlol = self.textlol[:-1]
            case _: self.textlol += e.char
        self.mainCanvas.itemconfigure(self.textMainInfo, text="Valid folders:\n"+"\n".join([x for x in self.inputText.get("1.0", "end-1c").split("\n") if os.path.isdir(x)]))

    def inputTextFocusIn(self, e):
        if self.inputText.get("1.0", "end-1c") == self.inputTextPlaceholder:
            self.inputText.delete("1.0", "end-1c")
            self.inputText.configure(fg="black")
    def inputTextFocusOut(self, e):
        if self.inputText.get("1.0", "end-1c") == "":
            self.inputText.insert(tk.INSERT, self.inputTextPlaceholder)
            self.inputText.configure(fg="gray")

    def ctrlEvent(self, e):
        if e.state == 4 and e.keysym == 'c':
            content = self.inputText.selection_get()
            self.clipboard_clear()
            self.clipboard_append(content)
            return "break"
        elif e.state == 4 and e.keysym == 'v':
            self.inputText.insert('end', self.selection_get(selection='CLIPBOARD'))
            return "break"
        else:
            return "break"

# \u2714
app = HomeActivity()
app.mainloop()