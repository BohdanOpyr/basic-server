import pickle
try:
    data = pickle.load(open('data', 'rb'))
except FileNotFoundError:
    data = {'name':'user', 'logo':'white.png', 'color tones':'0, 0, 0', 'bgcolor tones':'255, 255, 255'}


from tkinter import *
from tkinter import _tkinter
tk = Tk()
inputs = {}
for n in data:
    c = Canvas(tk, width=200, height=20)
    c.pack()
    c.create_text(100, 10, text=n)
    e = Entry(tk)
    e.insert(END, data[n])
    e.pack()
    inputs[n] = e
def save():
    for n in inputs:
        data[n] = inputs[n].get()
    pickle.dump(data, open('data', 'wb'))
b = Button(tk, command=save, text='update')
b.pack()
try:
    while True:
        tk.update()
except _tkinter.TclError:
    save()
