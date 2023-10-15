import tkinter as tk
from tkinter import ttk
import sqlite3


# Класс Main
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Главное окно
    def init_main(self):
        # Создаем панель инструментов
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
# Добавление иконок
        self.add_img = tk.PhotoImage(file='C:/image/add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить контакт', command=self.open_dialog, bg='#d7d8e0',
                                    bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='C:/image/update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='C:/image/delete.png')
        btn_delete_dialog = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='C:/image/search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='beige', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='C:/image/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'fio', 'category', 'phone'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('fio', width=365, anchor=tk.CENTER)
        self.tree.column('category', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('fio', text='ФИО')
        self.tree.heading('category', text='Категория')
        self.tree.heading('phone', text='Телефон')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

# Добавление данных
    def records(self, fio, category, phone):
        self.db.insert_data(fio, category, phone)
        self.view_records()

# Обновление данных
    def update_record(self, fio, category, phone):
        self.db.c.execute('''UPDATE phonebook SET fio=?, category=?, phone=? WHERE ID=?''',
                          (fio, category, phone, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# вывод данных в виджет таблицы 
    def view_records(self):
        # выбираем информацию из БД
        self.db.c.execute('''SELECT * FROM phonebook''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# УДАЛЕНИЕ ЗАПИСЕЙ 
    def delete_records(self):
        # цикл по выделенным записям 
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.c.execute('''DELETE FROM phonebook WHERE id=? ''', (self.tree.set(selection_item, '#1'),))
            # сохранение изменений в БД 
            self.db.conn.commit()
            # обновление виджета таблицы
            self.view_records()

# поиск записи 
    def search_records(self, fio):
        fio = ('%' + fio + '%',)
        self.db.c.execute('''SELECT * FROM phonebook WHERE fio LIKE ?''', fio)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

# Открытие дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child() # Вызываем
        self.view = app

    def init_child(self):
        # Заголовок окна
        self.title('Добавить контакт')
        # Размер окна
        self.geometry('400x220')
        # Ограничение изменения размеров окна
        self.resizable(False, False)

        # подписки
        label_fio = tk.Label(self, text='ФИО')
        label_fio.place(x=50, y=50)
        label_select = tk.Label(self, text='Категория')
        label_select.place(x=50, y=80)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=110)

        # добавляем строку ввода для наименования
        self.entry_fio = ttk.Entry(self)
        # меняем координаты объекта
        self.entry_fio.place(x=200, y=50)

        #Добавляем строку ввода телефона
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=110)

        # добавляем строку выбора категории
        self.combobox = ttk.Combobox(self, values=[u'Школа', u'Друзья', 'Работа'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=150)

        #Кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=150)
        #Срабатывания по ПКМ
		# при нажатии кнопки вызывается метод records, которому передаются значения из трок ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_fio.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_phone.get()))

        self.grab_set() # перехватываем все события происходящие в придожении
        self.focus_set() # Сфокусирован на окне которое открыто


# Класс обновления унаследованный от дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()


    def init_edit(self):
        self.title('Редактировать контакт')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=150)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_fio.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_phone.get()))
        # закрываем окно редактирования 
        self.btn_ok.destroy()


    def default_data(self):
        self.db.c.execute('''SELECT * FROM phonebook WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_fio.insert(0, row[1])
        if row[2] != 'Школа':
            self.combobox.current(1)
        self.entry_phone.insert(0, row[3])


# класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# создание базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('phonebook.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS phonebook (id integer primary key,fio text, 
            category text, phone text)''')
        self.conn.commit()

    def insert_data(self, fio, category, phone):
        self.c.execute('''INSERT INTO phonebook (fio, category, phone) VALUES (?, ?, ?) ''',
                       (fio, category, phone))
        self.conn.commit()


# основной код для запуска
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    # Заголовок окна
    root.title("Телефоная книга, Phone book")
    # Размер окна
    root.geometry("665x450")
    # Ограничение изменения размеров окна
    root.resizable(False, False)
    root.mainloop()