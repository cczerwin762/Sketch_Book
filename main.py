import tkinter as tk
from tkinter import Frame, Label, Menu, Button, PhotoImage
from PIL import Image
import os

class sketchPad():
    def __init__(self,width = 500, height = 500):
        self.cursorcolor = "#ffffff"
        self.bgcolor = "#000000"
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.root.wm_title("SketchPad")
        self.root.geometry('500x500+200+200')
        self.canvas = tk.Canvas(self.root, height=self.width, width=self.height, bg=self.bgcolor)
        self.menu = Menu(self.root)
        self.file = Menu(self.menu, tearoff = 0)
        self.help = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label = "File", menu = self.file)
        self.menu.add_cascade(label = "Help", menu = self.help)
        self.file.add_command(label = "Save", command=self.save_callback)
        self.help.add_command(label = "How to Use", command = self.display_help)
        # Make into an executable
        self.root.config(menu=self.menu)
        self.img = None
        self.canvas.pack(side = tk.BOTTOM)
        self.howto = None
        self.save = None
        self.create()
        self.root.mainloop()


    def create(self):
        self.img = PhotoImage(width=self.width, height=self.height)
        self.canvas.create_image((self.width // 2, self.height // 2), image=self.img, state="normal")
        self.canvas.bind("<Button-1>", self.clicked_callback)
        self.canvas.bind("<B1-Motion>", self.clicked_callback)
        self.canvas.bind("<Button-2>", self.change_cursorcolor)
        self.canvas.bind("<Button-3>", self.clear_callback)
        self.canvas.focus_set()
        self.canvas.bind("<space>", self.invert_colorscheme)

    def clicked_callback(self, event):
        self.img.put(self.cursorcolor,(event.x,event.y))
        self.root.update()

    def clear_callback(self, event):
        self.canvas.delete("all")
        self.create()
        self.root.update()

    def change_cursorcolor(self,event):
        self.cursorcolor = ("#ffffff" if self.cursorcolor == "#000000" else "#000000")

    def invert_colorscheme(self, event):
        (self.bgcolor, self.cursorcolor) = ("#ffffff","#000000") if self.bgcolor=="#000000" else ("#000000", "#ffffff")
        self.canvas.delete("all")
        self.canvas.configure(bg = self.bgcolor)
        self.create()
        self.root.update()

    def save_callback(self):
        self.save = tk.Tk()
        self.savename = tk.StringVar(self.save)
        self.save.wm_title("Save")
        self.saveframe = Frame(self.save)
        self.saveframe.pack()
        self.saveas = Label(self.saveframe, text = "Save as: ")
        self.saveas.pack(side = tk.TOP)
        self.savenameentry = tk.Entry(self.saveframe, textvariable = self.savename).pack(side=tk.LEFT)
        self.savebutton = Button(self.saveframe, text = "Save", command = self.save_as_jpeg)
        self.savebutton.pack(side = tk.RIGHT)
        self.save.update()
        self.save.mainloop()

    def display_help(self):
        self.howto = tk.Tk()
        self.howto.wm_title("How to Use")
        self.howtoframe = Frame(self.howto)
        self.howtoframe.pack()
        self.text = tk.Text(self.howtoframe, height = 8, width = 65)
        self.text.pack()
        self.text.insert(tk.END,
                        "Welcome!\n"
                        "- Click and drag mouse to draw,\n- Right click to clear,\n- Middle click to change cursor color,\n"
                        "- Press space to clear image and change background color.")
        self.howto.mainloop()

    def save_as_jpeg(self):
        print("saving")
        name = self.savename.get() +".jpg"
        self.savename.set("")
        self.canvas.postscript(file = name)
        savedimg = Image.open(name)
        savedimg.save(name,"JPEG")





if __name__ == "__main__":
    sketchPad = sketchPad()
