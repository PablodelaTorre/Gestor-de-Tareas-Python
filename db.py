from tkinter import *
import sqlite3

root = Tk()
root.title('Gestor de Tareas')
root.geometry('500x500')
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)


conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id, ))
        conn.commit()
        render_todos
    return _remove

#Currying
def complete(id):
    def _complete():
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()

    return _complete

def render_todos():
    rows = c.execute("SELECT * FROM todo").fetchall()
    
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else '#eb4034'
        l = Checkbutton(frame, text=description, width=42, fg=color, anchor='w', command=complete(id))
        l.grid(row=i, column=0, sticky='w')
        l.select() if completed else l.deselect()
        btn1 = Button(frame, text='Eliminar', command=remove(id))
        btn1.grid(row=i, column=1)

def addtodo():
    todo = e.get()
    if todo:
        c.execute("""
            INSERT INTO todo (description, completed) VALUES (?, ?)
        """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addtodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5)

e.focus()

root.bind('<Return>', lambda x: addtodo())

render_todos()

root.mainloop()
