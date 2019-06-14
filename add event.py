import pickle, time, collage_maker, random
from tkinter import *
from tkinter import filedialog


try:
    news = pickle.load(open('news', 'rb'))
except:
    news = []
    pickle.dump([], open('news', 'wb'))


def add(title, images, text):
    num = random.randint(0, 1000000000)
    collage_maker.make_collage(images, 'collages/news_collage_%d.png'%num, 1000, 500)
    news.append([time.ctime(), images, text, num, title])


def main():
    tk = Tk()
    images = Frame(tk, border=10)
    Label(images, text='Choose several images', font=('Ariel', 25)).pack()
    l = Listbox(images, width=100, height=50)
    l.pack()
    Button(images, text="Delete",
           command=lambda l=l: l.delete(ANCHOR)).pack(side='right')
    Button(images, text="Add",
           command=lambda: l.insert(END, filedialog.Open(tk).show())).pack(side='left')
    images.pack(side='left')
    text = Frame(tk, border=10)
    Label(text, text='Info:', font=('Ariel', 25)).pack()
    Label(text, text='Title', font=('Ariel', 10)).pack()
    title = Entry(text)
    title.pack()
    Label(text, text='Body', font=('Ariel', 10)).pack()
    body = Text(text, width=100, height=50)
    body.pack()
    text.pack(side='right')
    def create():
        print(title.get(), list(l.get(0, END)), body.get('0.0', END))
        add(title.get(), list(l.get(0, END)), body.get('0.0', END))
        tk.destroy()
        pickle.dump(news, open('news', 'wb'))
    Button(tk, text='CREATE', command=create).pack(side='bottom')
    tk.mainloop()

if __name__ == '__main__':
    main()
