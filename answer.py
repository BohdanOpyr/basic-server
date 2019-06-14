import pickle, time, collage_maker, random
from tkinter import *
from tkinter import filedialog


try:
    questions = pickle.load(open('contact_us', 'rb'))
except:
    questions = []
    pickle.dump([], open('contact_us', 'wb'))


def main():
    tk = Tk()
    tk.title('feedback')
    questions_frame = Frame(tk, border=10)
    questions_frame.pack(side='left')
    Label(questions_frame, text='Choose question', font=('Ariel', 25)).pack()
    l = Listbox(questions_frame, width=100, height=50)
    l.pack()
    def answer():
        if len(l.curselection()) != 1:
            return
        id = l.curselection()[0]
        tk = Tk()
        tk.title('answer')
        text = Text(tk)
        text.pack()
        def answer_save():
            answer = text.get('0.0', END)
            tk.destroy()
            try:
                answers = pickle.load(open('answers', 'rb'))
            except:
                answers = {}
            answers[id] = answer
            pickle.dump(answers, open('answers', 'wb'))
        Button(tk, command=answer_save, text='Submit').pack()
    answer_frame = Frame(tk, border=10)
    answer_frame.pack(side='right')
    Label(answer_frame, text='Body', font=('Ariel', 25)).pack()
    c = Canvas(answer_frame, width=500, height=750)
    c.pack()
    Button(answer_frame, text='Answer', command=answer).pack()
    for topic, body, key in questions:
        l.insert(END, topic)
    while True:
        tk.update()
        if len(l.curselection()) == 1:
            topic, body, key = questions[l.curselection()[0]]
            c.delete('all')
            c.create_text(250, 375, text=body)
    tk.mainloop()

if __name__ == '__main__':
    main()
